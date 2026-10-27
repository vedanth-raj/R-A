"""
AI Conversation Engine for Draft Generation
Provides natural, conversational AI interaction like Gemini AI
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    import google.genai as genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class AIConversationEngine:
    """
    Conversational AI engine for natural interaction during draft generation.
    Works like Gemini AI with context awareness and intelligent responses.
    """
    
    def __init__(self):
        """Initialize the conversation engine with Gemini AI."""
        self.logger = logging.getLogger(__name__)
        self.gemini_client = None
        self.conversation_history = []
        self.context = {
            'topic': None,
            'papers': [],
            'user_preferences': {},
            'draft_sections': {}
        }
        self._setup_gemini()
    
    def _setup_gemini(self):
        """Setup Gemini AI client."""
        if GEMINI_AVAILABLE:
            gemini_key = os.getenv('GEMINI_API_KEY')
            if gemini_key:
                try:
                    self.gemini_client = genai.Client(api_key=gemini_key)
                    self.gemini_model = "gemini-2.5-flash"  # Latest stable model
                    self.logger.info("AI Conversation Engine initialized with Gemini")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize Gemini: {e}")
            else:
                self.logger.warning("No Gemini API key found in environment")
    
    def set_context(self, topic: str, papers: List[Dict], user_preferences: Dict = None):
        """Set the conversation context."""
        self.context['topic'] = topic
        self.context['papers'] = papers
        self.context['user_preferences'] = user_preferences or {}
        self.logger.info(f"Context set: topic='{topic}', papers={len(papers)}")
    
    def chat(self, user_message: str) -> str:
        """
        Have a natural conversation with the AI about draft generation.
        
        Args:
            user_message: User's message/question/instruction
            
        Returns:
            AI's response
        """
        if not self.gemini_client:
            return "AI conversation engine not available. Please check your Gemini API key."
        
        # Build conversation context
        context_prompt = self._build_context_prompt()
        
        # Add user message to history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Build full conversation prompt
        full_prompt = f"""{context_prompt}

CONVERSATION HISTORY:
{self._format_conversation_history()}

USER: {user_message}

AI ASSISTANT: """
        
        try:
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,  # Higher for more natural conversation
                    max_output_tokens=1000
                )
            )
            
            ai_response = response.text.strip()
            
            # Add AI response to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            return ai_response
            
        except Exception as e:
            self.logger.error(f"AI conversation failed: {e}")
            return f"I apologize, but I encountered an error: {str(e)}. Could you please try rephrasing your request?"
    
    def generate_with_conversation(self, section_type: str, initial_instruction: str = None) -> Tuple[str, str]:
        """
        Generate a draft section with conversational AI guidance.
        
        Args:
            section_type: Type of section to generate
            initial_instruction: Optional initial instruction from user
            
        Returns:
            Tuple of (draft_content, ai_explanation)
        """
        if not self.gemini_client:
            return ("AI not available", "Please check your Gemini API key.")
        
        # Build generation prompt with conversation style
        prompt = self._build_generation_prompt(section_type, initial_instruction)
        
        try:
            import time
            start_time = time.time()
            
            self.logger.info(f"Starting conversational generation for {section_type}")
            
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=800,
                    timeout=30  # 30 second timeout
                )
            )
            
            elapsed = time.time() - start_time
            self.logger.info(f"Conversational generation completed in {elapsed:.2f} seconds")
            
            full_response = response.text.strip()
            
            # Try to separate explanation from content
            if "---DRAFT CONTENT---" in full_response:
                parts = full_response.split("---DRAFT CONTENT---")
                explanation = parts[0].strip()
                content = parts[1].strip() if len(parts) > 1 else full_response
            else:
                explanation = "I've generated the draft based on your requirements."
                content = full_response
            
            # Store in context
            self.context['draft_sections'][section_type] = content
            
            return (content, explanation)
            
        except TimeoutError as e:
            self.logger.error(f"Conversational generation timed out: {e}")
            return ("", "Generation timed out. Please try again.")
        except Exception as e:
            self.logger.error(f"Generation with conversation failed: {e}")
            return ("", f"I encountered an error: {str(e)}")
    
    def improve_draft(self, draft_content: str, improvement_request: str) -> Tuple[str, str]:
        """
        Improve a draft based on conversational feedback.
        
        Args:
            draft_content: Current draft content
            improvement_request: User's improvement request
            
        Returns:
            Tuple of (improved_content, ai_explanation)
        """
        if not self.gemini_client:
            return (draft_content, "AI not available")
        
        prompt = f"""Improve this draft based on user feedback.

CURRENT DRAFT:
{draft_content[:1500]}

USER REQUEST: {improvement_request}

Respond in two parts:
1. Brief explanation of changes (1-2 sentences)
2. Improved draft

Format:
[Brief explanation]

---IMPROVED DRAFT---
[Improved content]"""
        
        try:
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=1000  # Reduced from 1500 for speed
                )
            )
            
            full_response = response.text.strip()
            
            # Separate explanation from improved content
            if "---IMPROVED DRAFT---" in full_response:
                parts = full_response.split("---IMPROVED DRAFT---")
                explanation = parts[0].strip()
                improved_content = parts[1].strip() if len(parts) > 1 else draft_content
            else:
                explanation = "I've made improvements based on your feedback."
                improved_content = full_response
            
            return (improved_content, explanation)
            
        except Exception as e:
            self.logger.error(f"Draft improvement failed: {e}")
            return (draft_content, f"I encountered an error: {str(e)}")
    
    def ask_clarification(self, section_type: str) -> str:
        """
        AI asks for clarification before generating.
        
        Args:
            section_type: Type of section to generate
            
        Returns:
            AI's clarification question
        """
        if not self.gemini_client:
            return "What specific aspects would you like me to focus on?"
        
        prompt = f"""You are an expert academic writing assistant. The user wants to generate a {section_type} section for their research paper on "{self.context.get('topic', 'their topic')}".

Before generating, ask them 2-3 helpful clarifying questions to ensure you create exactly what they need. Be conversational and friendly.

For example:
- What tone would you prefer? (formal academic, accessible, technical)
- Are there specific aspects you want emphasized?
- What length would work best for your needs?
- Any particular structure or format you prefer?

Ask questions relevant to a {section_type} section."""
        
        try:
            response = self.gemini_client.models.generate_content(
                model=self.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9,
                    max_output_tokens=300
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            self.logger.error(f"Clarification request failed: {e}")
            return "What specific aspects would you like me to focus on in this section?"
    
    def _build_context_prompt(self) -> str:
        """Build context prompt for conversation."""
        return f"""You are an expert academic writing assistant with a friendly, conversational personality. You're helping a researcher write a systematic review.

CURRENT CONTEXT:
- Research Topic: {self.context.get('topic', 'Not specified')}
- Number of Papers: {len(self.context.get('papers', []))}
- Sections Generated: {', '.join(self.context.get('draft_sections', {}).keys()) or 'None yet'}

YOUR ROLE:
- Be helpful, friendly, and conversational
- Provide expert academic writing guidance
- Ask clarifying questions when needed
- Explain your reasoning
- Adapt to the user's preferences
- Be encouraging and supportive

GUIDELINES:
- Use natural, conversational language
- Be concise but thorough
- Show enthusiasm for helping
- Acknowledge user's requests clearly
- Offer suggestions proactively"""
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for context."""
        if not self.conversation_history:
            return "No previous conversation."
        
        formatted = []
        for msg in self.conversation_history[-6:]:  # Last 6 messages for context
            role = "USER" if msg['role'] == 'user' else "AI"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def _build_generation_prompt(self, section_type: str, initial_instruction: str = None) -> str:
        """Build prompt for draft generation with conversation."""
        base_instructions = {
            'abstract': 'a concise abstract (250-350 words)',
            'introduction': 'an introduction (500-700 words)',
            'methodology': 'a methods section (400-600 words)',
            'methods': 'a methods section (400-600 words)',
            'results': 'a results section (500-700 words)',
            'discussion': 'a discussion (500-700 words)',
            'references': 'APA references'
        }
        
        section_instruction = base_instructions.get(section_type, f'a {section_type} section')
        
        prompt = f"""Generate {section_instruction} for a review on "{self.context.get('topic', 'the topic')}" analyzing {len(self.context.get('papers', []))} papers.

"""
        
        if initial_instruction:
            prompt += f"""USER INSTRUCTIONS: {initial_instruction}

"""
        
        prompt += f"""Respond in two parts:
1. Brief explanation (1-2 sentences)
2. The content

Format:
[Brief explanation]

---DRAFT CONTENT---
[The {section_type} content]"""
        
        return prompt
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        self.logger.info("Conversation history reset")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation."""
        if not self.conversation_history:
            return "No conversation yet."
        
        total_messages = len(self.conversation_history)
        user_messages = sum(1 for msg in self.conversation_history if msg['role'] == 'user')
        ai_messages = sum(1 for msg in self.conversation_history if msg['role'] == 'assistant')
        
        return f"Conversation: {total_messages} messages ({user_messages} from you, {ai_messages} from AI)"


if __name__ == "__main__":
    # Test the conversation engine
    engine = AIConversationEngine()
    
    # Set context
    engine.set_context(
        topic="Machine Learning in Healthcare",
        papers=[{"title": "Sample Paper 1"}, {"title": "Sample Paper 2"}]
    )
    
    # Test conversation
    print("AI:", engine.chat("Hi, I need help writing an abstract"))
    print("\nAI:", engine.chat("Make it focus on recent advances"))
    
    # Test generation
    content, explanation = engine.generate_with_conversation("abstract", "Focus on clinical applications")
    print(f"\nExplanation: {explanation}")
    print(f"\nContent preview: {content[:200]}...")

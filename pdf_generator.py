"""
PDF Generator for Research Drafts
Converts generated drafts to formatted PDF documents
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime
import os
import re

class DraftPDFGenerator:
    """Generate formatted PDF from research drafts"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor='#1a1a1a',
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor='#2c3e50',
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection heading style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor='#34495e',
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor='#333333',
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        ))
        
        # Citation style
        self.styles.add(ParagraphStyle(
            name='Citation',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor='#555555',
            leftIndent=20,
            spaceAfter=8
        ))
    
    def _clean_text(self, text):
        """Clean text for PDF rendering"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Escape special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text.strip()
    
    def _parse_draft_sections(self, draft_text):
        """Parse draft text into sections"""
        sections = []
        current_section = None
        current_content = []
        
        lines = draft_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for section headers (lines with ## or all caps)
            if line.startswith('##') or (line.isupper() and len(line) > 3):
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content)
                    })
                
                # Start new section
                current_section = line.replace('##', '').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Add last section
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content)
            })
        
        return sections
    
    def generate_comprehensive_pdf(self, draft_text, output_path, title="Research Draft", metadata=None):
        """Generate comprehensive PDF from draft text"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Add title
        story.append(Paragraph(self._clean_text(title), self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Add metadata if provided
        if metadata:
            meta_text = f"Generated: {datetime.now().strftime('%B %d, %Y')}"
            if 'papers_count' in metadata:
                meta_text += f" | Papers Analyzed: {metadata['papers_count']}"
            story.append(Paragraph(meta_text, self.styles['Normal']))
            story.append(Spacer(1, 0.5*inch))
        
        # Parse and add sections
        sections = self._parse_draft_sections(draft_text)
        
        for section in sections:
            # Add section title
            story.append(Paragraph(self._clean_text(section['title']), self.styles['SectionHeading']))
            
            # Add section content
            paragraphs = section['content'].split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(self._clean_text(para), self.styles['CustomBody']))
                    story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def generate_topic_wise_pdf(self, topics_dict, output_path, title="Topic-Wise Research Analysis"):
        """Generate topic-wise PDF with separate sections for each topic"""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Add title
        story.append(Paragraph(self._clean_text(title), self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Add generation date
        meta_text = f"Generated: {datetime.now().strftime('%B %d, %Y')} | Topics: {len(topics_dict)}"
        story.append(Paragraph(meta_text, self.styles['Normal']))
        story.append(Spacer(1, 0.5*inch))
        
        # Add table of contents
        story.append(Paragraph("Table of Contents", self.styles['SectionHeading']))
        for i, topic in enumerate(topics_dict.keys(), 1):
            story.append(Paragraph(f"{i}. {self._clean_text(topic)}", self.styles['Normal']))
        story.append(PageBreak())
        
        # Add each topic section
        for topic, content in topics_dict.items():
            # Topic title
            story.append(Paragraph(self._clean_text(topic), self.styles['SectionHeading']))
            story.append(Spacer(1, 0.2*inch))
            
            # Parse subsections if any
            if isinstance(content, dict):
                for subtopic, subcontent in content.items():
                    story.append(Paragraph(self._clean_text(subtopic), self.styles['SubsectionHeading']))
                    story.append(Paragraph(self._clean_text(str(subcontent)), self.styles['CustomBody']))
                    story.append(Spacer(1, 0.15*inch))
            else:
                # Add content paragraphs
                paragraphs = str(content).split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(self._clean_text(para), self.styles['CustomBody']))
                        story.append(Spacer(1, 0.1*inch))
            
            # Page break between topics
            story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def generate_from_papers(self, papers_data, output_path, draft_type="comprehensive"):
        """Generate PDF from papers data structure"""
        if draft_type == "comprehensive":
            # Combine all paper content
            combined_text = ""
            for paper in papers_data:
                combined_text += f"\n\n## {paper.get('title', 'Untitled')}\n\n"
                combined_text += paper.get('content', paper.get('abstract', ''))
            
            return self.generate_comprehensive_pdf(
                combined_text,
                output_path,
                title="Comprehensive Research Analysis",
                metadata={'papers_count': len(papers_data)}
            )
        
        elif draft_type == "topic_wise":
            # Organize by topics
            topics_dict = {}
            for paper in papers_data:
                title = paper.get('title', 'Untitled')
                content = paper.get('content', paper.get('abstract', ''))
                topics_dict[title] = content
            
            return self.generate_topic_wise_pdf(
                topics_dict,
                output_path,
                title="Topic-Wise Research Analysis"
            )

# Convenience functions
def generate_pdf(draft_text, output_path, pdf_type="comprehensive", **kwargs):
    """
    Generate PDF from draft text
    
    Args:
        draft_text: The draft content
        output_path: Where to save the PDF
        pdf_type: 'comprehensive' or 'topic_wise'
        **kwargs: Additional metadata
    """
    generator = DraftPDFGenerator()
    
    if pdf_type == "comprehensive":
        return generator.generate_comprehensive_pdf(draft_text, output_path, **kwargs)
    elif pdf_type == "topic_wise":
        # Parse topics from text
        sections = generator._parse_draft_sections(draft_text)
        topics_dict = {s['title']: s['content'] for s in sections}
        return generator.generate_topic_wise_pdf(topics_dict, output_path)
    
    return None

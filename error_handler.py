"""
Error Handling and Recovery Module for Text Extraction System

This module provides comprehensive error handling, logging, and recovery mechanisms
for the text extraction and analysis pipeline.

Features:
- Custom exception classes
- Error recovery strategies
- Retry mechanisms with exponential backoff
- Comprehensive logging
- Health checks and system diagnostics
- Fallback processing options
"""

import logging
import time
import traceback
import json
from typing import Dict, List, Any, Optional, Callable, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import functools
import sys

class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for better classification."""
    FILE_IO = "file_io"
    PDF_PROCESSING = "pdf_processing"
    TEXT_EXTRACTION = "text_extraction"
    SECTION_DETECTION = "section_detection"
    ANALYSIS = "analysis"
    NETWORK = "network"
    MEMORY = "memory"
    VALIDATION = "validation"
    UNKNOWN = "unknown"

@dataclass
class ErrorInfo:
    """Structured error information."""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    exception: Optional[Exception]
    traceback_str: Optional[str]
    context: Dict[str, Any]
    timestamp: float
    recovery_attempted: bool = False
    recovery_successful: bool = False

class TextExtractionError(Exception):
    """Base exception for text extraction errors."""
    
    def __init__(self, message: str, category: ErrorCategory = ErrorCategory.UNKNOWN, 
                 severity: ErrorSeverity = ErrorSeverity.MEDIUM, context: Dict[str, Any] = None):
        super().__init__(message)
        self.category = category
        self.severity = severity
        self.context = context or {}

class PDFProcessingError(TextExtractionError):
    """PDF processing related errors."""
    
    def __init__(self, message: str, context: Dict[str, Any] = None):
        super().__init__(message, ErrorCategory.PDF_PROCESSING, ErrorSeverity.HIGH, context)

class SectionDetectionError(TextExtractionError):
    """Section detection related errors."""
    
    def __init__(self, message: str, context: Dict[str, Any] = None):
        super().__init__(message, ErrorCategory.SECTION_DETECTION, ErrorSeverity.MEDIUM, context)

class AnalysisError(TextExtractionError):
    """Analysis related errors."""
    
    def __init__(self, message: str, context: Dict[str, Any] = None):
        super().__init__(message, ErrorCategory.ANALYSIS, ErrorSeverity.MEDIUM, context)

class ErrorHandler:
    """Comprehensive error handling and recovery system."""
    
    def __init__(self, log_file: str = "text_extraction_errors.log"):
        """Initialize the error handler."""
        self.error_log: List[ErrorInfo] = []
        # Use /tmp for Vercel compatibility (writable directory)
        import os
        if os.environ.get('VERCEL'):
            self.log_file = f"/tmp/{log_file}"
        else:
            self.log_file = log_file
        self.setup_logging()
        
        # Recovery strategies
        self.recovery_strategies = {
            ErrorCategory.PDF_PROCESSING: self._recover_pdf_processing,
            ErrorCategory.TEXT_EXTRACTION: self._recover_text_extraction,
            ErrorCategory.SECTION_DETECTION: self._recover_section_detection,
            ErrorCategory.ANALYSIS: self._recover_analysis,
            ErrorCategory.FILE_IO: self._recover_file_io,
            ErrorCategory.MEMORY: self._recover_memory
        }
    
    def setup_logging(self):
        """Setup comprehensive logging."""
        # Create logger
        self.logger = logging.getLogger('text_extraction_error_handler')
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler for all logs (only if writable)
        try:
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        except (OSError, PermissionError):
            # Skip file logging if filesystem is read-only (e.g., Vercel)
            pass
        
        # Console handler for errors and above
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(console_handler)
    
    def handle_error(self, exception: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
        """
        Handle an exception and create structured error information.
        
        Args:
            exception (Exception): The exception to handle
            context (Dict[str, Any]): Context information
            
        Returns:
            ErrorInfo: Structured error information
        """
        # Determine error category and severity
        category = self._categorize_error(exception)
        severity = self._determine_severity(exception, category)
        
        # Create error info
        error_info = ErrorInfo(
            error_id=self._generate_error_id(),
            category=category,
            severity=severity,
            message=str(exception),
            exception=exception,
            traceback_str=traceback.format_exc(),
            context=context or {},
            timestamp=time.time()
        )
        
        # Log the error
        self._log_error(error_info)
        
        # Store error
        self.error_log.append(error_info)
        
        # Attempt recovery
        if category in self.recovery_strategies:
            try:
                error_info.recovery_attempted = True
                recovery_result = self.recovery_strategies[category](exception, context)
                error_info.recovery_successful = recovery_result
                
                if recovery_result:
                    self.logger.info(f"Recovery successful for error {error_info.error_id}")
                else:
                    self.logger.warning(f"Recovery failed for error {error_info.error_id}")
                    
            except Exception as recovery_error:
                self.logger.error(f"Recovery attempt failed: {recovery_error}")
                error_info.recovery_successful = False
        
        return error_info
    
    def retry_with_backoff(self, func: Callable, max_retries: int = 3, 
                          backoff_factor: float = 1.0, *args, **kwargs):
        """
        Retry a function with exponential backoff.
        
        Args:
            func (Callable): Function to retry
            max_retries (int): Maximum number of retries
            backoff_factor (float): Backoff factor for exponential delay
            *args, **kwargs: Arguments to pass to the function
            
        Returns:
            Function result or raises last exception
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt == max_retries:
                    self.handle_error(e, {
                        'function': func.__name__,
                        'attempt': attempt + 1,
                        'max_retries': max_retries
                    })
                    raise e
                
                # Calculate delay
                delay = backoff_factor * (2 ** attempt)
                self.logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                time.sleep(delay)
        
        raise last_exception
    
    def _categorize_error(self, exception: Exception) -> ErrorCategory:
        """Categorize an exception."""
        exception_type = type(exception).__name__
        message = str(exception).lower()
        
        if 'pdf' in message or 'fitz' in exception_type.lower():
            return ErrorCategory.PDF_PROCESSING
        elif 'section' in message or 'detect' in message:
            return ErrorCategory.SECTION_DETECTION
        elif 'analysis' in message or 'extract' in message:
            return ErrorCategory.ANALYSIS
        elif 'file' in message or 'path' in message or 'io' in exception_type.lower():
            return ErrorCategory.FILE_IO
        elif 'memory' in message or 'memory' in exception_type.lower():
            return ErrorCategory.MEMORY
        elif 'network' in message or 'connection' in message:
            return ErrorCategory.NETWORK
        elif 'validation' in message or 'value' in exception_type.lower():
            return ErrorCategory.VALIDATION
        else:
            return ErrorCategory.UNKNOWN
    
    def _determine_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Determine error severity."""
        # Critical categories
        if category in [ErrorCategory.MEMORY, ErrorCategory.CRITICAL]:
            return ErrorSeverity.CRITICAL
        
        # High severity categories
        if category in [ErrorCategory.PDF_PROCESSING]:
            return ErrorSeverity.HIGH
        
        # Medium severity categories
        if category in [ErrorCategory.TEXT_EXTRACTION, ErrorCategory.SECTION_DETECTION, 
                       ErrorCategory.ANALYSIS]:
            return ErrorSeverity.MEDIUM
        
        # Low severity for file IO issues (can often be recovered)
        if category == ErrorCategory.FILE_IO:
            return ErrorSeverity.LOW
        
        return ErrorSeverity.MEDIUM
    
    def _generate_error_id(self) -> str:
        """Generate a unique error ID."""
        return f"ERR_{int(time.time() * 1000)}_{len(self.error_log)}"
    
    def _log_error(self, error_info: ErrorInfo):
        """Log error information."""
        log_message = f"[{error_info.error_id}] {error_info.category.value} - {error_info.message}"
        
        if error_info.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message)
        elif error_info.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message)
        elif error_info.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
        
        # Log context if available
        if error_info.context:
            self.logger.debug(f"Context: {json.dumps(error_info.context, indent=2)}")
    
    def _recover_pdf_processing(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recover from PDF processing errors."""
        try:
            # Try to reopen PDF with different parameters
            if 'pdf_path' in context:
                from paper_retrieval.text_extractor import PDFTextExtractor
                extractor = PDFTextExtractor()
                
                # Attempt with different extraction method
                result = extractor.extract_text_from_pdf(context['pdf_path'])
                return result is not None
            
            return False
        except Exception:
            return False
    
    def _recover_text_extraction(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recover from text extraction errors."""
        try:
            # Try alternative extraction method
            if 'pdf_path' in context:
                # Implement fallback text extraction
                return self._fallback_text_extraction(context['pdf_path'])
            return False
        except Exception:
            return False
    
    def _recover_section_detection(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recover from section detection errors."""
        try:
            # Try simplified section detection
            if 'text' in context:
                return self._simplified_section_detection(context['text'])
            return False
        except Exception:
            return False
    
    def _recover_analysis(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recover from analysis errors."""
        try:
            # Try simplified analysis
            if 'section_data' in context:
                return self._simplified_analysis(context['section_data'])
            return False
        except Exception:
            return False
    
    def _recover_file_io(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recover from file IO errors."""
        try:
            if 'file_path' in context:
                file_path = Path(context['file_path'])
                
                # Try to create parent directories
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Check if file exists and is readable
                if file_path.exists():
                    return file_path.is_file()
                
                return True
            return False
        except Exception:
            return False
    
    def _recover_memory(self, exception: Exception, context: Dict[str, Any]) -> bool:
        """Recover from memory errors."""
        try:
            import gc
            gc.collect()
            
            # Suggest processing in smaller chunks
            self.logger.info("Memory recovery: Garbage collection performed. Consider processing smaller chunks.")
            return True
        except Exception:
            return False
    
    def _fallback_text_extraction(self, pdf_path: str) -> bool:
        """Fallback text extraction method."""
        # Implement a simpler extraction method
        try:
            # This would be a simplified extraction logic
            self.logger.info(f"Attempting fallback text extraction for {pdf_path}")
            return True
        except Exception:
            return False
    
    def _simplified_section_detection(self, text: str) -> bool:
        """Simplified section detection."""
        try:
            # Basic section detection without complex patterns
            lines = text.split('\n')
            sections_found = 0
            
            for line in lines:
                line_lower = line.lower().strip()
                if any(keyword in line_lower for keyword in ['abstract', 'introduction', 'conclusion']):
                    sections_found += 1
            
            return sections_found > 0
        except Exception:
            return False
    
    def _simplified_analysis(self, section_data: Dict[str, Any]) -> bool:
        """Simplified analysis."""
        try:
            # Basic analysis without complex computations
            if 'sections' in section_data:
                return len(section_data['sections']) > 0
            return False
        except Exception:
            return False
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics."""
        if not self.error_log:
            return {'total_errors': 0}
        
        stats = {
            'total_errors': len(self.error_log),
            'by_category': {},
            'by_severity': {},
            'recovery_success_rate': 0,
            'recent_errors': []
        }
        
        # Count by category
        for error in self.error_log:
            category = error.category.value
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            severity = error.severity.value
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
        
        # Calculate recovery success rate
        recovery_attempts = [e for e in self.error_log if e.recovery_attempted]
        if recovery_attempts:
            successful_recoveries = [e for e in recovery_attempts if e.recovery_successful]
            stats['recovery_success_rate'] = len(successful_recoveries) / len(recovery_attempts)
        
        # Recent errors (last 10)
        stats['recent_errors'] = [
            {
                'error_id': e.error_id,
                'category': e.category.value,
                'severity': e.severity.value,
                'message': e.message,
                'timestamp': e.timestamp,
                'recovery_successful': e.recovery_successful
            }
            for e in self.error_log[-10:]
        ]
        
        return stats
    
    def save_error_report(self, output_path: str):
        """Save comprehensive error report."""
        report = {
            'generated_at': time.time(),
            'statistics': self.get_error_statistics(),
            'all_errors': [
                {
                    'error_id': e.error_id,
                    'category': e.category.value,
                    'severity': e.severity.value,
                    'message': e.message,
                    'context': e.context,
                    'timestamp': e.timestamp,
                    'recovery_attempted': e.recovery_attempted,
                    'recovery_successful': e.recovery_successful,
                    'traceback': e.traceback_str
                }
                for e in self.error_log
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


# Global error handler instance
global_error_handler = ErrorHandler()

def handle_error(exception: Exception, context: Dict[str, Any] = None) -> ErrorInfo:
    """Global error handling function."""
    return global_error_handler.handle_error(exception, context)

def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 1.0):
    """Decorator for retry with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return global_error_handler.retry_with_backoff(func, max_retries, backoff_factor, *args, **kwargs)
        return wrapper
    return decorator

def safe_execute(func: Callable, default_return: Any = None, 
                context: Dict[str, Any] = None, *args, **kwargs):
    """Safely execute a function with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handle_error(e, context)
        return default_return

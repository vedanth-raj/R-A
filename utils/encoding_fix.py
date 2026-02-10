"""
Encoding fix utility for Windows console
Ensures proper UTF-8 encoding for Unicode characters
"""

import sys
import codecs


def fix_console_encoding():
    """
    Fix Windows console encoding to support Unicode characters.
    Call this at the start of any script that prints to console.
    """
    if sys.platform == 'win32':
        try:
            # Python 3.7+
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            # Python < 3.7
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def safe_print(text, fallback_encoding='ascii'):
    """
    Safely print text with Unicode characters.
    Falls back to ASCII with replacement if encoding fails.
    
    Args:
        text: Text to print
        fallback_encoding: Encoding to use if UTF-8 fails (default: 'ascii')
    """
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: encode with replacement characters
        safe_text = text.encode(fallback_encoding, 'replace').decode(fallback_encoding)
        print(safe_text)


# Auto-fix encoding when module is imported
fix_console_encoding()

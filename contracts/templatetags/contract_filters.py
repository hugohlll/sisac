from django import template
import re

register = template.Library()

@register.filter
def format_cpf(value):
    """
    Formats a CPF string (11 digits) into XXX.XXX.XXX-XX.
    Removes non-digits first.
    """
    if not value:
        return ""
    
    digits = re.sub(r'\D', '', str(value))
    
    if len(digits) != 11:
        return value # Return original if not 11 digits
        
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

@register.filter
def format_cep(value):
    """
    Formats a CEP string (8 digits) into XX.XXX-XXX.
    Removes non-digits first.
    Example: 21235650 -> 21.235-650
    """
    if not value:
        return ""
        
    digits = re.sub(r'\D', '', str(value))
    
    if len(digits) != 8:
        # If it's already formatted or different length, try to adapt or return original
        # The user example was 21.235-650 (10 chars, 8 digits)
        return value 
    
    return f"{digits[:2]}.{digits[2:5]}-{digits[5:]}"

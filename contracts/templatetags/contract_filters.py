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
    
    if len(digits) >= 11:
        # Take the first 11 digits if longer
        cpf = digits[:11]
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        
    return value # Return original if not enough digits

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

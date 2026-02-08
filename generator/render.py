from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

def render_pdf(template_src, context_dict, filename="document.pdf", base_url=None):
    """
    Render a PDF from a Django template.
    """
    html_string = render_to_string(template_src, context_dict)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    
    HTML(string=html_string, base_url=base_url).write_pdf(response)
    
    return response

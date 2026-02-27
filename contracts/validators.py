from django.core.exceptions import ValidationError
import os

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('O arquivo não pode exceder 5MB.')

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Formato não suportado. Use PDF, JPG ou PNG.')

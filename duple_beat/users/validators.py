from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


#   this file is used for DJANGO FORM validation. 
 
def validate_budget(value):
    
    if not 0 < len(value) < 3:
        raise ValidationError(
            _('%(value)s, this is not a valid budget range'),
            params={'value': value},
        )

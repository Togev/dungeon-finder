import re

from django.core.exceptions import ValidationError


def UsernameAlphaNumericUnderscoreValidator(value):
    if not re.match(r"[a-zA-Z][a-zA-Z0-9_]*", value):
        raise ValidationError('Username must start with a letter and can only contain letters, numbers and underscores.')
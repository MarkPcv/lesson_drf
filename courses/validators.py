from rest_framework.serializers import ValidationError

def validate_url(value: str):
    """
    Validates that URL leads to YouTube content
    """
    if "youtube.com" not in value:
        raise ValidationError("This content cannot be added!")

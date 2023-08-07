from rest_framework import serializers

from courses.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for :model:`users.User`
    """
    # List of payments
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'

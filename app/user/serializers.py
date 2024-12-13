"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import gettext as _


from rest_framework import serializers # type: ignore

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length':5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data) 
    
    def update(self, instance, validated_data): #Overriding update method instance of model to be updated
        """Update and return user."""
        password = validated_data.pop('password', None) #Retrieve password and remove it also from val dict, default none if they dont provide pass
        user = super().update(instance, validated_data) #Updating from parent class logic

        if password:  # if user provided new password during update
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField() #collects and validates email 
    password = serializers.CharField(
        style={'input_type':'password'}, #collects pass in plain text hidden ***
        trim_whitespace = False,    #dont trim whitespaces
    )

    def validate(self,attrs): #dict including validated fields
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(   #A built-in Django method that checks the provided credentials against the database.
            request=self.context.get('request'), 
            username = email,
            password = password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs
    
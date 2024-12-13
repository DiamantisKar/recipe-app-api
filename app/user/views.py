"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions #type: ignore
from rest_framework.authtoken.views import ObtainAuthToken #type: ignore
from user.serializers import UserSerializer,AuthTokenSerializer
from rest_framework.settings import api_settings #type: ignore


class CreateUserView(generics.CreateAPIView): #Handles request for db
    """Create a new user in the system."""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):  #Functionality for retrieving and updating get and patch-put
    """Manage the authenticated user."""
    serializer_class = UserSerializer 
    authentication_classes = [authentication.TokenAuthentication] #Setting auth classes
    permission_classes = [permissions.IsAuthenticated] #setting permission classes

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user #Http get request to this endpoint-calls get obj to get user -retrieve authenticated user- runs through serializer-returning result to api
    
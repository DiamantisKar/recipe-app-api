"""
Views for the recipe APIs.
"""

from rest_framework import viewsets #type:ignore
from rest_framework.authentication import TokenAuthentication #type:ignore
from rest_framework.permissions import IsAuthenticated #type:ignore

from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet): #Model viewset already provides CRUD ops
    """View for manage resipe APIs."""
    serializer_class = serializers.RecipeSerializer #serializer used
    queryset = Recipe.objects.all() #Specifying objects managable by api
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):   #Override for users to get only their own recipes.
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
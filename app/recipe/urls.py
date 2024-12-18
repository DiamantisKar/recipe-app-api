"""
URL mappings for recipe APP.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter #type:ignore

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet) #url prefix

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
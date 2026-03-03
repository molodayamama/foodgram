from django.shortcuts import get_object_or_404, redirect
from django.urls import path

from .models import Recipe


def short_link_redirect(request, code):
    recipe = get_object_or_404(Recipe, short_link=code)
    return redirect(f'/recipes/{recipe.id}/')


urlpatterns = [
    path('<str:code>/', short_link_redirect, name='short-link'),
]

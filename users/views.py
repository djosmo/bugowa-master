from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def logout_view(request):
    """Wylogowanie użytkownika."""
    logout(request)
    return HttpResponseRedirect(reverse('blog:post_list'))

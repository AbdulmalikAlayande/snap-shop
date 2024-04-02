from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from tags.models import Tag


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home_page.html'

class TagsPageView(ListView):
    model = Tag
    template_name = 'tags_page.html'
    context_object_name = 'Tags'

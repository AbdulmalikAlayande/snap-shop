from django.urls import path
from tags.views import TagsPageView

urlpatterns = [
    path('', TagsPageView.as_view(), name='tags_page')
]

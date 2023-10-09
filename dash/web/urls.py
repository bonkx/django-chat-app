from django.urls import path
from django.views.generic import TemplateView

from .views import encryption, home, user

urlpatterns = [
    path('', home.home, name="home"),
    path('encryption/', encryption.index, name="encryption"),
    path('ajax/search-user/', user.ajax_search_user, name="ajax_search_user"),
    # path('404/', TemplateView.as_view(template_name='404.html')),
    # path('500/', TemplateView.as_view(template_name='500.html')),
]

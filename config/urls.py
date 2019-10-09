from django.urls import path

from django_security_headers_example.core.views import LandingPageView


urlpatterns = [
    path("", view=LandingPageView.as_view(), name="landing_page"),
]

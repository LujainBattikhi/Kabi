from django.urls import path

from Kabi.apps.main.views import HomePageView

app_name = 'main'
urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
]
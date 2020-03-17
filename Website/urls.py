from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

from API import views as api_views
# Is Builder below required?
from Builder import views as builder_views
from Website.Auth import views as website_auth_views
from Dashboard import views as dash_view
from Users import views as enum_view

# Michael Old Reports
from Locations import views as location_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path("", website_auth_views.home_view, name="home"),

    # url('home/', include(("Home.urls", "Home"), namespace='Home')),
    url('tables/', include(("API.urls", "API"), namespace="API")),
    url(r'^API-token-auth/', obtain_auth_token, name='api_token_auth'),

    # API VIEWS: AUTH - Nadhirah
    path("users/", api_views.UserCreate.as_view(), name="user_create"),
    path("login/api", api_views.LoginView.as_view(), name="login_api"),
    url(r'^api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Auth - JingTing
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("login/", csrf_exempt(website_auth_views.login_view), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    url('questionnaires/', include(("Builder.urls", "Builder"), namespace="Builder")),
    url('dashboard/', include(("Dashboard.urls", "Dashboard"), namespace="Dashboard")),
    url('enumerators/', include(("Users.urls", "Enumerator"), namespace="Enumerator")), 
    url('reports/', include(("Reports.urls", "Reports"), namespace="Reports")),
    ]
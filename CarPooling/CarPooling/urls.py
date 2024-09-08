"""
URL configuration for CarPooling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .initcmds import *
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestione/' , include('gestione.urls')),
    re_path(r"^$|^\/$|^home\/$", home_page ,name="home"),  # Homepage
    path("register/", UserCreateView.as_view(), name="register"), # Register {templates/user_create.html}
    path("login/", auth_views.LoginView.as_view(), name="login"),   # Login (pre-built Django) {templates/registration/login.html}
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), # Logout (pre-built Django) {templates/registration/logged_out.html}
    path("registerDriver/" , createDriver , name="registerDriver" ),
    path('gestione/', include('gestione.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#delete_all_unlinked_imgs()
#generate_next_month_rides(15)
#init_db()
#erase_car_tables()

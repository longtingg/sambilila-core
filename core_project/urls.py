from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # The Django Admin panel inside the tenant schema
    path('admin/', admin.site.urls),
    
    # Route the root of the tenant domain directly to your custom login page
    path('', auth_views.LoginView.as_view(
        template_name='portal/login.html',
        redirect_authenticated_user=True
    ), name='tenant_login'),
    
    # Explicit login path if needed by internal middleware redirects
    path('login/', auth_views.LoginView.as_view(
        template_name='portal/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    # Logout path
    path('logout/', auth_views.LogoutView.as_view(next_page='tenant_login'), name='logout'),
]

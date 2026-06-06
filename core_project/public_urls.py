from django.contrib import admin
from django.urls import path
from .views import school_search_view

urlpatterns = [
    # Expose the admin panel on the public schema
    path('admin/', admin.site.urls),
    
    path('', school_search_view, name='home'),
    path('search/', school_search_view, name='school_search'),
]

from django.contrib import admin
from django.urls import path, include
from expense import views as expense_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', expense_views.home, name='home'),
    path('login/', users_views.login_view, name='login'),
    path('register/', users_views.register_view, name='register'),
    path('user/', include('users.urls')),
    path('expense/', include('expense.urls')),
]
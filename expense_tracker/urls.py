from django.contrib import admin
from django.urls import path, include
from expense import views as expense_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', expense_views.home, name='home'),
    path('expense/', include('expense.urls')),
]

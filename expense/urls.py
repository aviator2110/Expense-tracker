from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('<int:expense_id>/update/', views.update_expense, name='update_expense'),
    path('<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('<int:expense_id>/', views.expense_detail, name='expense_detail'),
]

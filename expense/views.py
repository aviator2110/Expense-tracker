from django.shortcuts import render

from expense.models import Expense


def home(request):
    expenses = Expense.objects.all()

    return render(request, 'expense/home.html', {'expenses': expenses})

def expense_detail(request, expense_id):
    expense = Expense.objects.get(pk=expense_id)

    return render(request, 'expense/expense_detail.html', {'expense': expense})
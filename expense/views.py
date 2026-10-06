from django.shortcuts import render
from django.db.models import Sum
from expense.models import Expense


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'expense/home.html')

    expenses = Expense.objects.filter(author=request.user)
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_count = expenses.count()

    context = {
        'expenses': expenses,
        'total_amount': total_amount,
        'total_count': total_count,
    }
    return render(request, 'expense/home.html', context)


def expense_detail(request, expense_id):
    if not request.user.is_authenticated:
        expense = None
    else:
        expense = Expense.objects.filter(pk=expense_id, author=request.user).first()
    return render(request, 'expense/expense_detail.html', {'expense': expense})
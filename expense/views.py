from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from expense.forms import ExpenseForm
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


def add_expense(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to record an expense.')
        return redirect('login')

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.author = request.user
            expense.save()
            messages.success(request, 'Expense recorded successfully.')
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'expense/add_expense.html', {'form': form})


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if expense.author != request.user:
        return HttpResponseForbidden('You are not authorized to delete this expense')

    if request.method == 'POST':
        expense.delete()
        messages.success(request,'Expense deleted successfully.')
        return redirect('home')
    return render(request, 'expense/delete_expense.html', {'expense': expense})


def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if expense.author != request.user:
        return HttpResponseForbidden('You are not authorized to update this expense')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request,'Expense updated successfully.')
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense/update_expense.html', {'form': form})
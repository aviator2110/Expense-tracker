from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from expense.forms import ExpenseForm
from django.db.models import Sum
from expense.models import Expense, Category, PaymentType


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'expense/home.html')

    expenses = Expense.objects.filter(author=request.user)

    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    payment_type_id = request.GET.get('payment_type', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    if q:
        expenses = expenses.filter(name__icontains=q)
    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if payment_type_id:
        expenses = expenses.filter(payment_type_id=payment_type_id)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    has_filters = bool(q or category_id or payment_type_id or start_date or end_date)

    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_count = expenses.count()

    categories = Category.objects.all()
    payment_types = PaymentType.objects.all()

    context = {
        'expenses': expenses,
        'total_amount': total_amount,
        'total_count': total_count,
        'categories': categories,
        'payment_types': payment_types,
        'q': q,
        'selected_category': category_id,
        'selected_payment_type': payment_type_id,
        'start_date': start_date,
        'end_date': end_date,
        'has_filters': has_filters,
    }
    return render(request, 'expense/home.html', context)


@login_required
def expense_detail(request, expense_id):
    if not request.user.is_authenticated:
        expense = None
    else:
        expense = Expense.objects.filter(pk=expense_id, author=request.user).first()
    return render(request, 'expense/expense_detail.html', {'expense': expense})


@login_required
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


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if expense.author != request.user:
        messages.error(request, 'You are not authorized to delete this expense.')
        return redirect('home')

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('home')
    return render(request, 'expense/delete_expense.html', {'expense': expense})


@login_required
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if expense.author != request.user:
        messages.error(request, 'You are not authorized to edit this expense.')
        return redirect('home')

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense/update_expense.html', {'form': form})
from django.utils import timezone
from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'payment_type', 'note', 'date']
        labels = {
            'name': 'Expense Name',
            'amount': 'Amount',
            'category': 'Category',
            'payment_type': 'Payment Type',
            'note': 'Note',
            'date': 'Date',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter expense name'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount','type': 'number','step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter note', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter date','type': 'date'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        name = (cleaned_data.get('name') or '').strip()
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')
        if len(name) < 3:
            self.add_error('name', 'Name must be at least 3 characters long')
        if amount is not None and amount <= 0:
            self.add_error('amount', 'Amount must be greater than 0')
        if date is not None and date > timezone.now().date():
            self.add_error('date', 'Date cannot be in the future')
        return cleaned_data
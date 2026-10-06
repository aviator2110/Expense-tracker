from expense.models import Category, Expense, PaymentType
from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'category', 'payment_type', 'date', 'note', 'author')
    list_filter = ('date', 'category', 'payment_type', 'author')
    search_fields = ('name', 'note', 'category__name', 'payment_type__name', 'author__username')
    date_hierarchy = 'date'
    ordering = ('-date',)
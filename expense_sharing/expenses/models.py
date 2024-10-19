from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    SPLIT_CHOICES = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENTAGE', 'Percentage'),
    ]

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_created')
    created_at = models.DateTimeField(auto_now_add=True)

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

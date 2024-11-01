from django.contrib.auth.models import AbstractUser
from django.db import models


class DebitModel(models.Model):

    LOAN_TYPE_CHOICES = [
        ('LENT', 'Lent'),
        ('BORROWED', 'Borrowed'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="loans")
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES)
    is_closed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_loan_type_display()} - {self.amount}"

    class Meta:
        verbose_name_plural = "Debits"
        verbose_name = "Debit"

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import transaction


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50) 
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        user = self.user
        if self.transaction_type == 'INCOME':
            user.current_balance =  user.current_balance - self.amount
        else:
            user.current_balance =  user.current_balance + self.amount
        
        user.save()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        is_new = self.pk is None 
        user = self.user
        if is_new:
           
            if self.transaction_type == 'INCOME':
                user.current_balance = user.current_balance + self.amount
            else:
                user.current_balance = user.current_balance - self.amount
            user.save()
        else:
            old_instance = Transaction.objects.get(pk=self.pk)
            if old_instance.transaction_type == 'INCOME':
                user.current_balance =  user.current_balance - old_instance.amount
            else:
                user.current_balance =  user.current_balance + old_instance.amount

            if self.transaction_type == 'INCOME':
                user.current_balance =  user.current_balance + self.amount
            else:
                user.current_balance =  user.current_balance - self.amount

        with transaction.atomic():
            user.save()
            super().save(*args, **kwargs)

        

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
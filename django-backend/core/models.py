from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.telegram_id)


class TokenBalance(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balance'
    )
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.telegram_id}: {self.balance}'


class TokenTransaction(models.Model):
    PURCHASE = 'purchase'
    GENERATION = 'generation'

    TYPE_CHOICES = [
        (PURCHASE, 'Purchase'),
        (GENERATION, 'Generation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
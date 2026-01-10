from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    callback_data = models.CharField(max_length=255, blank=True, null=True)
    callback_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.telegram_id)

    def set_callback_data(self, value, ttl_minutes=15):
        from django.utils import timezone
        self.callback_data = value
        self.callback_expires_at = timezone.now() + timezone.timedelta(minutes=ttl_minutes)
        self.save(update_fields=["callback_data", "callback_expires_at"])

    def get_callback_data(self):
        from django.utils import timezone
        if self.callback_expires_at and self.callback_expires_at < timezone.now():
            self.callback_data = None
            self.callback_expires_at = None
            self.save(update_fields=["callback_data", "callback_expires_at"])
            return None
        return self.callback_data


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
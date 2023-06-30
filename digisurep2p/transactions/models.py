from django.db import models

from digisurep2p.users.models import User


class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name="sent_transactions", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

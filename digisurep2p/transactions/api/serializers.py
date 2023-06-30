from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from digisurep2p.transactions.models import Transaction
from digisurep2p.users.models import User


class TransactionSerializer(serializers.ModelSerializer):
    recipient_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "sender", "recipient_email", "amount", "timestamp"]
        read_only_fields = ["id", "sender", "timestamp"]

    def validate(self, data):
        """
        Validate the transaction data
        """
        recipient_email = data.get("recipient_email")
        amount = data.get("amount")

        # Check if recipient exists
        try:
            User.objects.get(email=recipient_email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Recipient does not exist.")

        # Check if sender has enough balance
        sender = self.context["request"].user
        if sender.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")

        return data

    def create(self, validated_data):
        """
        Create the transaction
        """
        recipient_email = validated_data.pop("recipient_email")
        recipient = User.objects.get(email=recipient_email)
        sender = self.context["request"].user

        # Update users' balances
        sender.balance -= validated_data["amount"]
        recipient.balance += validated_data["amount"]
        sender.save()
        recipient.save()

        # Create transaction
        transaction = Transaction.objects.create(sender=sender, receiver=recipient, **validated_data)

        return transaction

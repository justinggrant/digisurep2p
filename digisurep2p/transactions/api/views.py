# Create your views here.
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from digisurep2p.base.views import BaseGenericViewSet
from digisurep2p.transactions.models import Transaction

from .serializers import TransactionSerializer


class TransactionViewSet(BaseGenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Send money to another user within the system by "
        + "providing the recipient's email and the amount to send.",
        summary="Send money to a user",
    )
    @action(methods=["post"], url_path="send", detail=False)
    def send_money(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid():
            # Create transaction
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Retrieve a list of transactions where the user is the sender or recipient.",
        summary="Get user transactions",
    )
    def list(self, request):
        # List all transactions where the user is the sender or recipient
        transactions = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        serializer = self.serializer_class(transactions, many=True)

        return Response(serializer.data)

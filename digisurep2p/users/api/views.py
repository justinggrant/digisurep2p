from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from digisurep2p.base.views import BaseGenericViewSet

from .serializers import DepositSerializer, LoginSerializer, RegisterSerializer

User = get_user_model()


class UserViewSet(BaseGenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_classes = {
        "register": RegisterSerializer,
        "login": LoginSerializer,
        "deposit": DepositSerializer,
    }

    @extend_schema(
        description="Register a new user by providing an email and password.",
        summary="Register a user",
    )
    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            data = serializer.data
            data["token"] = token.key
            return Response(data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        description="Log a user in by providing an email and password.",
        summary="Login a user",
    )
    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)

    @extend_schema(
        description="Get the current user's balance.",
        summary="Retrieve user balance",
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def balance(self, request):
        # This method returns the current balance for the user
        return Response({"balance": request.user.balance}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Deposit money into the current user's account by providing the amount to deposit.  "
        + "The amount must be an decimal greater than 0.",
        summary="Depost money into a user's account",
    )
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def deposit(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]

        request.user.balance += amount
        request.user.save()

        return Response({"balance": request.user.balance}, status=status.HTTP_200_OK)

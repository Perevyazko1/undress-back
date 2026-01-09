from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User, TokenBalance, TokenTransaction
from .serializers import CheckUserSerializer, CreateUserSerializer, TokenChangeSerializer


@api_view(['POST'])
def check_user(request):
    serializer = CheckUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    telegram_id = serializer.validated_data['telegram_id']

    user, created = User.objects.get_or_create(
        telegram_id=telegram_id
    )

    balance, _ = TokenBalance.objects.get_or_create(
        user=user,
        defaults={"balance": 0}
    )

    return Response({
        "created": created,
        "telegram_id": user.telegram_id,
        "tokens": balance.balance
    })



@api_view(['POST'])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    telegram_id = serializer.validated_data['telegram_id']

    user, created = User.objects.get_or_create(
        telegram_id=telegram_id
    )

    if created:
        TokenBalance.objects.create(user=user, balance=0)

    return Response({
        'created': created,
        'telegram_id': telegram_id,
        'tokens': user.balance.balance
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['POST'])
def add_tokens(request):
    serializer = TokenChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    telegram_id = serializer.validated_data['telegram_id']
    amount = serializer.validated_data['amount']

    try:
        user = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return Response(
            {'detail': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    balance = user.balance
    balance.balance += amount
    balance.save()

    TokenTransaction.objects.create(
        user=user,
        amount=amount,
        type=TokenTransaction.PURCHASE
    )

    return Response({
        'tokens': balance.balance
    })


@api_view(['POST'])
def spend_tokens(request):
    serializer = TokenChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    telegram_id = serializer.validated_data['telegram_id']
    amount = serializer.validated_data['amount']

    try:
        user = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return Response(
            {'detail': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    balance = user.balance

    if balance.balance < amount:
        return Response(
            {'detail': 'Not enough tokens'},
            status=status.HTTP_400_BAD_REQUEST
        )

    balance.balance -= amount
    balance.save()

    TokenTransaction.objects.create(
        user=user,
        amount=-amount,
        type=TokenTransaction.GENERATION
    )

    return Response({
        'tokens': balance.balance
    })

@api_view(['POST'])
def get_tokens(request):
    serializer = CheckUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    telegram_id = serializer.validated_data['telegram_id']

    try:
        user = User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return Response(
            {'detail': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    balance = user.balance

    return Response({
        'tokens': balance.balance
    })
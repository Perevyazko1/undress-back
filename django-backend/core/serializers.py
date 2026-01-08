from rest_framework import serializers


class CheckUserSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()


class CreateUserSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()


class TokenChangeSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)
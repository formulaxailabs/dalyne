from rest_framework import serializers
from core_module.models import TransactionsModel


class OrderSerializer(serializers.ModelSerializer):
    plan_id = serializers.IntegerField(
        required=True,
        allow_null=False
    )
    cost = serializers.IntegerField(
        required=True,
        allow_null=False
    )

    class Meta:
        model = TransactionsModel
        fields = ('plan_id', 'cost')


class OrderGetSerializer(serializers.ModelSerializer):
    plan_id = serializers.IntegerField(
        required=True,
        allow_null=False
    )

    class Meta:
        model = TransactionsModel
        fields = "__all__"


class CapturePaymentSerializer(serializers.Serializer):
    razorpay_payment_id = serializers.CharField(
        required=True,
        allow_null=True,
        allow_blank=True
    )
    razorpay_order_id = serializers.CharField(
        required=True,
        allow_null=True,
        allow_blank=True
    )
    razorpay_signature = serializers.CharField(
        required=True,
        allow_null=True,
        allow_blank=True
    )

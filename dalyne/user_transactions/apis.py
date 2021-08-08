from rest_framework import generics, permissions, response, status
from .serializers import OrderSerializer, OrderGetSerializer, CapturePaymentSerializer
from core_module.models import TransactionsModel, Plans
import razorpay
from django.conf import settings


def get_razorpay_client():
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
    return client


class TransactionAPI(generics.CreateAPIView):
    serializer_class = OrderSerializer
    model = TransactionsModel
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        client = get_razorpay_client()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            amount = serializer.validated_data['cost']
            plan = Plans.objects.filter(id=serializer.validated_data['plan_id']).first()
            order = client.order.create(
                {
                    "amount": int(amount) * 100,
                    "currency": "INR",
                    "payment_capture": "1"
                }
            )
            obj = self.model.objects.create(
                plan=plan,
                order_id=order['id'],
                cost=amount
            )
            order_serializer = OrderGetSerializer(obj)
            response_dict = dict()
            response_dict['payment'] = order
            response_dict["order_data"] = order_serializer.data
            return response.Response(
                response_dict,
                status=status.HTTP_200_OK
            )
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CapturePaymentAPI(generics.CreateAPIView):
    serializer_class = CapturePaymentSerializer
    model = TransactionsModel
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        client = get_razorpay_client()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = TransactionsModel.objects.get(id=serializer.validated_data['razorpay_order_id'])
            amount = order.cost * 100
            data = dict(serializer.validated_data)
            check = client.utility.verify_payment_signature(data)
            if check is not None:
                return response.Response(
                    {
                        'error': 'Oops!! Payment cannot be processed at this moment.Please try again.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                payment_id = serializer.validated_data['razorpay_payment_id']
                client.payment.capture(payment_id, amount)
                order.is_transaction_successful = True
                order.save()

                return response.Response(
                    {'msg': 'Payment successfully received'},
                    status=status.HTTP_200_OK
                )
            except:
                return response.Response(
                    {
                        'error': 'Oops!! Payment cannot be processed at this moment.Please try again.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

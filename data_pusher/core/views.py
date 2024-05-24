from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account, Destination, Webhook
from .serializers import AccountSerializer, DestinationSerializer, WebhookSerializer
import requests


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return self.queryset.filter(account__account_id=account_id)
        return self.queryset


class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return self.queryset.filter(account__account_id=account_id)
        return self.queryset


@api_view(['POST'])
def incoming_data(request):
    secret_token = request.headers.get('CL-X-TOKEN')
    if not secret_token:
        return Response({'error': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        account = Account.objects.get(app_secret_token=secret_token)
    except Account.DoesNotExist:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data

    # Trigger webhooks for the event 'data_received'
    webhooks = Webhook.objects.filter(account=account, event='data_received', enabled=True)
    for webhook in webhooks:
        destination = webhook.destination
        headers = destination.headers
        url = destination.url
        method = destination.http_method

        if method == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)

        if response.status_code != 200:
            return Response({'error': 'Failed to send data to destination'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Data sent successfully'}, status=status.HTTP_200_OK)

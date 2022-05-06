from rest_framework import views
from rest_framework.response import Response

from ..payments.sisow.service import get_ideal_banks
from .serializers import iDealBankSerializer


class IdealBanksView(views.APIView):
    def get(self, request):
        serializer = iDealBankSerializer(instance=get_ideal_banks(), many=True)
        return Response(serializer.data)

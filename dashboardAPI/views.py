from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from .models import Purchases, Companies, Participants
from .serializers import PurchasesSerializer, CompaniesSerializer


def save_models(request):
    qs = Purchases.objects.all()
    for obj in qs:
        obj.save()


class CompaniesList(APIView):
    def get(self, request):
        companies = Companies.objects.all()[:1000]    
        serializer = CompaniesSerializer(companies, many=True)
        return Response(serializer.data)


class CompaniesDetail(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        companies = Companies.objects.filter(id__in=id)
        serializer = CompaniesSerializer(companies, many=True)
        return Response(serializer.data)


class WinrateCompany(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        inn = Companies.objects.get(id=id).supplier_inn
        orders = Participants.objects.filter(supplier_inn=inn)
        count_orders = len(orders)
        win = 0
        for res in orders:
            res = res.is_winner
            if res == 'Да':
                win += 1
        return Response({'winrate': win/count_orders, 'count_orders': count_orders})


# class Regions(APIView):
#     def post(self. request):
#         id 
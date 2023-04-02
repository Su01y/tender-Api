from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from .models import Purchases, Companies
from .serializers import PurchasesSerializer, CompaniesSerializer


def save_models(request):
    qs = Purchases.objects.all()
    for obj in qs:
        obj.save()


class CompaniesList(APIView):
    def get(self, request):
        companies = Companies.objects.all()
        serializer = CompaniesSerializer(companies, many=True)
        return Response(serializer.data)


class CompaniesDetail(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        companies = Companies.objects.filter(id__in=id)
        serializer = CompaniesSerializer(companies, many=True)
        return Response(serializer.data)
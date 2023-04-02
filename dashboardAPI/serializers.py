from rest_framework import serializers

from .models import Purchases, Companies


class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies 
        fields = '__all__'


# class OrdersSerializer(serializers):
#     data = serializers.DateField()
#     name = serializers.CharField()
#     res = serializers.BooleanField()
#     cat = serializers.CharField()

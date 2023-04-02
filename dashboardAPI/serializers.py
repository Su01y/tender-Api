from rest_framework import serializers

from .models import Purchases, Companies, Participants, Contracts


class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies 
        fields = '__all__'


# class AspirantEducation(serializers.ModelSerializer):
#     class Meta:
#         model = Aspirant
#         fields = ('name', 'education')
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Purchases, Companies, Participants
from .serializers import CompaniesSerializer
from .category import categorize


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
        companies = Companies.objects.filter(id=id)
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
        return Response({'winrate': int(win / count_orders), 'count_orders': count_orders})


class Regions(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        inn = Companies.objects.get(id=id).supplier_inn
        orders = Participants.objects.filter(supplier_inn=inn)
        regions = dict()
        for order in orders:
            if order.is_winner == 'Да':
                purch_id = order.purch_id
                region = Purchases.objects.get(purch_id=purch_id).delivery_region
                if region in regions:
                    regions[region] += 1
                else:
                    regions[region] = 0
        return Response(regions)


class DatePrice(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        inn = Companies.objects.get(id=id).supplier_inn
        orders = Participants.objects.filter(supplier_inn=inn)
        months = dict()
        for order in orders:
            if order.is_winner == 'Да':
                purch_id = order.purch_id
                month = Purchases.objects.get(purch_id=purch_id).publish_date.month
                price = Purchases.objects.get(purch_id=purch_id).price
                if month in months:
                    months[month] += price
                else:
                    months[month] = price
        return Response(months)


class Category(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        inn = Companies.objects.get(id=id).supplier_inn
        orders = Participants.objects.filter(supplier_inn=inn)
        categories = dict()
        for order in orders:
            if order.is_winner == 'Да':
                purch_id = order.purch_id
                cat = Purchases.objects.get(purch_id=purch_id).lot_name
                if cat:
                    cat = categorize(cat)
                    price = Purchases.objects.get(purch_id=purch_id).price
                    if cat in categories:
                        categories[cat] += price
                    else:
                        categories[cat] = price
        return Response(categories)
    

# class Orders(APIView):
#     def post(self, request):
#         id = request.data.get('id', ())
#         inn = Companies.objects.get(id=id).supplier_inn
#         orders = Participants.objects.filter(supplier_inn=inn)
#         for order in orders:
#             if order.is_winner == 'Да':
#                 purch_id = order.purch_id
                
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
            if res.is_winner == 'Да':
                win += 1
        return Response({'winrate': int(win / count_orders * 100), 'count_orders': count_orders})


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
        years = dict()
        for order in orders:
            if order.is_winner == 'Да':
                purch_id = order.purch_id
                year = Purchases.objects.get(purch_id=purch_id).publish_date.year
                price = Purchases.objects.get(purch_id=purch_id).price
                if year in years:
                    years[year] += price
                else:
                    years[year] = price

        dict_list = []

        for key, value in years.items():
            new_dict = {}
            new_dict["year"] = key
            new_dict["moneyIncome"] = str(int(value))
            dict_list.append(new_dict)
        return Response(dict_list)


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
                print(cat)
                if cat:
                    cat = categorize(cat)
                    price = Purchases.objects.get(purch_id=purch_id).price
                    if cat in categories:
                        categories[cat] += price
                    else:
                        categories[cat] = price
        dict_list = []

        for key, value in categories.items():
            new_dict = {}
            new_dict["category"] = key.title()
            new_dict["moneyIncome"] = str(int(value))
            dict_list.append(new_dict)
        return Response(dict_list)
    

# class Orders(APIView):
#     def post(self, request):
#         id = request.data.get('id', ())
#         inn = Companies.objects.get(id=id).supplier_inn
#         orders = Participants.objects.filter(supplier_inn=inn)
#         for order in orders:
#             if order.is_winner == 'Да':
#                 purch_id = order.purch_id
                
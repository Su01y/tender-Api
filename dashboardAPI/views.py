from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Contracts, Purchases, Companies, Participants
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


class AllContracts(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        inn = Companies.objects.get(id=id).supplier_inn
        orders = Participants.objects.filter(supplier_inn=inn)
        results = []
        for order in orders:
            if order.is_winner == 'Да':
                frame = dict()
                purch_id = order.purch_id
                try:
                    date = Contracts.objects.get(purch_id=purch_id).contract_conclusion_date
                    price = Contracts.objects.get(purch_id=purch_id).price
                    frame['id'] = purch_id
                    frame['data'] = date
                    frame['price'] = price
                    results.append(frame)
                finally:
                    continue
        return Response(results)


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


class RadarChart(APIView):
    def post(self, request):
        id = request.data.get('id', ())
        inn = Companies.objects.get(id=id).supplier_inn
        orders = Participants.objects.filter(supplier_inn=inn)

        y2022 = dict({
            'year': 2022,
            'orders': 0,
            'price': 0,
            'count': 0,
            'win': 0,
            'region': []
        })
        y2021 = dict({
            'year': 2021,
            'orders': 0,
            'price': 0,
            'count': 0,
            'win': 0,
            'region': []
        })
        for order in orders:
            purch_id = order.purch_id
            if Purchases.objects.get(purch_id=purch_id).publish_date.year == 2022:            
                y2022['orders'] += 1

            if Purchases.objects.get(purch_id=purch_id).publish_date.year == 2021:
                y2021['orders'] += 1

            if order.is_winner == 'Да':
                purch_id = order.purch_id
                try:
                    contract = Contracts.objects.get(purch_id=purch_id)
                    year = contract.contract_conclusion_date.year
                    region = Purchases.objects.get(purch_id=purch_id).delivery_region
                    if year == 2022:
                        y2022['price'] += contract.price
                        y2022['count'] += 1
                        if region not in y2022['region']:
                            y2022['region'].append(region)
                        y2022['win'] += 1
                    
                    if year == 2021:
                        y2021['price'] += contract.price
                        y2021['count'] += 1
                        if region not in y2021['region']:
                            y2021['region'].append(region)
                        y2021['win'] += 1
                finally:
                    continue

        y2022['region'] = len(y2022['region'])
        y2021['region'] = len(y2021['region'])
        y2022['win'] = int(y2022['count'] / y2022['orders'] * 100) / 100
        y2021['win'] = int(y2021['count'] / y2021['orders'] * 100) / 100

        y2022['price'] = round(y2022['price'] / (y2022['price'] + y2021['price']), 4)
        y2021['price'] = round(y2021['price'] / (y2022['price'] + y2021['price']), 4)

        y2022['count'] = round(y2022['count'] / (y2022['count'] + y2021['count']), 4)
        y2021['count'] = round(y2021['count'] / (y2022['count'] + y2021['count']), 4)

        y2022['orders'] = round(y2022['orders'] / (y2022['orders'] + y2021['orders']), 4)
        y2021['orders'] = round(y2021['orders'] / (y2022['orders'] + y2021['orders']), 4)

        y2022['region'] = round(y2022['region'] / (y2022['region'] + y2021['region']), 4)
        y2021['region'] = round(y2021['region'] / (y2022['region'] + y2021['region']), 4)
        
        data = [y2022, y2021]
        result = []

        region_dict = {"param": "region"}    
        for region in set(d['region'] for d in data):
            for d in data:
                if d['region'] == region:
                    region_dict[str(d['year'])] = d['region']
        result.append(region_dict)

        tastes = ["price", "orders", "count", "win"]
        for taste in tastes:
            taste_dict = {"param": taste}
            for d in data:
                taste_dict[str(d['year'])] = d[taste]
            result.append(taste_dict)

        return Response(result)
from django.urls import path
from .views import save_models, CompaniesList, CompaniesDetail, WinrateCompany, Regions, DatePrice, Category, AllContracts


urlpatterns = [
    path('api/', save_models),
    path('api/companies/', CompaniesList.as_view()),
    path('api/get-company/', CompaniesDetail.as_view()),
    path('api/get-winrate/', WinrateCompany.as_view()),
    path('api/get-regions/', Regions.as_view()),
    path('api/date-price/', DatePrice.as_view()),
    path('api/category/', Category.as_view()),
    path('api/contracts/', AllContracts.as_view()),
]

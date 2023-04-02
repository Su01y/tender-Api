from django.urls import path
from .views import save_models, CompaniesList, CompaniesDetail, WinrateCompany


urlpatterns = [
    path('api/', save_models),
    path('api/companies/', CompaniesList.as_view()),
    path('api/get-company/', CompaniesDetail.as_view()),
    path('api/get-winrate/', WinrateCompany.as_view()),
]

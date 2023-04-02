from django.urls import path
from .views import save_models, CompaniesList, CompaniesDetail


urlpatterns = [
    path('api/', save_models),
    path('api/companies/', CompaniesList.as_view()),
    path('api/get_company/', CompaniesDetail.as_view())
]

from django.urls import path
from .views import HomeRSVPView, ListaPresentesView, DashboardView, exportar_pdf_convidados

urlpatterns = [
    path('', HomeRSVPView.as_view(), name='home'),
    path('presentes/', ListaPresentesView.as_view(), name='lista_presentes'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/pdf/', exportar_pdf_convidados, name='exportar_pdf'),
]
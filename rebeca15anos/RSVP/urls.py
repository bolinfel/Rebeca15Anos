from django.urls import path
from .views import HomeRSVPView, ListaPresentesView

urlpatterns = [
    path('', HomeRSVPView.as_view(), name='home'),
    path('presentes/', ListaPresentesView.as_view(), name='lista_presentes'),
    # Remova ou comente a linha da ConfirmacaoSucessoView
]
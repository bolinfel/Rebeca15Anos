from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Convidado, Presente
from .forms import RSVPForm

class HomeRSVPView(SuccessMessageMixin, CreateView):
    """View principal que exibe as informações e processa o RSVP."""
    model = Convidado
    form_class = RSVPForm
    template_name = 'RSVP/home.html'
    success_url = reverse_lazy('home')
    success_message = "Sua confirmação foi enviada com sucesso! Mal podemos esperar pela festa."

    def get_context_data(self, **kwargs):
        """Injeta dados adicionais como a lista de presentes (opcional) ou prazos."""
        context = super().get_context_data(**kwargs)
        # Exemplo: passar a data limite para o template
        context['data_limite'] = "25 de Março de 2026"
        return context

class ListaPresentesView(ListView):
    """View para exibição dos presentes disponíveis."""
    model = Presente
    template_name = 'RSVP/lista_presentes.html'
    context_object_name = 'presentes'

    def get_queryset(self):
        # Garante que convidados não vejam presentes já reservados
        return Presente.objects.filter(esta_reservado=False)
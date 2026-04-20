from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Convidado, Presente, Acompanhante
from .forms import RSVPForm
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class HomeRSVPView(SuccessMessageMixin, CreateView):
    model = Convidado
    form_class = RSVPForm
    template_name = 'RSVP/home.html'
    success_url = reverse_lazy('home')
    success_message = "Confirmação realizada com sucesso!"

    def form_valid(self, form):
        # Usamos transaction.atomic para garantir que se um acompanhante falhar, nada seja salvo
        with transaction.atomic():
            # Salva o convidado principal
            self.object = form.save()
            
            # Pega a quantidade de acompanhantes enviada
            qtd = int(self.request.POST.get('qtd_acompanhantes', 0))
            
            from .models import Acompanhante
            for i in range(1, qtd + 1):
                p_nome = self.request.POST.get(f'acomp_primeiro_{i}')
                u_nome = self.request.POST.get(f'acomp_ultimo_{i}')
                idade_acomp = self.request.POST.get(f'acomp_idade_{i}') # Novo
                
                if p_nome and u_nome:
                    Acompanhante.objects.create(
                        convidado_principal=self.object,
                        primeiro_nome=p_nome,
                        ultimo_nome=u_nome,
                        idade=idade_acomp if idade_acomp else None
                    )
            
            return super().form_valid(form)

class ListaPresentesView(ListView):
    model = Presente
    template_name = 'RSVP/lista_presentes.html'
    context_object_name = 'presentes'

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Lógica de reserva para convidados (já existente)
            if 'btn_reservar' in request.POST:
                presente = get_object_or_404(Presente, id=request.POST.get('presente_id'))
                presente.reservado_por_nome = f"{request.POST.get('primeiro_nome')} {request.POST.get('ultimo_nome')}"
                presente.esta_reservado = True
                presente.save()
            return redirect('lista_presentes')

        # Lógica exclusiva para ADMIN (Aniversariante)
        if 'btn_cadastrar' in request.POST:
            Presente.objects.create(
                nome=request.POST.get('nome'),
                descricao=request.POST.get('descricao'),
                imagem_url=request.POST.get('imagem_url'),
                link_compra=request.POST.get('link_compra')
            )
        
        elif 'btn_editar' in request.POST:
            presente = get_object_or_404(Presente, id=request.POST.get('presente_id'))
            presente.nome = request.POST.get('nome')
            presente.descricao = request.POST.get('descricao')
            presente.imagem_url = request.POST.get('imagem_url')
            presente.link_compra = request.POST.get('link_compra')
            # Opcional: resetar reserva se o admin desejar
            if request.POST.get('limpar_reserva') == 'on':
                presente.esta_reservado = False
                presente.reservado_por_nome = ""
            presente.save()

        elif 'btn_excluir' in request.POST:
            presente = get_object_or_404(Presente, id=request.POST.get('presente_id'))
            presente.delete()

        return redirect('lista_presentes')

# Mixin para garantir que apenas a aniversariante (admin) acesse
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'RSVP/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        convidados = Convidado.objects.all().prefetch_related('acompanhantes')
        
        context['convidados'] = convidados
        context['total_convidados'] = convidados.count()
        context['total_acompanhantes'] = Acompanhante.objects.count()
        context['total_geral'] = context['total_convidados'] + context['total_acompanhantes']
        return context

def exportar_pdf_convidados(request):
    if not request.user.is_staff:
        return HttpResponse("Acesso negado", status=403)

    convidados = Convidado.objects.all().prefetch_related('acompanhantes')
    template_path = 'RSVP/pdf_template.html'
    context = {'convidados': convidados}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_convidados_rebeca.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       return HttpResponse('Erro ao gerar PDF', status=500)
    return response
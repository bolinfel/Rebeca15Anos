from django import forms
from .models import Convidado

class RSVPForm(forms.ModelForm):
    qtd_acompanhantes = forms.IntegerField(
        label="Quantos acompanhantes?", 
        min_value=0, 
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'id': 'id_qtd_acompanhantes'})
    )

    class Meta:
        model = Convidado
        fields = ['primeiro_nome', 'ultimo_nome', 'email', 'telefone', 'idade', 'comentarios']
        widgets = {
            'primeiro_nome': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Primeiro Nome'}),
            'ultimo_nome': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Último Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'seu@email.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': '(00) 00000-0000', 'type': 'tel'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Sua idade'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control rounded-4', 'rows': 2, 'placeholder': 'Alguma mensagem?'}),
        }
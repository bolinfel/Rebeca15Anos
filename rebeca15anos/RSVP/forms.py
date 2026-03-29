from django import forms
from .models import Convidado

class RSVPForm(forms.ModelForm):
    class Meta:
        model = Convidado
        fields = ['nome_completo', 'email', 'telefone', 'status', 'acompanhantes']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Nome Completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'seu@email.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': '(00) 00000-0000'}),
            'status': forms.Select(attrs={'class': 'form-select rounded-pill'}),
            'acompanhantes': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'min': '0'}),
        }
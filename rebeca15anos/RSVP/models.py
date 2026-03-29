from django.db import models
from django.core.validators import MinValueValidator

class Evento(models.Model):
    """Armazena os detalhes do aniversário centralizados."""
    titulo = models.CharField(max_length=100, default="Meu Aniversário")
    data_evento = models.DateTimeField()
    local = models.TextField()
    limite_confirmacao = models.DateField(help_text="Data máxima para confirmar presença")

    def __str__(self):
        return self.titulo

class Convidado(models.Model):
    """Dados de quem vai (ou não) à festa."""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('NAO_VAI', 'Não poderei ir'),
    ]

    nome_completo = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE')
    acompanhantes = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    data_resposta = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_completo} ({self.get_status_display()})"

class Presente(models.Model):
    """Itens da lista de desejos."""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    link_referencia = models.URLField(blank=True, null=True, help_text="Link de exemplo em alguma loja")
    
    # Lógica de Reserva
    esta_reservado = models.BooleanField(default=False)
    reservado_por = models.ForeignKey(
        Convidado, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="presentes_escolhidos"
    )

    class Meta:
        ordering = ['nome']

    def __str__(self):
        status = " (Reservado)" if self.esta_reservado else " (Disponível)"
        return f"{self.nome}{status}"
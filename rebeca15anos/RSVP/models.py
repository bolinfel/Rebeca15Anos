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
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    idade = models.PositiveIntegerField(null=True, blank=True) # Novo campo
    status = models.CharField(max_length=15, default='CONFIRMADO')
    comentarios = models.TextField(blank=True, null=True)
    data_resposta = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"

class Presente(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    imagem_url = models.URLField(blank=True, null=True, help_text="Link de uma imagem do presente")
    link_compra = models.URLField(blank=True, null=True)
    esta_reservado = models.BooleanField(default=False)
    # Quem reservou (pode ser diferente do nome na lista de convidados)
    reservado_por_nome = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Acompanhante(models.Model):
    convidado_principal = models.ForeignKey(Convidado, on_delete=models.CASCADE, related_name='acompanhantes')
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    idade = models.PositiveIntegerField(null=True, blank=True) # Novo campo

    def __str__(self):
        return f"{self.primeiro_nome} (Acomp. de {self.convidado_principal.primeiro_nome})"
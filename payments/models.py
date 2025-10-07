from django.db import models
from django.utils import timezone

class Plan(models.Model):
    """Planos/Modalidades"""
    PLAN_TYPE_CHOICES = (
        ('monthly', 'Mensal'),
        ('quarterly', 'Trimestral'),
        ('semiannual', 'Semestral'),
        ('annual', 'Anual'),
    )
    
    name = models.CharField(max_length=100, verbose_name='Nome do Plano')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Descrição')
    
    # Valores
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES, verbose_name='Tipo de Plano')
    
    # Benefícios
    benefits = models.JSONField(default=list, help_text='Lista de benefícios', verbose_name='Benefícios')
    classes_per_week = models.IntegerField(null=True, blank=True, verbose_name='Aulas por Semana')
    has_video_access = models.BooleanField(default=True, verbose_name='Acesso a Vídeos?')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Ativo?')
    order = models.IntegerField(default=0, verbose_name='Ordem')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['order', 'price']
    
    def __str__(self):
        return f"{self.name} - {self.get_plan_type_display()}"


class Payment(models.Model):
    """Registro de Pagamentos"""
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    )
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='payments', verbose_name='Aluna')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, verbose_name='Plano')
    
    # Valores
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    due_date = models.DateField(verbose_name='Data de Vencimento')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Data de Pagamento')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    
    # Integração Mercado Pago
    mercadopago_payment_id = models.CharField(max_length=100, blank=True, verbose_name='ID Mercado Pago')
    mercadopago_status = models.CharField(max_length=50, blank=True, verbose_name='Status Mercado Pago')
    mercadopago_response = models.JSONField(null=True, blank=True, verbose_name='Resposta Mercado Pago')
    
    # Metadados
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='Método de Pagamento')
    reference_code = models.CharField(max_length=100, blank=True, verbose_name='Código de Referência')
    notes = models.TextField(blank=True, verbose_name='Observações')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.student} - R$ {self.amount} - {self.get_status_display()}"


class Subscription(models.Model):
    """Assinaturas recorrentes"""
    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='subscription', verbose_name='Aluna')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, verbose_name='Plano')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Ativa?')
    start_date = models.DateField(default=timezone.now, verbose_name='Data de Início')
    end_date = models.DateField(null=True, blank=True, verbose_name='Data de Término')
    
    # Mercado Pago
    mercadopago_subscription_id = models.CharField(max_length=100, blank=True, verbose_name='ID Assinatura MP')
    
    # Controle
    auto_renewal = models.BooleanField(default=True, verbose_name='Renovação Automática?')
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name='Cancelada em')
    cancellation_reason = models.TextField(blank=True, verbose_name='Motivo do Cancelamento')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
    
    def __str__(self):
        return f"{self.student} - {self.plan}"
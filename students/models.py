from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    """Perfil completo do aluno"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    
    # Dados pessoais
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    rg = models.CharField(max_length=20, blank=True, verbose_name='RG')
    address = models.CharField(max_length=200, blank=True, verbose_name='Endereço')
    city = models.CharField(max_length=100, blank=True, verbose_name='Cidade')
    state = models.CharField(max_length=2, blank=True, verbose_name='Estado')
    zip_code = models.CharField(max_length=10, blank=True, verbose_name='CEP')
    
    # Contatos de emergência
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name='Contato de Emergência')
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Telefone de Emergência')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    enrollment_date = models.DateField(default=timezone.now, verbose_name='Data de Matrícula')
    
    # Modalidade
    modality = models.ForeignKey('payments.Plan', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Plano')
    
    class Meta:
        verbose_name = 'Aluna'
        verbose_name_plural = 'Alunas'
        ordering = ['user__first_name']
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Anamnesis(models.Model):
    """Ficha de Anamnese"""
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='anamnesis')
    
    # Objetivos
    main_goal = models.TextField(verbose_name='Objetivo Principal')
    secondary_goals = models.TextField(blank=True, verbose_name='Objetivos Secundários')
    
    # Histórico de saúde
    has_health_issues = models.BooleanField(default=False, verbose_name='Possui problemas de saúde?')
    health_issues_description = models.TextField(blank=True, verbose_name='Descrição dos problemas')
    
    has_injuries = models.BooleanField(default=False, verbose_name='Possui lesões?')
    injuries_description = models.TextField(blank=True, verbose_name='Descrição das lesões')
    
    has_surgeries = models.BooleanField(default=False, verbose_name='Já fez cirurgias?')
    surgeries_description = models.TextField(blank=True, verbose_name='Descrição das cirurgias')
    
    # Medicamentos
    takes_medication = models.BooleanField(default=False, verbose_name='Toma medicamentos?')
    medication_list = models.TextField(blank=True, verbose_name='Lista de medicamentos')
    
    # Atividade física
    ACTIVITY_LEVEL_CHOICES = (
        ('sedentary', 'Sedentário'),
        ('light', 'Atividade Leve'),
        ('moderate', 'Atividade Moderada'),
        ('intense', 'Atividade Intensa'),
        ('athlete', 'Atleta'),
    )
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, default='sedentary', verbose_name='Nível de Atividade')
    previous_exercises = models.TextField(blank=True, verbose_name='Atividades físicas anteriores')
    
    # Hábitos
    smoker = models.BooleanField(default=False, verbose_name='Fumante?')
    alcohol_consumption = models.CharField(max_length=50, blank=True, verbose_name='Consumo de álcool')
    sleep_hours = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(24)], verbose_name='Horas de Sono')
    
    # Observações
    observations = models.TextField(blank=True, verbose_name='Observações Gerais')
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ficha de Anamnese'
        verbose_name_plural = 'Fichas de Anamnese'
    
    def __str__(self):
        return f"Anamnese - {self.student.user.get_full_name()}"


class MenstrualCycle(models.Model):
    """Controle de Ciclo Menstrual"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='menstrual_cycles')
    
    cycle_start_date = models.DateField(verbose_name='Data de início do ciclo')
    cycle_duration = models.IntegerField(default=28, validators=[MinValueValidator(1), MaxValueValidator(60)], verbose_name='Duração do Ciclo')
    has_symptoms = models.BooleanField(default=False, verbose_name='Apresenta sintomas?')
    symptoms_description = models.TextField(blank=True, verbose_name='Descrição dos sintomas')
    
    # Intensidade dos sintomas
    INTENSITY_CHOICES = (
        ('light', 'Leve'),
        ('moderate', 'Moderado'),
        ('intense', 'Intenso'),
    )
    symptoms_intensity = models.CharField(max_length=20, choices=INTENSITY_CHOICES, blank=True, verbose_name='Intensidade dos Sintomas')
    
    observations = models.TextField(blank=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Ciclo Menstrual'
        verbose_name_plural = 'Ciclos Menstruais'
        ordering = ['-cycle_start_date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.cycle_start_date}"


class Measurement(models.Model):
    """Medidas e Avaliação Física"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='measurements')
    
    # Data da medição
    measurement_date = models.DateField(default=timezone.now, verbose_name='Data da Medição')
    
    # Peso e altura
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso (kg)')
    height = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Altura (m)')
    
    # Circunferências (em cm)
    neck = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Pescoço (cm)')
    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Peitoral (cm)')
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Cintura (cm)')
    abdomen = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Abdômen (cm)')
    hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Quadril (cm)')
    right_arm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Braço Direito (cm)')
    left_arm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Braço Esquerdo (cm)')
    right_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Coxa Direita (cm)')
    left_thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Coxa Esquerda (cm)')
    right_calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Panturrilha Direita (cm)')
    left_calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Panturrilha Esquerda (cm)')
    
    # Composição corporal
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='% Gordura')
    muscle_mass_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='% Massa Muscular')
    
    # IMC (calculado automaticamente)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='IMC')
    
    # Observações
    observations = models.TextField(blank=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'
        ordering = ['-measurement_date']
    
    def save(self, *args, **kwargs):
        # Calcular IMC automaticamente
        if self.weight and self.height:
            self.bmi = self.weight / (self.height ** 2)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.measurement_date}"
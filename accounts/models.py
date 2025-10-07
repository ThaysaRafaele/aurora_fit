from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Usuário customizado - base para reutilização"""
    USER_TYPE_CHOICES = (
        ('student', 'Aluno'),
        ('instructor', 'Professor'),
        ('admin', 'Administrador'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student', verbose_name='Tipo de Usuário')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name='Foto de Perfil')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"
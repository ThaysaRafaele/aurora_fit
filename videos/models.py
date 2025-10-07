from django.db import models
from django.conf import settings

class VideoCategory(models.Model):
    """Categorias de vídeos"""
    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name='Descrição')
    icon = models.CharField(max_length=50, blank=True, help_text='Nome do ícone (ex: FontAwesome)')
    order = models.IntegerField(default=0, verbose_name='Ordem')
    
    class Meta:
        verbose_name = 'Categoria de Vídeo'
        verbose_name_plural = 'Categorias de Vídeos'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Video(models.Model):
    """Vídeos de aulas gravadas"""
    VIDEO_TYPE_CHOICES = (
        ('recorded', 'Gravado'),
        ('live_archived', 'Live Arquivada'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Descrição')
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, related_name='videos', verbose_name='Categoria')
    
    # Arquivo ou URL
    video_file = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name='Arquivo de Vídeo')
    video_url = models.URLField(blank=True, help_text='URL do YouTube, Vimeo, etc.', verbose_name='URL do Vídeo')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True, verbose_name='Miniatura')
    
    # Informações
    duration = models.DurationField(null=True, blank=True, verbose_name='Duração')
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPE_CHOICES, default='recorded', verbose_name='Tipo')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Instrutora')
    
    # Controle de acesso
    is_public = models.BooleanField(default=False, verbose_name='Público?')
    requires_subscription = models.BooleanField(default=True, verbose_name='Requer assinatura?')
    
    # Metadados
    views_count = models.IntegerField(default=0, verbose_name='Visualizações')
    likes_count = models.IntegerField(default=0, verbose_name='Curtidas')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Publicado em')
    
    class Meta:
        verbose_name = 'Vídeo'
        verbose_name_plural = 'Vídeos'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title


class LiveClass(models.Model):
    """Aulas ao vivo (transmissões)"""
    STATUS_CHOICES = (
        ('scheduled', 'Agendada'),
        ('live', 'Ao Vivo'),
        ('finished', 'Finalizada'),
        ('cancelled', 'Cancelada'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Instrutora')
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    
    # Agendamento
    scheduled_date = models.DateTimeField(verbose_name='Data e Hora')
    duration_minutes = models.IntegerField(default=60, verbose_name='Duração (minutos)')
    
    # Transmissão
    stream_url = models.URLField(blank=True, help_text='URL da transmissão (YouTube Live, etc.)', verbose_name='URL da Transmissão')
    chat_enabled = models.BooleanField(default=True, verbose_name='Chat Habilitado?')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Status')
    
    # Arquivo após transmissão
    archived_video = models.OneToOneField(Video, on_delete=models.SET_NULL, null=True, blank=True, related_name='live_source', verbose_name='Vídeo Arquivado')
    
    # Metadados
    max_participants = models.IntegerField(null=True, blank=True, verbose_name='Máximo de Participantes')
    registered_participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered_lives', blank=True, verbose_name='Participantes Registrados')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Aula ao Vivo'
        verbose_name_plural = 'Aulas ao Vivo'
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_date.strftime('%d/%m/%Y %H:%M')}"
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Clients(models.Model):
    email = models.EmailField(verbose_name='email', unique=True)
    fullname = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f"{self.fullname} ({self.email})"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Messages(models.Model):
    subject = models.CharField(verbose_name='Тема')
    content = models.TextField(verbose_name='Содержание')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class MailingSettings(models.Model):
    start_date = models.DateTimeField(verbose_name='Начало рассылки')
    end_date = models.DateTimeField(verbose_name='Окончание рассылки')
    period_choices = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    periodicity = models.CharField(max_length=10, choices=period_choices, verbose_name='Периодичность')
    status_choices = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='created', verbose_name='Статус')
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Clients, verbose_name='Клиенты')

    def __str__(self):
        return f"Рассылка №{self.pk} сообщения {self.message}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingLogs(models.Model):
    date_time = models.DateTimeField(verbose_name='Дата и время')
    status = models.CharField(verbose_name='Статус попытки')
    server_response = models.CharField(verbose_name='Ответ сервера', **NULLABLE)
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f"{self.pk} {self.status} {self.mailing_settings}"

    class Meta:
        verbose_name = 'логи рассылки'
        verbose_name_plural = 'логи рассылок'


class Log(models.Model):
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Рассылка')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=20, verbose_name='Статус попытки')
    response = models.TextField(blank=True, verbose_name='Ответ сервера')

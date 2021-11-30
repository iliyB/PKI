from typing import List

from Crypto.PublicKey import RSA

from django.core.files.base import ContentFile
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Certificate(models.Model):
    """
    Model for Certificate x.509
    """
    version = models.CharField(
        max_length=20,
        blank=True,
        default="1",
        verbose_name="Версия сертификата"
    )
    serial_number = models.CharField(
        max_length=50,
        verbose_name="Серийный номер сертификата", blank=True, null=True
    )
    id_algorithm_signature = models.CharField(
        max_length=50,
        verbose_name="Идентификатор алгоритма цифровой подписи", blank=True, null=True
    )
    publisher_name = models.CharField(
        max_length=50,
        verbose_name="Имя издателя", blank=True, null=True
    )
    start_time = models.DateTimeField(
        verbose_name="Дата начала действия сертификата", blank=True, null=True
    )
    end_time = models.DateTimeField(
        verbose_name="Дата конца действия сертификата", blank=True, null=True
    )
    subject_name = models.CharField(
        max_length=50,
        verbose_name="Имя субъекта сертификата", blank=True, null=True
    )
    public_key = models.CharField(
        max_length=500,
        verbose_name="Публичный ключ субъекта", blank=True, null=True
    )
    id_publisher = models.CharField(
        max_length=200,
        verbose_name="Уникальный идентификатор издателя", blank=True, null=True
    )
    id_subject = models.CharField(
        max_length=200,
        verbose_name="Уникальный идентификатор субъекта", blank=True, null=True
    )
    signature = models.CharField(
        max_length=2000,
        verbose_name="Цифровая электронная подпись сертификата", blank=True, null=True
    )

    # def get_absolute_url(self):
    #     return reverse('certificate_detail_url', kwargs={'pk': self.pk})

    def get_check_url(self):
        return reverse('check_key_url', kwargs={'pk': self.pk})

    def __str__(self):
        return self.serial_number or ''

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'


class User(AbstractUser):

    certificate =models.OneToOneField(
        Certificate,
        verbose_name="Cертификат пользователя",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='user'
    )
    certificates = models.ManyToManyField(
        Certificate,
        verbose_name="Сертификаты субъектов",
        blank=True,
        null=True,
        related_name='subject_user'
    )
    secret_key = models.CharField(
        max_length=40,
        blank=True,
        default=BaseUserManager.make_random_password(40)
    )
    private_key = models.FileField(
        upload_to="private_key",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS: List = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if not self.private_key:
            private_key = RSA.generate(2024)
            self.private_key.save(
                f'{self.username}.pem',
                ContentFile(private_key.export_key('PEM')),
                save=True
            )


class Key(models.Model):
    public_key = models.FileField(upload_to="public", blank=True, null=True)
    private_key = models.FileField(upload_to="private", blank=True, null=True)
    active = models.BooleanField(
        default=True, blank=True
    )

    class KeyType(models.TextChoices):
        Reg = "Ключ регистрационного центра"
        Cert = "Ключ сертификационного центра"

    type = models.CharField(
        max_length=100,
        choices=KeyType.choices,
        blank = True, null = True
    )

    def __str__(self):
        return self.type


class File(models.Model):
    source_file = models.FileField(upload_to="source_file", blank=True, null=True)
    new_file = models.FileField(upload_to="new_file", blank=True, null=True)

    def __str__(self):
        return str(self.pk)

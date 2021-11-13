from django.db import models


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
        max_length=200,
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
        max_length=600,
        verbose_name="Цифровая электронная подпись сертификата", blank=True, null=True
    )

    # def get_absolute_url(self):
    #     return reverse('certificate_detail_url', kwargs={'pk': self.pk})

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

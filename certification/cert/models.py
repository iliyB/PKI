from django.db import models
from django.urls import reverse


class InfoCancellation(models.Model):
    code_choise = [
        ('1', "Причина не определена"),
        ('2', "Повреждение ключа конечного пользователя"),
        ('3', "Повреждение ключа УЦ"),
        ('4', "Изменение информации в сертификате(не повреждение)"),
        ('5', "Приостановление действия ключа"),
        ('6', "Завершение использования"),
        ('7', "Приостановление использования"),
        ('8', "Отмена временного приостановления")
    ]

    revocation_date = models.DateTimeField(
        verbose_name="Дата получения запроса об аннулировании", blank=True, null=True
    )
    reason_code = models.CharField(
        max_length=5,
        choices=code_choise,
        verbose_name="Код причины аннулирования", blank=True, null=True
    )
    hold_instruction_code = models.CharField(
        max_length=20,
        verbose_name="Код временного приостановления сертификата (OID)", blank=True, null=True
    )
    invalidity_date = models.DateTimeField(
        verbose_name="Дата признания сертификата недействительным", blank=True, null=True
    )


    def __str__(self):
        return str(self.revocation_date)

    class Meta:
        verbose_name = 'Причина аннулирования сертификата'
        verbose_name_plural = 'Причины аннулирования сертификата'


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
    active = models.BooleanField(
        default=True,
        verbose_name="Указывает, является ли сертификат действующим", blank=True
    )
    info_cancellation = models.OneToOneField(
        InfoCancellation,
        verbose_name="Информация об аннулировании", blank=True, null=True,
        related_name="certificate",
        on_delete=models.CASCADE
    )
    signature = models.CharField(
        max_length=600,
        verbose_name="Цифровая электронная подпись сертификата", blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse('certificate_detail_url', kwargs={'pk': self.pk})

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'



class Key(models.Model):
    public_key = models.FileField(upload_to="public", blank = True, null = True)
    private_key = models.FileField(upload_to="private", blank = True, null = True)
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

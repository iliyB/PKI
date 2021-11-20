from django.db import models
from django.urls import reverse


class Subject(models.Model):
    address = models.CharField(
        max_length=50,
        verbose_name="Сетевой адрес субъекта", blank=True, null=True
    )
    subject_name = models.CharField(
        max_length=50,
        verbose_name="Имя субъекта", unique=True
    )
    secret_key = models.CharField(
        max_length=50,
        verbose_name="Секретный ключ субъекта(для подтверждения личности)", blank=True, null=True
    )

    def __str__(self):
        return self.subject_name

    class Meta:
        verbose_name = 'Субъект'
        verbose_name_plural = 'Субъекты'

    def get_absolute_url(self):
        return reverse('subject_detail_url', kwargs={'pk': self.pk})


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

class As(models.Model):
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
    certificate_serial_number = models.CharField(
        max_length=50,
        verbose_name="Серийный номер сертификата"
    )
    revocation_date = models.DateTimeField(
        verbose_name="Дата получения запроса об аннулировании",
        auto_now_add=True
    )
    reason_code = models.CharField(
        max_length=5,
        choices=code_choise,
        verbose_name="Код причины аннулирования",
    )
    hold_instruction_code = models.CharField(
        max_length=20,
        verbose_name="Код временного приостановления сертификата (OID)",
        blank=True, null=True
    )
    invalidity_date = models.DateTimeField(
        verbose_name="Дата признания сертификата недействительным",
        auto_now_add=True
    )
    certificate_issuer = models.CharField(
        max_length=50,
        verbose_name="Имя издателя сертификата, ассоциированного с косвенным САС",
        blank=True, null=True
    )
    signature = models.CharField(
        max_length=600,
        verbose_name="Цифровая электронная подпись сертификата", blank=True, null=True
    )

    def __str__(self):
        return self.certificate_serial_number

    class Meta:
        verbose_name = 'Аннулированный сертификат'
        verbose_name_plural = 'Аннулированные сертификаты'

    def get_absolute_url(self):
        return reverse('as_detail_url', kwargs={'pk': self.pk})


class Sas(models.Model):
    """
    Model fo Sas
    """

    version = models.CharField(
        max_length=20,
        blank=True,
        default="1",
        verbose_name="Версия сертификата"
    )
    id_algorithm_signature = models.CharField(
        max_length=50,
        verbose_name="Идентификатор алгоритма цифровой подписи", blank=True, null=True
    )
    issuer = models.CharField(
        max_length=50,
        verbose_name="Уникальное имя УЦ-издателя САС"
    )
    this_update = models.DateTimeField(
        verbose_name="Дата выпуска данного САС"
    )
    next_update = models.DateTimeField(
        verbose_name="Планируемая дата следующего САС"
    )
    authority_key_identifier = models.CharField(
        max_length=50,
        verbose_name="Идентификатор ключа, используемого для подтверждения САС"
    )
    crl_number = models.CharField(
        max_length=50,
        verbose_name="Серийный номер списка аннулированных сертификатов"
    )
    issuing_distribution_point = models.CharField(
        max_length=200,
        verbose_name="Атрибуты выпускающего пункта распространения САС"
    )
    delta_crl_indicator = models.CharField(
        max_length=200,
        verbose_name="Индикатор разностного списка аннулированных сертификатов (дельта-списка)"
    )
    certificate = models.ManyToManyField(
        As,
        related_name="sas"
    )

    def __str__(self):
        return self.crl_number

    class Meta:
        verbose_name = 'Список аннулированных сертификат'
        verbose_name_plural = 'Списки аннулированных сертификатов'


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


class HistoryRegistration(models.Model):
    subject = models.ForeignKey(
        Subject,
        verbose_name="Имя субъекта",
        on_delete=models.CASCADE, null=True, blank=True,
        related_name='registrations'
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True
    )
    status = models.BooleanField(
        default=True, blank=True
    )
    certificate_serial_number = models.CharField(
        max_length=50,
        verbose_name="Серийный номер сертификата",
        blank=True, null=True,
    )

    def __str__(self):
        return str(self.subject) + str(self.attempt_time)

    class Meta:
        verbose_name = 'Попытка регистрации'
        verbose_name_plural = 'Попытки регистрации'


class HistoryGetKey(models.Model):
    subject = models.ForeignKey(
        Subject,
        verbose_name="Имя субъекта",
        on_delete=models.CASCADE,
        related_name='subjects', null=True, blank=True,
    )
    object = models.ForeignKey(
        Subject,
        verbose_name="Имя объекта",
        on_delete=models.CASCADE,
        related_name='object_list', null=True, blank=True,
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.subject) + ":" + str(self.object)

    class Meta:
        verbose_name = 'История запроса на публичный ключ'
        verbose_name_plural = 'История запросов на публичные ключи'
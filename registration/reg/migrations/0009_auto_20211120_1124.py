# Generated by Django 3.2.9 on 2021-11-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0008_auto_20211106_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='as',
            name='signature',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Цифровая электронная подпись сертификата'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='signature',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Цифровая электронная подпись сертификата'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='public_key',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Публичный ключ субъекта'),
        ),
    ]

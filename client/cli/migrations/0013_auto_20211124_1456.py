# Generated by Django 3.2.9 on 2021-11-24 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cli', '0012_alter_user_secret_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='signature',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Цифровая электронная подпись сертификата'),
        ),
        migrations.AlterField(
            model_name='user',
            name='secret_key',
            field=models.CharField(blank=True, default='GqHDcegFrf', max_length=40),
        ),
    ]

# Generated by Django 3.2.9 on 2021-11-20 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cli', '0007_auto_20211118_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='public_key',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Публичный ключ субъекта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='secret_key',
            field=models.CharField(blank=True, default='GE5SzmnpWZ', max_length=40),
        ),
    ]

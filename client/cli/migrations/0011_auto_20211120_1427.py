# Generated by Django 3.2.9 on 2021-11-20 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cli', '0010_auto_20211120_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='private_key',
            field=models.FileField(blank=True, null=True, upload_to='private'),
        ),
        migrations.AlterField(
            model_name='key',
            name='public_key',
            field=models.FileField(blank=True, null=True, upload_to='public'),
        ),
        migrations.AlterField(
            model_name='key',
            name='type',
            field=models.CharField(blank=True, choices=[('Ключ регистрационного центра', 'Reg'), ('Ключ сертификационного центра', 'Cert')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='secret_key',
            field=models.CharField(blank=True, default='tA2NAszyAY', max_length=40),
        ),
    ]

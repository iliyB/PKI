# Generated by Django 3.2.9 on 2021-12-04 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0012_alter_certificate_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sas',
            name='certificate',
            field=models.ManyToManyField(blank=True, null=True, related_name='sas', to='reg.As'),
        ),
    ]

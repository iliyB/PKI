# Generated by Django 3.2.9 on 2021-11-18 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cli', '0005_alter_user_secret_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='secret_key',
            field=models.CharField(blank=True, default='f8Y6bXgXZ5', max_length=40),
        ),
    ]
# Generated by Django 5.0.7 on 2025-05-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamacoes', '0004_reclamacao_bloquear'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='rejeitar',
            field=models.BooleanField(default=False),
        ),
    ]

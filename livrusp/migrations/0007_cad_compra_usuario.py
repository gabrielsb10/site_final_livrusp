# Generated by Django 3.1.4 on 2020-12-11 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livrusp', '0006_remove_cad_compra_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cad_compra',
            name='usuario',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='livros_compra', to='auth.user'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2.4 on 2021-07-20 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urlshortener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortener',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='shorteners', to='auth.user'),
            preserve_default=False,
        ),
    ]

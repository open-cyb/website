# Generated by Django 3.2.4 on 2021-07-12 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='website',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]

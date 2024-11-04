# Generated by Django 5.1.2 on 2024-11-03 04:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HerSupport', '0003_biomarker_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biomarker',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('response', models.CharField(blank=True, default='', max_length=1000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

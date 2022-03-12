# Generated by Django 3.2.12 on 2022-03-12 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email address'),
        ),
    ]

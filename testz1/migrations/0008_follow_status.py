# Generated by Django 4.2.3 on 2023-07-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testz1', '0007_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('approved', 'Aprobada'), ('denied', 'Denegada')], default='pending', max_length=10),
        ),
    ]
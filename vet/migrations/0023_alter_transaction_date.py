# Generated by Django 4.0.6 on 2022-07-26 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vet', '0022_productinvoice_date_serviceinvoice_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Date of Transaction'),
        ),
    ]

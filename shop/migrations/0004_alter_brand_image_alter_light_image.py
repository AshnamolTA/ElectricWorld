# Generated by Django 5.1.4 on 2024-12-29 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_order_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
        migrations.AlterField(
            model_name='light',
            name='image',
            field=models.ImageField(blank=True, default='preview_image/image.png', null=True, upload_to='image'),
        ),
    ]

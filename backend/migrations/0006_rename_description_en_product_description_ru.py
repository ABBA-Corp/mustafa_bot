# Generated by Django 4.1.3 on 2022-12-02 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_rename_name_en_product_name_ru'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description_en',
            new_name='description_ru',
        ),
    ]

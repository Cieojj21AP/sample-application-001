# Generated by Django 5.0.2 on 2024-08-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address1',
            field=models.CharField(default='Tokyo', max_length=50, verbose_name='住所1'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address2',
            field=models.CharField(max_length=50, null=True, verbose_name='住所2'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='zipcode',
            field=models.IntegerField(default='1000000', max_length=20, verbose_name='郵便番号'),
        ),
    ]

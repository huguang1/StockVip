# Generated by Django 2.1.5 on 2019-05-29 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mosaic', '0003_auto_20190418_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lotteryreceiptdetails',
            options={'ordering': ['-id']},
        ),
    ]
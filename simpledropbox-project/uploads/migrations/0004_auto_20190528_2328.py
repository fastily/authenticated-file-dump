# Generated by Django 2.2.1 on 2019-05-28 23:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0003_auto_20190528_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 28, 23, 28, 24, 915296, tzinfo=utc)),
        ),
    ]

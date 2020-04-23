# Generated by Django 3.0.2 on 2020-04-22 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20200421_0649'),
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(default=-1)),
                ('description', models.CharField(default='', max_length=1000)),
                ('catalog', models.IntegerField(default=-1)),
                ('pic', models.CharField(default='', max_length=1000)),
                ('price', models.IntegerField(default=-1)),
            ],
        ),
        migrations.RemoveField(
            model_name='stock',
            name='description',
        ),
    ]

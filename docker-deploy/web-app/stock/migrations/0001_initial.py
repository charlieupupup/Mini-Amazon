# Generated by Django 3.0.2 on 2020-04-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(default=-1)),
                ('description', models.CharField(default='', max_length=1000)),
                ('count', models.IntegerField(default=-1)),
                ('worldid', models.IntegerField(default=-1)),
                ('whnum', models.IntegerField(default=-1)),
            ],
        ),
    ]

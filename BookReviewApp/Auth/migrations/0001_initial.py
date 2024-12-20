# Generated by Django 5.1.1 on 2024-10-26 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Email', models.CharField(max_length=255, unique=True)),
                ('Username', models.CharField(max_length=255, unique=True)),
                ('Password', models.CharField(max_length=255)),
                ('CreatedAt', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['ID'],
            },
        ),
    ]

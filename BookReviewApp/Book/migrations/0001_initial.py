# Generated by Django 5.1.1 on 2024-10-26 05:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('published_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published_books', to='Auth.auth')),
            ],
        ),
    ]

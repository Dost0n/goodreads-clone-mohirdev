# Generated by Django 4.2.7 on 2023-11-16 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default='default-book.jpg', upload_to='books/'),
        ),
    ]
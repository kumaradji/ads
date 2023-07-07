# Generated by Django 4.2.2 on 2023-07-06 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('category', models.CharField(choices=[('Tanks', 'Танки'), ('Healers', 'Хилы'), ('DD', 'ДД'), ('Merchants', 'Торговцы'), ('Guild Masters', 'Гилдмастеры'), ('Quest Givers', 'Квестгиверы'), ('Smiths', 'Кузнецы'), ('Tanner', 'Кожевники'), ('Potion', 'Зельевары'), ('Spellmasters', 'Мастера заклинаний')], default='Tanks', max_length=20, verbose_name='Category')),
                ('response_text', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('upload', models.FileField(blank=True, help_text='загрузите файл', upload_to='uploads/')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('is_ad_category', models.BooleanField(default=False, verbose_name='Is Advertisement Category')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField(verbose_name='Response text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('status', models.BooleanField(default=False, verbose_name='Is accepted')),
                ('adertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response_user', to='ads.advert', verbose_name='User')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='ads.advert', verbose_name='Article')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отклик',
                'verbose_name_plural': 'Отклики',
            },
        ),
    ]

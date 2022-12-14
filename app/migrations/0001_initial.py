# Generated by Django 4.1.2 on 2022-10-25 15:45

import colorfield.fields
import datetime
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
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=123, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Брэнд',
                'verbose_name_plural': 'Брэнды',
            },
        ),
        migrations.CreateModel(
            name='Cap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=123, verbose_name='Имя')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('cover', models.ImageField(upload_to='media/image/', verbose_name='Главное фото')),
                ('created_date', models.DateTimeField(verbose_name='Дата создания')),
                ('updated_date', models.DateTimeField(verbose_name='Дата изменения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Данный товар активен')),
                ('brand', models.ManyToManyField(related_name='caps', to='app.brand', verbose_name='Брэнды')),
            ],
            options={
                'verbose_name': 'Кепка',
                'verbose_name_plural': 'Кепки',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('cover', models.ImageField(upload_to='media/image/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField()),
                ('total', models.PositiveIntegerField(default=0)),
                ('address', models.CharField(max_length=123)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'В обработке'), (2, 'Заказ не принят'), (3, 'Заказ принят')], default=1, verbose_name='Статус')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(choices=[(1, 'S'), (2, 'M'), (3, 'L'), (4, 'XL')], verbose_name='Размер')),
                ('color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=123, samples=None, verbose_name='Цвет')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('created_date', models.DateTimeField(auto_now=True, verbose_name='Дата завоза')),
                ('updated_date', models.DateTimeField(verbose_name='Дата изменения')),
                ('cap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='app.cap', verbose_name='Кепка')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склад',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена Товара')),
                ('start_date', models.DateTimeField(verbose_name='Дата старта цены')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2999, 12, 31, 12, 0, 59), verbose_name='Дата конца цены')),
                ('is_active', models.BooleanField(default=True, verbose_name='Актуальная цена')),
                ('cap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='app.cap', verbose_name='Кепка')),
            ],
            options={
                'verbose_name': 'Цена',
                'verbose_name_plural': 'Цены',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='app.order', verbose_name='Заказ')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='app.stock', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Детальный заказ',
                'verbose_name_plural': 'Детальный заказ',
            },
        ),
        migrations.CreateModel(
            name='DetailPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/image/', verbose_name='Детальное фото')),
                ('cap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='app.cap', verbose_name='Кепка')),
            ],
            options={
                'verbose_name': 'Детальное фото',
                'verbose_name_plural': 'Детальные фотки',
            },
        ),
    ]

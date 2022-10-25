# Generated by Django 4.1.2 on 2022-10-21 13:27

import colorfield.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_alter_price_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/image/', verbose_name='Детальное фото')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='stock',
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=123, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='cap',
            name='brand',
            field=models.ManyToManyField(related_name='caps', to='app.brand', verbose_name='Брэнды'),
        ),
        migrations.AlterField(
            model_name='cap',
            name='cover',
            field=models.ImageField(upload_to='media/image/', verbose_name='Главное фото'),
        ),
        migrations.AlterField(
            model_name='cap',
            name='created_date',
            field=models.DateTimeField(verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='cap',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='cap',
            name='name',
            field=models.CharField(max_length=123, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='cap',
            name='updated_date',
            field=models.DateTimeField(verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='link',
            name='cover',
            field=models.ImageField(upload_to='media/image/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'В обработке'), (2, 'Заказ не принят'), (1, 'Заказ принят')], default=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='price',
            name='cap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='app.cap', verbose_name='Кепка'),
        ),
        migrations.AlterField(
            model_name='price',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2999, 12, 31, 12, 0, 59), verbose_name='Дата конца цены'),
        ),
        migrations.AlterField(
            model_name='price',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Актуальная цена'),
        ),
        migrations.AlterField(
            model_name='price',
            name='start_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата старта цены'),
        ),
        migrations.AlterField(
            model_name='price',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена Товара'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='cap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='app.cap', verbose_name='Кепка'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=123, samples=None, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='created_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата завоза'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='size',
            field=models.PositiveIntegerField(choices=[(1, 'S'), (2, 'M'), (3, 'L'), (1, 'XL')], verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='updated_date',
            field=models.DateTimeField(verbose_name='Дата изменения'),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='app.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='app.stock', verbose_name='Склад'),
        ),
        migrations.AddField(
            model_name='detailphoto',
            name='cap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='app.cap', verbose_name='Кепка'),
        ),
    ]

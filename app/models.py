from datetime import datetime
from django.utils.html import format_html
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField



User = get_user_model()


class Brand(models.Model):
    name = models.CharField(
        max_length=123,
        verbose_name=_('Имя')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'


class Cap(models.Model):
    brand = models.ManyToManyField(
        Brand,
        related_name='caps',
        verbose_name=_('Брэнды'),)
    name = models.CharField(
        max_length=123,
        verbose_name=_('Имя'))
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание'),)
    cover = models.ImageField(
        upload_to='media/image/',
        verbose_name=_('Главное фото'),)
    created_date = models.DateTimeField(
        verbose_name=_('Дата создания'),
    )
    updated_date = models.DateTimeField(
        verbose_name=_('Дата изменения'),
    )
    is_active = models.BooleanField(
        verbose_name=_('Данный товар активен'),
        default=True
    )

    def cover_image(self):
        return format_html(f'<img src="{self.cover.url}" style="width:100px;height:150px;" />')

    @property
    def price(self):
        return self.prices.get(is_active=True).value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кепка'
        verbose_name_plural = 'Кепки'


class DetailPhoto(models.Model):
    image = models.ImageField(
        upload_to='media/image/',
        verbose_name=_('Детальное фото'))
    cap = models.ForeignKey(
        Cap,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_('Кепка'))

    class Meta:
        verbose_name = 'Детальное фото'
        verbose_name_plural = 'Детальные фотки'


class Price(models.Model):
    value = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        verbose_name=_('Цена Товара'))
    start_date = models.DateTimeField(
        verbose_name=_('Дата старта цены'))
    end_date = models.DateTimeField(
        default=datetime(year=2999, month=12, day=31, hour=12, second=59),
        verbose_name=_('Дата конца цены'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Актуальная цена'))
    cap = models.ForeignKey(
        Cap,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name=_('Кепка'))

    def save(self, *args, **kwargs):

        previos_price = self.cap.prices.filter(is_active=True).last()

        if previos_price is not None and self != previos_price:
            previos_price.is_active = False
            previos_price.end_date = self.start_date
            previos_price.save()

        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.cap)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Stock(models.Model):
    cap = models.ForeignKey(
        Cap,
        on_delete=models.CASCADE,
        related_name='stocks',
        verbose_name=_('Кепка'))
    size = models.PositiveIntegerField(
        choices=(
            (1, 'S'),
            (2, 'M'),
            (3, 'L'),
            (4, 'XL'),
        ),
        verbose_name=_('Размер')
    )
    color = ColorField(
        max_length=123,
        verbose_name=_('Цвет'),
        default='#FF0000')
    quantity = models.PositiveIntegerField(
        verbose_name=_('Количество')
    )
    created_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата завоза'))
    updated_date = models.DateTimeField(
        verbose_name=_('Дата изменения')
    )

    def __str__(self):
        return f'{self.cap} {self.get_size_display()}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Пользователь')
    )
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField()
    total = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=123)
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'В обработке'),
            (2, 'Заказ не принят'),
            (3, 'Заказ принят'),
        ),
        default=1,
        verbose_name=_('Статус')
    )

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 3:
            for order_detail in self.order_details.all():
                stock = order_detail.stock

                stock.quantity -= order_detail.quantity
                stock.save()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_('Заказ'),
        related_name='order_details'
        )
    stock = models.ForeignKey(
        Stock,
        related_name='order_details',
        verbose_name=_('Склад'),
        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name=_('Количество')
    )

    class Meta:
        verbose_name = 'Детальный заказ'
        verbose_name_plural = 'Детальный заказ'


class Link(models.Model):
    url = models.URLField(
        verbose_name=_('Ссылка')
    )
    cover = models.ImageField(
        upload_to='media/image/',
        verbose_name=_('Изображение'))

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'


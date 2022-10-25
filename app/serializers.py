from rest_framework import serializers
from .models import Cap, Stock, Order, Brand, Link, Price, DetailPhoto, OrderDetail


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')


class CapListSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    brand = BrandSerializer(many=True)
    class Meta:
        model = Cap
        fields = ('id', 'cover', 'name', 'brand', 'price')


class SizeSerializer(serializers.ModelSerializer):

    size_name = serializers.CharField(source='get_size_display')

    class Meta:
        model = Stock
        fields = ('size', 'color', 'size_name')

    # def to_representation(self, instance):
    #     return super().to_representation(instance)['cap']


class DetailPhtotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailPhoto
        fields = ('image', )


class LinkSerializer(serializers.Serializer):
    class Meta:
        model = Link
        fields = ('id', 'url', 'cover')


class CapDetailSerializer(serializers.ModelSerializer):
    stocks = SizeSerializer(many=True)
    brand = BrandSerializer(many=True)
    detail_photo = DetailPhtotoSerializer(many=True, source='photos')

    class Meta:
        model = Cap
        fields = ('id', 'name', 'brand', 'cover', 'description', 'stocks', 'detail_photo', 'price')

        def to_representation(self, instance):
            return super().to_representation(instance)['stocks']


class StockSerializer(serializers.ModelSerializer):
    cap = CapListSerializer()
    size = serializers.CharField(source='get_size_display')

    class Meta:
        model = Stock
        fields = ('cap', 'size', 'color')


class OrderDetailCreateSerializer(serializers.ModelSerializer):

    color = serializers.CharField(write_only=True)
    size = serializers.CharField(write_only=True)
    cap = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderDetail
        exclude = ('order', )


class OrderDetailSerializer(serializers.ModelSerializer):
    stock = StockSerializer()

    class Meta:
        model = OrderDetail
        exclude = ('order', )


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_details = OrderDetailCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'order_details', 'address', 'total')

    def create(self, validated_data):
        order = Order(user=validated_data['user'], address=validated_data['address'], total=validated_data['total'])
        order.save()

        for order_detail in validated_data['order_details']:
            OrderDetail(order=order, stock=order_detail['stock'], quantity=order_detail['quantity']).save()

        return order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'order_details')


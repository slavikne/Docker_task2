from rest_framework import serializers
from .models import Product, StockProduct, Stock
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['title', 'description', 'stocks']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

    def create(self, validated_data):
        return super().create(validated_data)


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = ['address', 'positions']


    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for i in positions:
            StockProduct.objects.create(
                stock=stock,
                product=i.get('product'),
                quantity=i.get('quantity'),
                price=i.get('price'),
            )

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        for i in positions:
            q = StockProduct.objects.filter(product=i.get('product'), stock=stock)
            if q:
                q.update(
                    quantity=i.get('quantity'),
                    price=i.get('price'),
                )
            else:
                StockProduct.objects.create(
                    stock=stock,
                    product=i.get('product'),
                    quantity=i.get('quantity'),
                    price=i.get('price'),
                )
        return stock








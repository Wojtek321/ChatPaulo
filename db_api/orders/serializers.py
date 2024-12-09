from django.utils import timezone

from rest_framework import serializers

from core.models import Order, OrderItem

from datetime import timedelta


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'price', 'detail_note']
        extra_kwargs = {
            'price': {'read_only': True},
            'quantity': {'default': 1}
        }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_time', 'order_type', 'total_price', 'order_note',
            'customer_name', 'customer_phone', 'address', 'pickup_time',
            'delivery_time', 'items'
        ]
        extra_kwargs = {
            'order_time': {'read_only': True},
            'total_price': {'read_only': True}
        }

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must contain at least one item.")
        return items

    def validate(self, data):
        order_type = data.get('order_type')

        if order_type == 'on-site':
            self._validate_on_site(data)
        elif order_type == 'pick-up':
            self._validate_pick_up(data)
        elif order_type == 'delivery':
            self._validate_delivery(data)
        else:
            raise serializers.ValidationError(f"Invalid order type: '{order_type}'.")
        return data

    def _validate_on_site(self, data):
        data['customer_name'] = None
        data['customer_phone'] = None
        data['address'] = None
        data['pickup_time'] = None
        data['delivery_time'] = None

    def _validate_pick_up(self, data):
        if not data.get('customer_name'):
            raise serializers.ValidationError("Customer name is required for pick-up orders.")
        if not data.get('customer_phone'):
            raise serializers.ValidationError("Customer phone is required for pick-up orders.")
        data['pickup_time'] = timezone.now() + timedelta(minutes=30)
        data['delivery_time'] = None

    def _validate_delivery(self, data):
        if not data.get('customer_name'):
            raise serializers.ValidationError("Customer name is required for delivery orders.")
        if not data.get('customer_phone'):
            raise serializers.ValidationError("Customer phone is required for delivery orders.")
        if not data.get('address'):
            raise serializers.ValidationError("Address is required for delivery orders.")
        data['delivery_time'] = timezone.now() + timedelta(minutes=60)
        data['pickup_time'] = None

    def create(self, validated_data):
        validated_data['order_time'] = timezone.now()

        items_data = validated_data.pop('orderitem_set', [])
        total_price = 0

        for item_data in items_data:
            item = item_data['item']
            price = item.price
            quantity = item_data['quantity']
            total_price += price * quantity


        order = Order.objects.create(total_price=total_price, **validated_data)

        for item_data in items_data:
            item = item_data['item']
            price = item.price
            quantity = item_data['quantity']
            total_price += price * quantity

            OrderItem.objects.create(
                order=order,
                item=item,
                price=price,
                quantity=quantity,
                detail_note=item_data.get('detail_note'),
            )

        return order

    # TODO order update

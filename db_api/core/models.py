from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingredient'


class Item(models.Model):
    name = models.CharField(max_length=50)
    type = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item'


class Order(models.Model):
    order_time = models.DateTimeField()
    order_type = models.TextField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_note = models.TextField(blank=True, null=True)
    customer_name = models.CharField(max_length=250, blank=True, null=True)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    pickup_time = models.DateTimeField(blank=True, null=True)
    delivery_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, models.CASCADE)
    item = models.ForeignKey(Item, models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    detail_note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_item'


class Recipe(models.Model):
    item = models.ForeignKey(Item, models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, models.CASCADE)
    quantity = models.SmallIntegerField()
    unit = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'recipe'
        unique_together = (('item', 'ingredient'),)

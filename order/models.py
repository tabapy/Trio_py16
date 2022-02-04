from django.contrib.auth.models import User
from django.db import models

from menu.models import Product


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='orders')
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order Id: {self.pk} for {self.user.username}'

    @property
    def total_cost(self):
        return sum([item.get_cost() for item in self.items.all()])

    class Meta:
        ordering = ('-created',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'OrderId: {self.order.id}, {self.product.name}'

    def get_cost(self):
        return self.quantity * self.product.price


# Chefburger 2 - get_cost = chefburger.price * 2 = 12
# Cola - 3 - get_cost = cola.price * 3 = 9
#
# [9, 12]
# chefburger.price * 2 + cola.price * 3 = total_cost
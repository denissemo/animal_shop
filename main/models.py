from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='static/uploads')

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    description = models.TextField()
    weight = models.IntegerField()
    image = models.ImageField(upload_to='static/uploads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    age = models.ForeignKey(Age, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {} {} г'.format(self.brand.name, self.name, self.weight)


class Client(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    email = models.CharField(max_length=256, default=None)
    phone_number = models.CharField(max_length=256)

    def __str__(self):
        return f'Имя: {self.name}; Телефон: {self.phone_number}'


class Order(models.Model):
    items = models.ManyToManyField(Item)

    city = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    house_number = models.CharField(max_length=256)
    total = models.CharField(max_length=256)
    comment = models.TextField(default=None)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заказ #{self.id}; в город: {self.city}; телефон клиента: {self.client.phone_number}; товара на сумму: {self.total} грн.'

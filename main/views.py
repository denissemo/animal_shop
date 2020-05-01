from django.shortcuts import render, HttpResponse
from .models import *
import json
from collections import Counter


def main_page(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'main/main.html', context)


def category(request, category_id):
    if isinstance(category_id, str):
        items = Item.objects.filter(name__icontains=category_id)
    else:
        items = Item.objects.filter(category_id=category_id)

    context = {
        'items': items
    }

    return render(request, 'category/main.html', context)


def add_to_cart(request):
    item_id = request.GET.get('item_id')

    response = HttpResponse(200)

    items = request.COOKIES.get('items')

    if items is None:
        response.set_cookie('items', json.dumps([item_id]))
    else:
        try:
            items = json.loads(items)
            items.append(item_id)
            response.set_cookie('items', json.dumps(items))
        except Exception as e:
            print(e)

    return response


def cart(request):
    items = request.COOKIES.get('items')

    if not items or items == '[]':
        response = HttpResponse(
            render(request, 'main/cart.html', {'is_empty': True}))
        response.set_cookie('items', json.dumps([]))

        return response

    items = json.loads(items)
    item_ids = [int(i) for i in items]

    count = dict(Counter(item_ids))

    items = Item.objects.filter(pk__in=item_ids)

    for item in items:
        item.__setattr__('count', count.get(item.id))

    total = 0

    for it_id in item_ids:
        for item in items:
            if it_id == item.id:
                total += float(item.price)

    context = {
        'items': items,
        'total': total,
        'is_empty': False
    }

    response = HttpResponse(render(request, 'main/cart.html', context))

    response.set_cookie('items', json.dumps(item_ids))

    return response


def add_item(request):
    item_id = request.GET.get('item_id')
    response = update_items(request, item_id, 'add')

    return response


def remove_item(request):
    item_id = request.GET.get('item_id')
    response = update_items(request, item_id, 'remove')

    return response


def update_items(request, item_id, method):
    item_id = int(item_id)

    items = request.COOKIES.get('items')
    items = json.loads(items)
    item_ids = [int(i) for i in items]

    if method == 'add':
        item_ids.append(item_id)
    elif method == 'remove':
        try:
            item_ids.remove(item_id)
        except Exception as e:
            print(e)

    response = HttpResponse(200)
    response.set_cookie('items', json.dumps(item_ids))

    return response


def buy(request):
    name = request.GET.get('name')
    surname = request.GET.get('surname')
    email = request.GET.get('email')
    phone_number = request.GET.get('phone_number')
    city = request.GET.get('city')
    street = request.GET.get('street')
    house_number = request.GET.get('house_number')
    comment = request.GET.get('comment')
    total = request.GET.get('total')

    items = [name, surname, phone_number, city, street, house_number]

    if not any(items):
        return HttpResponse(400)

    items = request.COOKIES.get('items')
    items = json.loads(items)
    item_ids = [int(i) for i in items]

    client = Client(name=name, surname=surname, email=email,
                    phone_number=phone_number)
    client.save()

    order = Order(city=city, street=street, house_number=house_number,
                  comment=comment, total=total, client_id=client.id)
    order.save()

    for item_id in item_ids:
        item = Item.objects.get(id=item_id)
        order.items.add(item)

    response = HttpResponse(200)
    response.set_cookie('items', json.dumps([]))

    return response

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
import json

from .models import Category, Item, CategoryType
from .forms import CategoryForm, ItemForm


def index(request):
    return redirect("template_gen")


def template_gen(request):
    categories = Category.objects.all()
    positive_categories = sorted(
        filter(lambda c: c.type == CategoryType.POSITIVE.name, categories),
        key=lambda c: c.name.lower()
    )
    negative_categories = sorted(
        filter(lambda c: c.type == CategoryType.NEGATIVE.name, categories),
        key=lambda c: c.name.lower()
    )

    context = {
        "form": CategoryForm(),
        "positive_categories": positive_categories,
        "negative_categories": negative_categories,
    }
    return render(request, "template_gen.html", context)


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("template_gen")


def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
        return redirect("template_gen")
    else:
        form = CategoryForm(instance=category)

    return render(request, 'update_category.html', {"form": form, "category": category})


def delete_category(request, category_id):
    get_object_or_404(Category, pk=category_id).delete()
    return redirect("template_gen")


def manage_items(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, "manage_items.html", {"form": ItemForm(), "category": category})


def delete_item(request, category_id, item_id):
    get_object_or_404(Category, pk=category_id)
    get_object_or_404(Item, pk=item_id).delete()
    return redirect("manage_items", category_id)


def create_item(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            category.items.add(item)
            category.save()

    return redirect("manage_items", category_id)


def update_item(request, category_id, item_id):
    category = get_object_or_404(Category, pk=category_id)
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return redirect("manage_items", category_id)
    else:
        form = ItemForm(instance=item)

    return render(request, 'update_item.html', {"form": form, "category": category, "item": item})


def export_data(request):
    categories = Category.objects.all()

    categories_data = [
        {
            'id': category.id,
            'name': category.name,
            'type': category.type,
            'items': [
                {
                    'title': item.title,
                    'value': item.value
                }
                for item in category.items.all()
            ]
        }
        for category in categories
    ]

    response = JsonResponse(categories_data, safe=False)
    response['Content-Disposition'] = 'attachment; filename="ai-template-gen-bak.json"'
    return response


def import_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        data = json.load(uploaded_file)

        Item.objects.all().delete()
        Category.objects.all().delete()

        for category_data in data:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                type=category_data['type']
            )
            for item_data in category_data['items']:
                item, created = Item.objects.get_or_create(
                    title=item_data['title'],
                    value=item_data['value']
                )
                category.items.add(item)
                category.save()

    return redirect("template_gen")

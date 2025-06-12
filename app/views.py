from django.shortcuts import render, get_object_or_404, redirect

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
    return render(request, "manage_items.html", {"form": ItemForm(),"category": category})


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


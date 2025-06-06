from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path("template-gen/", views.template_gen, name="template_gen"),
    path("create-category/", views.create_category, name="create_category"),
    path("<int:category_id>/manage-items/", views.manage_items, name="manage_items"),
    path("<int:category_id>/manage-items/<int:item_id>/delete", views.delete_item, name="delete_items"),
    path("<int:category_id>/manage-items/create", views.create_item, name="create_item"),
]

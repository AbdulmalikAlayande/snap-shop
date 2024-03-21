from django.urls import path
from store import views

urlpatterns = [
    path("products/", views.get_all_products),
    path("product/<int:product_id>/", views.get_product),
    path("product/<int:product_price>/", views.filter_products_by_price),
    path("product/<int:min>/<int:max>/", views.filter_products_by_price_range),
    path("products/filter_complex_lookup", views.filter_using_complex_lookups),
    path("products/filter_complex_lookup_with_Q", views.filter_complex_lookups_using_the_Q_object),
    path("products/filter_complex_lookup_with_F", views.filter_complex_lookups_by_referencing_fields_with_the_F_object),
    path("products/filter_by_model_relationship", views.filter_by_model_relationship),
    path("products/filter_complex_lookup_multiple_filter", views.filter_using_complex_lookups_with_multiple_filter_calls),
]

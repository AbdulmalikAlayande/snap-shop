from django.urls import path
# from store import views_example, views
from store.views import CustomerRegistrationView, SnapShopProductsView, SnapShopProductView, AddToCartView


urlpatterns = [
    path('customer/register/', CustomerRegistrationView.as_view()),
    path('products/', SnapShopProductsView.as_view()),
    path('product/<int:id>', SnapShopProductView.as_view()),
    path('cart/add-item', AddToCartView.as_view())
]

# urlpatterns = [
#     path("products/", views_example.get_all_products),
#     path("product/<int:product_id>/", views_example.get_product),
#     path("product/<int:product_price>/", views_example.filter_products_by_price),
#     path("product/<int:min>/<int:max>/", views_example.filter_products_by_price_range),
#     path("products/filter_complex_lookup", views_example.filter_using_complex_lookups),
#     path("products/filter_complex_lookup_with_Q", views_example.filter_complex_lookups_using_the_Q_object),
#     path("products/filter_complex_lookup_with_F", views_example.filter_complex_lookups_by_referencing_fields_with_the_F_object),
#     path("products/get_sorted_products", views_example.get_sorted_products),
#     path("products/select_fields_to_query", views_example.select_fields_to_query),
#     path("products/get_customers_with_dot_com_account", views_example.get_customers_with_dot_com_account),
#     path("products/get_orders_placed_by_customer_with_id_1", views_example.get_orders_placed_by_customer_with_id_1),
#     path("products/annotate_customer_table_with_new_fields", views_example.annotate_customer_table_with_new_fields),
#     path("products/concat_fields_in_a_database_table", views_example.concat_fields_in_a_database_table),
#     path("products/filter_by_model_relationship", views_example.filter_by_model_relationship),
#     path("products/filter_complex_lookup_multiple_filter", views_example.filter_using_complex_lookups_with_multiple_filter_calls),
# ]

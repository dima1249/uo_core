from django.urls import path
from .views import *

urlpatterns = [
    path('brand/', ListCreateBrandAPIView.as_view(), name='get_post_brands'),
    path('brand/<int:pk>/', RetrieveUpdateDestroyBrandAPIView.as_view(), name='get_delete_update_brand'),

    path('product/', ListCreateProductAPIView.as_view(), name='get_post_products'),
    path('product/<int:pk>/', RetrieveUpdateDestroyProductAPIView.as_view(), name='get_delete_update_product'),

    path('category/', ListCreateCategoryAPIView.as_view(), name='get_post_categories'),
    path('category/<int:pk>/', RetrieveUpdateDestroyCategoryAPIView.as_view(), name='get_delete_update_category'),

    path("cart/", CartItemAPIView.as_view()),  # add item
    path("cart-item/<int:pk>/", CartItemView.as_view()),

    path("checkout/<int:pk>/", CheckoutView.as_view()),
    path("cart/checkout/", CheckoutCartView.as_view()),
    #
    path("order/<int:pk>/", OrderView.as_view()),

    path("create_invoice/", CreateInvoiceView.as_view()),
    # path("check_invoice/", CheckInvoiceView.as_view()),

    path(r"bank_check_invoicev2/(?P<ref_number>\d+)",
         BankCheckInvoiceV2, name=
         "BankCheckInvoiceV2", ),
    # restRouter.register(r"check_invoice", CheckInvoice, "CheckInvoice")
    # path("payment/", Payment),
]

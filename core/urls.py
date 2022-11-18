from django.urls import path
from .views import (
    ItemDetailView,
    #StartInvesting,
    CheckoutView,
    HomeView,
    invest,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    DashboardView,
    profile,
    VerificationView,
    home,
    add_to_transaction
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-transaction/<slug>/', add_to_transaction, name='add-to-transactions'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('dashboard/<slug>/', DashboardView.as_view(), name='profile'),
    path('start-investing/', invest, name='invest'),
    path('accounts/deposit/verification', VerificationView.as_view(), name='verification')
  
]

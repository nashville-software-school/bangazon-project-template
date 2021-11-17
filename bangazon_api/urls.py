from rest_framework.routers import DefaultRouter
from bangazon_api import views

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', views.CategoryView, 'category')
router.register(r'orders', views.OrderView, 'order')
router.register(r'payment-types', views.PaymentTypeView, 'paymentType')
router.register(r'products', views.ProductView, 'product')
router.register(r'stores', views.StoreView, 'store')

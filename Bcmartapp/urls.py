from django.urls import path

from .views import *

urlpatterns = [
	#Leave as empty string for base url
	path('', store, name="store"),
	path('cart/', cart, name="cart"),
	path('checkout/', checkout, name="checkout"),
  path('view/<det>/',detview,name="view_det"),
	path('update_item/', updateItem, name="update_item"),
	path('process_order/', processOrder, name="process_order"),
 

]
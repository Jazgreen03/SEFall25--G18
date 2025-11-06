"""
Manages the API calls for any operations related to the User

Current API Calls Handled:
    1. Place Order
    2. Get Order
    3. Get Active Orders
    4. Update Order Status
    5. Get Available Items
"""

from django.urls import path
import Order.views as views

urlpatterns = [
    path("items/<str:orgName>/", views.getAvailableItems),
    path("order/place/", views.placeOrder),
    path("orders/", views.getActiveOrders),
    path("orders/open/", views.getOpenOrders),
    path("order/<int:orderID>/update/", views.updateOrder),
    path("order/<int:orderID>/", views.singleOrderAction),
]

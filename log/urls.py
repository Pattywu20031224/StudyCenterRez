from django.urls import path
from .views import *

urlpatterns = [
    path('', LogList.as_view(), name='log_list'),
    path('checkout/', CheckoutUser.as_view(), name='checkout_user'), 
    path('checkout/<int:rid>/', CheckoutSeat.as_view(), name='checkout_seat'), 
    path('checkout/<int:rid>/<int:bid>/', CheckoutLog.as_view(), name='checkout_log'),
    path('return/', ReturnSeat.as_view(), name='return_seat'), 
    path('return/<int:lid>/', ReturnLog.as_view(), name='return_log'),
    path('<int:pk>/delete/', LogDelete.as_view(), name='log_delete'),
    path('mylog/', LogList.as_view(), name='log_list_mine'),
]
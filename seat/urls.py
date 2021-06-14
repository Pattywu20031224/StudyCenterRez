from django.urls import path
from .views import *

urlpatterns = [
    path('', SeatList.as_view(), name='seat_list'),
    path('add/', SeatAdd.as_view(), name='seat_add'), 
    path('<int:pk>/', SeatView.as_view(), name='seat_view'),
    path('<int:pk>/edit/', SeatEdit.as_view(), name='seat_edit'),
    path('<int:pk>/delete/', EquipDelete.as_view(), name='seat_delete'),
    path('<int:pk>/reserve/',SeatReserve.as_view(), name='seat_reserve'),
]
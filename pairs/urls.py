from django.urls import path

from pairs import views

app_name = 'pairs'

urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('<str:chain>/<str:pair_address>/', views.PairView.as_view(), name='pair_address'),
]

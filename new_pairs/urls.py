from django.urls import path

from new_pairs.views import NewPairsView

app_name = 'new_pairs'

urlpatterns = [
    path('<slug:chain>/', NewPairsView.as_view(), name='chain'),
]

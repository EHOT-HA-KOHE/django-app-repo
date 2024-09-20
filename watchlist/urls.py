from django.urls import path

from watchlist import views


app_name = 'watchlist'


urlpatterns = [
    path('categories/', views.CollectionsView.as_view(), name='categories'),
    path('categories/<str:category_name>', views.CollectionPairsView.as_view(), name='category_pools'),
    path('add_to_category/', views.AddPoolToCollectionView.as_view(), name='add_to_category'),
    path('del_from_category/', views.DelPoolFromCollectionView.as_view(), name='del_from_category'),
    path('create_category/', views.CreateNewCollectionView.as_view(), name='create_category'),
    path('del_category/', views.DelCollectionView.as_view(), name='del_category'),
]

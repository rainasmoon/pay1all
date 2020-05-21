from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
        path('', views.index, name='index'),
        path('<int:cid>/', views.index, name='index_c'),
        path('compare/<int:aproduct_id>/<int:bproduct_id>/', views.compare, name='compare'),
        path('compare/<int:aproduct_id>/<int:bproduct_id>/<int:cid>/', views.compare, name='compare_c'),
        path('vote/<int:aproduct_id>/<int:bproduct_id>/', views.vote, name='vote'),
        path('details/<int:pk>/', views.DetailsView.as_view(), name='details'),
        path('search/', views.search, name='search'),
        path('menus/', views.menus, name='menus'),
        path('results/', views.ResultsView.as_view(), name='results'),
        path('about/', views.about, name='about'),
]

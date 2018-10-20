from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'locations', views.LocationViewSets, base_name='locations-list')
router.register(r'spots', views.SpotViewSets, base_name='spots-list')
router.register(r'reports', views.ReportViewSets, base_name='reports-list')
router.register(r'comments', views.CommentViewSets, base_name='comments-list')
router.register(r'favs', views.FavViewSets, base_name='favs-list')

app_name = 'plan'
urlpatterns = [
    path('', include(router.urls))
]

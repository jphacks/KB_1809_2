from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from . import views


router = SimpleRouter()
router.register(r'locations', views.LocationViewSets, base_name='locations')
router.register(r'spots', views.SpotViewSets, base_name='spots')
router.register(r'plans', views.PlanViewSets, base_name='plans')

plan_nested_router = NestedSimpleRouter(router, r'plans', lookup='plan')
plan_nested_router.register(r'favs', views.FavViewSets)
plan_nested_router.register(r'comments', views.CommentViewSets, base_name='comment')
plan_nested_router.register(r'reports', views.ReportViewSets)

app_name = 'plan'
urlpatterns = [
    path('', include(router.urls)),
    path('', include(plan_nested_router.urls))
]

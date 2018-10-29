from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views
from accounts import views as account_views


router = DefaultRouter()
router.register(r'locations', views.LocationViewSets, base_name='locations')
router.register(r'spots', views.SpotViewSets, base_name='spots')
router.register(r'plans', views.PlanViewSets, base_name='plans')
router.register(r'users', account_views.UserViewSets, base_name='users')
router.register(r'me', account_views.MeViewSets, base_name='me')

plan_nested_router = NestedDefaultRouter(router, r'plans', lookup='plan')
plan_nested_router.register(r'favs', views.FavViewSets)
plan_nested_router.register(r'comments', views.CommentViewSets)
plan_nested_router.register(r'reports', views.ReportViewSets)

user_nested_router = NestedDefaultRouter(router, r'users', lookup='user')
user_nested_router.register(r'favs', views.UserFavView)
user_nested_router.register(r'plans', views.UserPlanView)

app_name = 'plan'
urlpatterns = [
    path('me/favs/', views.UserFavView.as_view({'get': 'list'})),
    path('me/plans/', views.UserPlanView.as_view({'get': 'list'})),
    path('me/plans/<int:pk>', views.UserPlanView.as_view({'get': 'retrieve'})),
    path('', include(router.urls)),
    path('', include(plan_nested_router.urls)),
    path('', include(user_nested_router.urls)),
]

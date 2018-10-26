from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'locations', views.LocationViewSets, base_name='locations')
router.register(r'spots', views.SpotViewSets, base_name='spots')
router.register(r'reports', views.ReportViewSets, base_name='reports')
router.register(r'comments', views.CommentViewSets, base_name='comments')
router.register(r'favs', views.FavViewSets, base_name='favs')
router.register(r'plans', views.PlanViewSets, base_name='plans')

app_name = 'plan'
urlpatterns = router.urls

from rest_framework import routers
from .views import ReviewViewSet

router = routers.DefaultRouter()

router.register(r'book-review', ReviewViewSet, basename='book review')

urlpatterns = router.urls
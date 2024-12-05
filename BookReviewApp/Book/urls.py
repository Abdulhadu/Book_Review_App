from rest_framework import routers
from .views import BooksViewSet

router = routers.DefaultRouter()

router.register('book', BooksViewSet, basename='signup')

urlpatterns = router.urls
from rest_framework import routers
from .views import SignUpViewSet, LoginViewSet

router = routers.DefaultRouter()

router.register('SignUp', SignUpViewSet, basename='signup')
router.register('Login', LoginViewSet, basename='login')

urlpatterns = router.urls
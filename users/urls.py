from rest_framework import routers

from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls

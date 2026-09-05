from rest_framework import routers
from .views import TaskModelViewSet

app_name = "task_api_v1"


router = routers.DefaultRouter()
router.register("my-task", TaskModelViewSet, basename="task-api")

urlpatterns = router.urls

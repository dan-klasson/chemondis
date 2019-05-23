from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'interviewers', views.InterviewerViewSet)
router.register(r'interviews', views.InterviewViewSet)
router.register(r'slots', views.TimeSlotCreateViewSet)

timeslot_router = routers.NestedDefaultRouter(
    router,
    r'interviews',
    lookup='interview'
)
timeslot_router.register(
    r'slots',
    views.TimeSlotListViewSet,
    basename='timeslot'
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(timeslot_router.urls)),
]

from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import routers

from variant_explorer import views

router = routers.DefaultRouter()
router.register(r'variants', views.VariantViewSet)
router.register(r'genes', views.GeneViewSet)

urlpatterns = [
    path('', views.index_view, name='index'),
    path('variants/', views.variant_rows_view, name='variant_rows'),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

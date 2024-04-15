from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.organization_trends, name='index')
    # path('financial-records/', views.get_financial_records, name='get_financial_records'),
    # path('add-financial-record/', views.add_financial_record, name='add_financial_record'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
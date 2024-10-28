from django.urls import path
from photo.views import (GifArchiveLV, GifArchiveDV, LikeLV, 
                         SearchFormView, SubGifArchiveLV, ManagementLV,
                         GifArchiveDelV, GifArchiveUV, CategoryGifArchiveLV,
                         GifArchiveCV)

app_name = "photo"

urlpatterns = [
    path('', GifArchiveLV.as_view(), name="index"),
    path('<int:pk>/', GifArchiveDV.as_view(), name='photo_detail'),
    path('like/', LikeLV.as_view(), name='liked_gif'),
    path('search/', SearchFormView.as_view(), name='search'),
    path('create/', GifArchiveCV.as_view(), name='create_photo'),
    path('subscriptions/', SubGifArchiveLV.as_view(), name='sub_list'),
    path('management/', ManagementLV.as_view(), name='management'),
    path('<int:pk>/update', GifArchiveUV.as_view(), name='photo_update'),
    path('<int:pk>/delete', GifArchiveDelV.as_view(), name='photo_delete'),
    path('<str:category_name>/', CategoryGifArchiveLV.as_view(), name='photo_category_list'),
]
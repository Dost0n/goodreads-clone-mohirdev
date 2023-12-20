from django.urls import path
from api.views import BookReviewDetailAPIView, BookReviewListAPIView, BookReviewDetailUpdateDeleteAPIView, BookViewset
from rest_framework.routers import DefaultRouter

app_name = 'api'
router = DefaultRouter()


urlpatterns = [
    path('reviews/<int:id>/', BookReviewDetailAPIView.as_view(), name='review-detail' ),
    path('reviews/', BookReviewListAPIView.as_view(), name='book-review-list' )
]

router.register(r'bookreviews', BookViewset, basename='bookreviews')
urlpatterns += router.urls

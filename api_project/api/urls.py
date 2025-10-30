from django.urls import path, include
from .views import BookViewSet, BookList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'my-models', BookViewSet)

urlpatterns = [
	path('', include(router.urls)),
	path('books/', BookList.as_view(), name='book-list'),
]

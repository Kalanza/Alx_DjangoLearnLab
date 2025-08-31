
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class StandardResultsSetPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-created_at')
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
	pagination_class = StandardResultsSetPagination
	filter_backends = [filters.SearchFilter, DjangoFilterBackend]
	search_fields = ['title', 'content']
	filterset_fields = ['author']

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by('-created_at')
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
	pagination_class = StandardResultsSetPagination
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['post', 'author']

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

# Feed endpoint
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
	"""
	Return posts from users the current user follows, ordered by creation date.
	"""
	user = request.user
	following_users = user.following.all()
	posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
	paginator = StandardResultsSetPagination()
	result_page = paginator.paginate_queryset(posts, request)
	serializer = PostSerializer(result_page, many=True)
	return paginator.get_paginated_response(serializer.data)

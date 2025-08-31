
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from rest_framework import generics
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
# Like and Unlike views
class LikePostView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, pk):
		post = generics.get_object_or_404(Post, pk=pk)
		like, created = Like.objects.get_or_create(user=request.user, post=post)
		if not created:
			return Response({'detail': 'You have already liked this post.'}, status=400)
		# Create notification for post author
		if post.author != request.user:
			Notification.objects.create(
				recipient=post.author,
				actor=request.user,
				verb='liked your post',
				target=post,
			)
		return Response({'detail': 'Post liked.'}, status=200)

class UnlikePostView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, pk):
		post = generics.get_object_or_404(Post, pk=pk)
		try:
			like = Like.objects.get(user=request.user, post=post)
			like.delete()
			return Response({'detail': 'Post unliked.'}, status=200)
		except Like.DoesNotExist:
			return Response({'detail': 'You have not liked this post.'}, status=400)
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

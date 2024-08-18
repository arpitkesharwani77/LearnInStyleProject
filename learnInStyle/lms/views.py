from rest_framework import viewsets, generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer,LoginSerializer, RegisterSerializer

from rest_framework.permissions import AllowAny
# Define the User model
User = get_user_model()

# ViewSets for Courses and Lessons
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['instructor']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    permission_classes=[AllowAny]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course']
    ordering_fields = ['title']
    ordering = ['title']
    permission_classes=[AllowAny]
    
# Register new users
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Login user and return JWT token
class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Logout user (client-side token invalidation)
class LogoutUserView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        # Simply inform the client to discard the token
        return Response({'detail': 'Successfully logged out'}, status=status.HTTP_204_NO_CONTENT)

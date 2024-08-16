from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Course
from .serializers import CourseSerializer

# List/Create Courses
class CourseListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve/Update/Delete Course
class CourseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = Course.objects.get(pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#--------------enrollment----------------#


from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(user=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_instructor:
            return Response({"detail": "You are not authorized to create a course."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        enrollment = Enrollment.objects.get(pk=pk, user=request.user)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def put(self, request, pk):
        enrollment = Enrollment.objects.get(pk=pk, user=request.user)
        serializer = EnrollmentSerializer(enrollment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# Adding a view that allows instructors to view, update, and delete only the courses they created.

class InstructorCourseListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_instructor:
            return Response({"detail": "You are not authorized to view this page."}, status=status.HTTP_403_FORBIDDEN)

        courses = Course.objects.filter(instructor=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

#Implementing a search functionality that allows users to filter courses by title, description, or category.
class CourseSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('query', None)
        if query:
            courses = Course.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
            )
        else:
            courses = Course.objects.all()

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

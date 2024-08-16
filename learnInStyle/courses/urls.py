from django.urls import path
from .views import (CourseListCreateView,
                 CourseDetailView,
                 EnrollmentListCreateView,
                 EnrollmentDetailView,
                 InstructorCourseListView,
                 CourseSearchView,
                 )
urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list'),
    
    path('enrollments/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('instructor/courses/', InstructorCourseListView.as_view(), name='instructor-course-list'),
     path('courses/search/', CourseSearchView.as_view(), name='course-search'),
]



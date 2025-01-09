import json
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Course, CourseRating, Enrollment
from utils.emails import send_course_enrollment_email

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_rated'] = CourseRating.objects.filter(
                user=self.request.user,
                course=self.object
            ).exists()
            context['is_enrolled'] = Enrollment.objects.filter(
                user=self.request.user,
                course=self.object,
                paid=True
            ).exists()
        return context

@login_required
@require_POST
def rate_course(request):
    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')
        rating_value = int(data.get('rating'))
        
        course = Course.objects.get(id=course_id)
        
        rating, created = CourseRating.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={'rating': rating_value}
        )
        
        return JsonResponse({
            'success': True,
            'average_rating': course.average_rating,
            'rating_count': course.ratings.count()
        })
        
    except Course.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Course not found'
        }, status=404)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({
            'success': False,
            'error': 'Invalid rating data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if Enrollment.objects.filter(user=request.user, course=course, paid=True).exists():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    if course.price > 0:
        return redirect('payments:payment_page', payment_type='course', item_id=course_id)
    else:
        Enrollment.objects.create(user=request.user, course=course, paid=True)
        # Send enrollment confirmation email
        send_course_enrollment_email(request.user, course)
        messages.success(request, 'You have successfully enrolled in the course.')
        return redirect('courses:course_detail', slug=course.slug)

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user, paid=True).select_related('course')
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})
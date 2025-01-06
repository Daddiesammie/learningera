import json
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Course, CourseRating

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

from django.conf import settings

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
        
        # Add Flutterwave public key to context
        context['flw_public_key'] = settings.FLW_PUBLIC_KEY
        
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
        
        # Calculate fresh ratings
        return JsonResponse({
            'success': True,
            'average_rating': course.average_rating,
            'rating_count': course.ratings.count()
        })
        
    except Course.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Course not found'
        })
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({
            'success': False,
            'error': 'Invalid rating data'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

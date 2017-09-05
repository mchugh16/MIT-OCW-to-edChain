import json

from django.http import JsonResponse
from django.views import View
from django.http import HttpResponseNotAllowed

from api.models import Course



class Index(View):

	def _to_json(self, courses):
		return {
			'courses': [{
				'pk': course.pk,
				'course_name': course.course_name,
				'instructors' : course.instructors,
				'version' : course.version,
				'level' : course.level,
				'chp_image' : course.chp_image,
				'chp_image_caption' : course.chp_image_caption,
				'course_description' : course.course_description,
				'course_features' : course.course_features
			} for course in courses]
		}

	
	def get(self, request):
		#later implement sorting (so order by version, filter by level, order by pk,course_name
		# current_userprofile = UserProfile.objects.get(token = token)
 
		courses = Course.objects.all()[:30]

		return JsonResponse(self._to_json(courses))


class CourseDetail(View):
	def serialize_course(self, course):
		return {
				'pk': course.pk,
				'course_name': course.course_name,
				'instructors' : course.instructors,
				'version' : course.version,
				'level' : course.level,
				'chp_image' : course.chp_image,
				'chp_image_caption' : course.chp_image_caption,
				'course_description' : course.course_description,
				'course_features' : course.course_features
			}


	def get(self, request, pk):
		course = Course.objects.get(pk=pk)
		data = {'course' : self.serialize_course(course)}
		return JsonResponse(data)


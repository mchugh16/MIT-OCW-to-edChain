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
				'title': post.title,
				'content': post.content,
				'user': post.user.username,
				'created_at': unix_timezone(post.created_at),
			} for post in posts]
		}

	
	def get(self, request, token=None, pk=None):
		# current_userprofile = UserProfile.objects.get(token = token)

		if pk:
			posts = [Post.objects.get(pk=pk)]
		elif token:
			current_user = User.objects.get(userprofile__token=token)
			posts = Post.objects.filter(user = current_user)
			
		else:
			posts = Post.objects.all().order_by('created_at')[:10]
		
		request.session.get('user_id', 'no_user')

		return JsonResponse(self._to_json(posts))


class CourseDetail(View):
	
	def get(self, request, pk, token):
		todo = ToDo.objects.get(pk=pk, user__userprofile__token=token)
		data = {'todo' : self.serialize_todo(todo)}
		return JsonResponse(data)


from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View

class Index(View):
	template = 'ui/index.html'
	
	def get(self,request):
		return render(request, self.template)


class CourseHomePage(View):
	template = 'ui/chp.html'

	def get(self, request):
		return render(request, self.template)



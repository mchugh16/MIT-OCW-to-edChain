from django.db import models

class Course(models.Model):
	course_name = models.TextField()
	instructors = models.TextField() 
	version = models.CharField(max_length=50) 
	level = models.CharField(max_length=50)
	chp_image = models.ImageField()
	chp_image_caption = models.TextField() 
	course_description = models.TextField() 
	course_features = models.TextField() 


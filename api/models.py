from django.db import models

class Course(models.Model):
	course_name = models.TextField()
	instructors = models.TextField() #not required 
	version = models.CharField(max_length=50) #not required
	level = models.CharField(max_length=50)
	#course home page = chp
	chp_image = models.ImageField()
	chp_image_caption = models.TextField() #not required
	course_description = models.TextField() #not required
	course_features = models.TextField() 


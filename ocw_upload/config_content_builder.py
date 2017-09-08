import os
import zipfile
import config


class ConfigBuilder():
	"""
	Construct and assemble parts of the product by implementing the
	Builder interface.
	Define and keep track of the representation it creates.
	Provide an interface for retrieving the product.

	
	"""
	def __init__(self):
		self._product = Product()

	def unzip(self, zip_name, linknum):

		cwd = os.getcwd()
		zip_path = os.path.join(cwd, zip_name)

		courses_dir = "../courses/" + linknum


		with zipfile.ZipFile(zip_path, 'r') as z:
			z.extractall(courses_dir)


	# def build_course(self, pk, course_name, instructors, version, level, chp_image_source, chp_image_caption, course_description, course_features):
	# 	"""
	# 	Build dictionary of course information, pass to course serializer.
	# 	Args:
	# 		pk - primary key
	# 		course_name - name of course
	# 		instructors - names of instructors
	# 		version - semester and year that course was originally taught in
	# 		level - undergraduate, graduate, etc.
	# 		chp_image_source - (source of) main image found on the course's homepage
	# 		chp_image_caption - caption of the main image found on the course's homepage
	# 		course_description - course description
	# 		course_features - sections into which the course is divided
	# 	"""
	# 	print(pk)
	# 	course_attributes = {
	# 		"course_name" : course_name,
	# 		"instructors" : instructors,
	# 		"version" : version,
	# 		"level" : level,
	# 		"chp_image" : chp_image_source,
	# 		"chp_image_caption" : chp_image_caption,
	# 		"course_description" : course_description,
	# 		"course_features" : course_features
	# 	}
	# 	self.serialize_course(pk, course_attributes)

	# def serialize_course(self, pk, course_attributes):
	# 	"""
	# 	Serialize course (so that format is like that of a fixture in JSON).
		
	# 	Args:
	# 		pk - primary key of the course
	# 		course_attributes - attributes of course with attribute names as
	# 							keys and corresponding data as values
	# 	"""
	# 	serialized_course = {

	# 			"model" : "api.course",
	# 			"pk" : pk,
	# 			"fields" : course_attributes
	# 		}
	# 	self.add_course(serialized_course)

	# def add_course(self, course):
	# 	"""
	# 	Add course to list of courses.

	# 	Args: 
	# 		course - dictionary with model, pk, fields as keys 
	# 	"""

	# 	self._product.courses.append(course)


	# def get_product(self):
	# 	self._product.courses_to_file()



class Product:
	def __init__(self):
		# self.outfile = outfile
		# self.courses = []
		pass


	# def courses_to_file(self):
	# 	"""
	# 	Write serialized courses to file.
	# 	"""
	# 	with open(self.outfile, 'w') as self.outfile:
	# 		json.dump(self.courses, self.outfile)






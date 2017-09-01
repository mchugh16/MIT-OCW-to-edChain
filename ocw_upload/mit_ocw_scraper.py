import requests
import bs4
import re

from fixture_builder import FixtureBuilder

class Director:

	def __init__(self, builder, root_url):
		self.root_url = root_url
		
		self._builder = builder
		self.mit_ocw_scraper= MITOCWScraper(self._builder, self.root_url)

	def construct(self):
		"""
		Instruct reader to process input and pass specified data 
		to the builder for the product to be constructed.
		"""
		self.mit_ocw_scraper.process()

class MITOCWScraper:
	#use vars and property decorator - convert to reader builder format

	def __init__(self, builder, root_url):
		self._builder = builder
		self.root_url = root_url
		self.pk = 0

	def process(self):
		#get links to all course homepages
		course_page_urls = self.get_course_page_urls()

		#find courses licensed under Creative Commons, pass their
		#information to the builder for construction of product
		self.get_allowed_course_page_urls(course_page_urls)

		#get product
		product = self.get_product()


	def get_course_page_urls(self):
		"""
		Scrape MIT OCW "View All Courses" page for links to all courses.

		Returns: List of links to all courses.
		"""
		view_courses_url = '/courses/?utm_source=ocw-megamenu&utm_medium=link&utm_campaign=mclstudy'
		index_url = self.root_url + view_courses_url
		response = requests.get(index_url)
		soup = bs4.BeautifulSoup(response.content)
		course_links_set = set()
		for link in soup.find_all("a", class_="preview", rel="coursePreview"):
			if "resources" not in link.get("href"):
				course_links_set.add(link.get("href"))

		return list(course_links_set)


	def get_allowed_course_page_urls(self, course_page_urls):
		"""
		Check license of each course and get links to courses
		protected under the creative commons license. Pass link
		and the soupified homepage of the course to course info getter.

		Args: 
			course_page_urls - list of relative links to all courses
							 	on MIT OCW's "View All Courses" page 

		"""

		for course_url in course_page_urls:
			index_url = self.root_url + course_url
			response = requests.get(index_url)
			soup = bs4.BeautifulSoup(response.content)
			cc_citation = soup.find("a", href = "https://creativecommons.org/licenses/by-nc-sa/4.0/")

			if cc_citation:
				self.get_course_info(course_url, soup)


	def get_course_info(self, course_url, soup):
		"""
		Set attributes of course (including the course's name, instructors,
		version (semester and year), level (undergraduate, graduate, etc),
		description, and features as well as the course homepage's main image
		and this image's caption) and pass attributes to builder.

		Args: 
			course_url - relative link to course
			soup - soupified homepage of course

		"""

		#set name of course
		course_name = self.get_course_name(soup)

		#set instructor's name, version (semester and year), level (undergraduate, graduate, etc.)
		course_info_div = soup.find("div", id="course_info")
		instructors = self.get_instructors(course_info_div)
		version = self.get_version(course_info_div)
		level = self.get_course_level(course_info_div)

		#set link to course homepage image and caption of image
		image_div = soup.find("div", id="chpImage")
		chp_image = self.get_chp_image(image_div)
		chp_image_caption = self.get_chp_image_caption(image_div)

		#set description of course
		description = self.get_course_description(soup)

		#set features of course (found on left nav bar)
		features = self.get_course_features(soup)

		#get primary key
		self.pk += 1

		#pass attributes to builder 
		self._builder.build_course(self.pk, course_name, instructors, version, level, chp_image, chp_image_caption, description, features)



	def get_course_name(self, soup):
		"""
		Get the name of a specified course.

		Args: 
			soup - soupified homepage of course

		Returns: The course name.
		"""
		course_name_div = soup.find("div", id="course_title")
		course_name = course_name_div.find("h1", itemprop = "name").get_text()
		return course_name


	def get_instructors(self, course_info_div):
		"""
		Get the names of instructors of a specified course.

		Args:
			course_info_div - "html division" (container with course info)
		"""
		instructor_div = course_info_div.find("p", itemprop="author")
		if instructor_div:
			instructor = instructor_div.get_text()
		elif instructor_div == None:
			instructor = "Not Available"

		return instructor

	def get_version(self, course_info_div):
		"""
		Get the version (semester and year) of a specified course.

		Args:
			course_info_div - "html division" (container with course info)
		"""
		version_div = course_info_div.find("p", itemprop = "startDate")
		if version_div:
			version = version_div.get_text()
		elif version_div == None:
			version = "Not Available"

		return version

	def get_course_level(self, course_info_div):
		"""
		Get the level (undergraduate, graduate, etc.) of a specified course.

		Args:
			course_info_div - "html division" (container with course info)
		"""
		level = course_info_div.find("p", itemprop = "typicalAgeRange").get_text()

		return level

	def get_chp_image(self, image_div):
		"""
		Get the explicit link to the image on a specified course's homepage.

		Args:
			image_div - "html division" (container with homepage image and caption)
		"""
		image_url = image_div.find("img").get("src")
		chp_image_source = self.root_url + image_url

		return chp_image_source

	def get_chp_image_caption(self, image_div):
		"""
		Get the caption of the image on a specified course's homepage.

		Args:
			image_div - "html division" (container with homepage image and caption)
		"""
		caption_div = image_div.find("p")
		if caption_div:
			chp_image_caption = caption_div.get_text()
		elif caption_div == None:
			chp_image_caption = ""

		return chp_image_caption

	def get_course_description(self, soup):
		"""
		Get the description of a specified course.

		Args: 
			soup - soupified homepage of course
		"""
		course_description_div = soup.find("div", id="description", itemprop="description")
		course_description_div_div = course_description_div.find("p")
		if course_description_div_div:
			course_description = course_description_div_div.get_text()
		elif course_description_div_div == None:
			course_description = ""

		return course_description

	def get_course_features(self, soup):
		"""
		Get the features (the divisions into which a course is organized) for a specified course.

		Args: 
			soup - soupified homepage of course
		"""
		features = []
		left_nav_bar_div = soup.find("div", id="left")
		list_features = left_nav_bar_div.find("ul")
		for feature in list_features.find_all("a"):
			feature_text = feature.get_text()
			clean_feature_text = re.sub('\s+',' ', feature_text)
			features.append(clean_feature_text.strip())

		course_features = features

		return course_features

	def get_product(self):
		self._builder.get_product()





def main():
	root_url = "https://ocw.mit.edu"
	outfile = "mit_ocw_CC_courses.json"

	director = Director(FixtureBuilder(outfile), root_url)
	director.construct()

if __name__ == "__main__":
	main()
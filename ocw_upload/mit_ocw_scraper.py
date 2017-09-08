import requests
import bs4
import re
import urllib.request, urllib.parse, urllib.error

from fixture_builder import FixtureBuilder
from config_content_builder import ConfigBuilder

class Director:

	def __init__(self, fixture_builder, config_builder, root_url):
		self.root_url = root_url
		
		self._fixture_builder = fixture_builder
		self._config_builder = config_builder
		self.mit_ocw_scraper= MITOCWScraper(self._fixture_builder, self._config_builder, self.root_url)

	def construct(self):
		"""
		Instruct reader to process input and pass specified data 
		to the builder for the product to be constructed.
		"""
		self.mit_ocw_scraper.process()

class MITOCWScraper:
	#use vars and property decorator - convert to reader builder format

	def __init__(self, fixture_builder, config_builder, root_url):
		self._fixture_builder = fixture_builder
		self._config_builder = config_builder
		self.root_url = root_url
		self.pk = 0
		self.content_download_urls = []

	def process(self):
		#get links to all course homepages
		course_page_urls = self.get_course_page_urls()

		#find courses licensed under Creative Commons, pass their
		#information to the builder for construction of product
		self.get_allowed_course_page_urls(course_page_urls)

		#get product
		product = self.get_product()

		content_urls = self.get_course_content()
		self.download_course_content(content_urls)



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
		and the soupified homepage of the course to course info getter 
		AND course download url getter.

		Args: 
			course_page_urls - list of relative links to all courses
								on MIT OCW's "View All Courses" page 

		"""

		for course_url in course_page_urls[0:3]:
			index_url = self.root_url + course_url
			response = requests.get(index_url)
			soup = bs4.BeautifulSoup(response.content)
			cc_citation = soup.find("a", href = "https://creativecommons.org/licenses/by-nc-sa/4.0/")

			if cc_citation:
				print(course_url)
				# self.get_course_info(soup)
				self.get_course_download_urls(soup)

	def get_course_info(self, soup):
		"""
		Set attributes of course (including the course's name, instructors,
		version (semester and year), level (undergraduate, graduate, etc),
		description, and features as well as the course homepage's main image
		and this image's caption) and pass attributes to builder.

		Args: 
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
		self._fixture_builder.build_course(self.pk, course_name, instructors, version, level, chp_image, chp_image_caption, description, features)



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

	def get_course_download_urls(self, soup):
		"""
		Get links to download pages for each course.

		Args:
			soup - soupified homepage of course
		"""
		left_nav_bar_div = soup.find("div", id="left")
		list_features = left_nav_bar_div.find("ul")
		for feature in list_features.find_all("a"):
			if feature.get_text() == "Download Course Materials":
				feature_link = feature.get("href")
				full_link = self.root_url + feature_link
				self.content_download_urls.append(full_link)

	def get_course_content(self):
		"""
		Get download links for each course's content.

		Returns: List of download links
		"""
		content_urls = []
		for link in self.content_download_urls:
			response = requests.get(link)
			soup = bs4.BeautifulSoup(response.content)
			course_wrapper = soup.find("div", id="course_wrapper")
			download_page_info = course_wrapper.find("main", id="course_inner_chp")
			download_div = download_page_info.find("div", class_="downloadLink")
			download_link_a = download_div.find("a", class_="downloadNowButton")
			download_link = download_link_a.get("href")
			full_link = self.root_url + download_link
			content_urls.append(full_link)

		return content_urls

	def download_course_content(self, content_links):
		"""
		Download content folders for every course, pass zip file to config builder.
		
		Args:
			content_links - links to zipped content files

		"""

		link_num = 0
		for link in content_links:
			filename = "course" + str(link_num) + ".zip"
			urllib.request.urlretrieve(link, filename)
			f = urllib.request.urlopen(link)
			data = f.read()

			filename2 = "../courses/" + filename
			with open(filename2, "wb") as zip_code:
				zip_code.write(data)

			self._config_builder.unzip(filename2, link_num)

			link_num += 1




	def get_product(self):
		self._fixture_builder.get_product()





def main():
	root_url = "https://ocw.mit.edu"
	outfile = "mit_ocw_CC_courses.json"

	director = Director(FixtureBuilder(outfile), ConfigBuilder(), root_url)
	director.construct()

if __name__ == "__main__":
	main()
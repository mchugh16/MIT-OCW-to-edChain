import requests
import bs4
import re
import json

root_url = "https://ocw.mit.edu"



def get_course_page_urls():
	"""
	Scrape MIT OCW "View All Courses" page for links to all courses.

	Returns: List of links to all courses.
	"""
	index_url = root_url + '/courses/?utm_source=ocw-megamenu&utm_medium=link&utm_campaign=mclstudy'
	response = requests.get(index_url)
	soup = bs4.BeautifulSoup(response.content)
	course_links_set = set()
	for link in soup.find_all("a", class_="preview", rel="coursePreview"):
		if "resources" not in link.get("href"):
			course_links_set.add(link.get("href"))

	return list(course_links_set)




def get_allowed_course_page_urls(course_page_urls, dict_of_courses):
	"""
	Check license of each course and get links of courses with creative commons license.

	Returns: Dictionary with links to courses protected under creative commons as keys 
			and dictionary with attribute names as values
	"""

	for url in course_page_urls:
		print(url)
		index_url = root_url + url
		response = requests.get(index_url)
		soup = bs4.BeautifulSoup(response.content)
		citation = soup.find("a", href = "https://creativecommons.org/licenses/by-nc-sa/4.0/")

		if citation:
			course_info = get_course_info(url, soup)
			dict_of_courses.update(course_info)

	return dict_of_courses



def get_course_info(course_url, soup):
	full_course_url = root_url + course_url

	#get course name
	course_name_div = soup.find("div", id="course_title")
	course_name = course_name_div.find("h1", itemprop = "name").get_text()

	#get instructor's name, version (semester and year), level (undergraduate, graduate, etc.)
	course_info_div = soup.find("div", id="course_info")
	instructor_div = course_info_div.find("p", itemprop="author")
	if instructor_div:
		instructor = instructor_div.get_text()
	elif instructor_div == None:
		instructor = None
	version_div = course_info_div.find("p", itemprop = "startDate")
	if version_div:
		version = version_div.get_text()
	elif version_div == None:
		version = None


	level = course_info_div.find("p", itemprop = "typicalAgeRange").get_text()

	#get link to course homepage image and caption of image
	image_div = soup.find("div", id="chpImage")
	image_url = image_div.find("img").get("src")
	image_source = root_url + image_url
	caption_div = image_div.find("p")
	if caption_div:
		caption = caption_div.get_text()
	elif caption_div == None:
		caption = None

	#get description of course
	course_description_div = soup.find("div", id="description", itemprop="description")
	course_description_div_div = course_description_div.find("p")
	if course_description_div_div:
		course_description = course_description_div_div.get_text()
	elif course_description_div_div == None:
		course_description = None

	features = []
	left_nav_bar_div = soup.find("div", id="left")
	list_features = left_nav_bar_div.find("ul")
	for feature in list_features.find_all("a"):
		feature_text = feature.get_text()
		clean_feature_text = re.sub('\s+',' ', feature_text)
		features.append(clean_feature_text.strip())


	attribute_dict = {
				"Course Name" : course_name,
				"Instructor(s)" : instructor,
				"Version" : version,
				"Level" : level,
				"Homepage Image" : image_source,
				"Image Caption" : caption,
				"Course Description" : course_description,
				"Course Features" : features
		}

	course_dict = {
		full_course_url : attribute_dict
		}

	return course_dict

def courses_to_file(course_dict):
	with open("mit_ocw_CC_courses.json", 'w') as outfile:
		json.dump(course_dict, outfile)

	


def main():

	courses = {}
	course_page_urls = get_course_page_urls()
	allowed_courses_dict = (get_allowed_course_page_urls(course_page_urls, courses))
	courses_to_file(allowed_courses_dict)





if __name__ == "__main__":
	main()
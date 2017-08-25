import os
# import zipfile
# import fileinput

import config

# zip_name = '18-06sc-fall-2011.zip'

# def unzip(zip_name):

# 	cwd = os.getcwd()
# 	zip_path = os.path.join(cwd, zip_name)


# 	with zipfile.ZipFile(zip_path, 'r') as z:
# 	    z.extractall(cwd)

def traverse_dir(root_dir):
	for dir_name, sub_dir_list, file_list in os.walk(root_dir):
		for filename in file_list:
			file_path = os.path.join(dir_name, filename)

			with open(file_path, "r") as file:
				print(file_path)
				print(file.read())
				# #file to list 
				# filelist = [] 
				# for line in file:
				# 	file_list += line
				# print(file_list)
		#create full path name to each file, print text 





# os.listdir(dir_path)
#	dir_path = os.path.join(cwd, zip_dir_name)




def main():
	for course_folder in config.COURSE_FOLDERS:
		dir_name = os.path.join(config.COURSES_DIR, course_folder)
		traverse_dir(dir_name)


if __name__ == '__main__':
	main()
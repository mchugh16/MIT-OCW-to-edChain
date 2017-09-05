# MIT Open Courseware to edChain

Publish MIT Open Courseware to edChain nodes by crawling the MIT's OCW site 
and converting XML specifications of each course to json schemas using core descriptors 
from schema.org.


## Getting Started

To get a copy of the project up and running on your local machine for development and testing purposes, please see below.

To generate schemas for courses..
Download and unzip a course's content from the ocw site and add its path to COURSE_FOLDERS
in the config file located in the ocw_upload folder. By running read_imsmanifest.py, every imsmanifest file 
included in the course's content folder will be parsed 
and important information, including the sections into which the course is organized,
paths to the course's resources (but not the actual data for those resources), and other specifications 
of the course, will be written to a json file as specified in build_schema.py. 
The exact schema used to organize each course's content can be 
found in schema_dict.py


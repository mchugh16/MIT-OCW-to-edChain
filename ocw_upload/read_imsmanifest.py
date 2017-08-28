import xml.etree.ElementTree as ElementTree
import xmltodict
import os

import config
from build_schema import SchemaBuilder


class Director:

	def __init__(self, builder, config, course_folder):
		self.full_path = os.path.join(config.COURSES_DIR, course_folder)
		self.file_full_path = os.path.join(self.full_path, config.IMS_MANIFEST)
		
		self._builder = builder
		self.imsmanifest_reader = IMSManifestReader(self._builder, self.file_full_path)


	def construct(self):
		self.imsmanifest_reader.process()




class IMSManifestReader:

	XMLNAMESPACES = {
			"default": "http://www.imsglobal.org/xsd/imscp_v1p1",
			"xsi" : "http://www.w3.org/2001/XMLSchema-instance",
			"adlcp" : "http://www.adlnet.org/xsd/adlcp_rootv1p2",
			"cwsp" : "http://www.dspace.org/xmlns/cwspace_imscp",
			"ocw" : "https://ocw.mit.edu/xmlns/ocw_imscp",
			"lom" : "https://ocw.mit.edu/xmlns/LOM"
		}

	def __init__(self, builder, imsmanifest):
		self._builder = builder
		self.imsmanifest = imsmanifest


	def process(self):
		root = self.find_imsmanifest_root(self.imsmanifest)
		item_parent_map = self.map_parents_items(self.imsmanifest)

		organizations = self.read_organizations(root, item_parent_map)
		resources = self.read_resources(root)
		metadata = self.read_subject_metadata(root)
		course_name = self.read_course_name(root)
		course_code = self.read_course_code(root)
		course_version = self.read_version(root)
		course_instructor = self.read_instructor(root)

		product = self._builder.get_product()
		


	def find_imsmanifest_root(self, imsmanifest):
		"""
		Read imsmanifest.xml into an element tree, find root.

		Args: imsmanifest - full path for imsmanifest file

		Returns: Root element of imsmanifest document's tree

		"""
		tree = ElementTree.parse(imsmanifest)
		root = tree.getroot()
		root_attribs = root.attrib
		return root

	def map_parents_items(self, imsmanifest):
		"""
		Map items to organization parent elements from 
		imsmanifest document tree.

		Args: imsmanifest - full path for imsmanifest file

		Returns: Dictionary with item ids as keys 
				and parent ids as values
		"""

		tree = ElementTree.parse(imsmanifest)
		item_parent_map = {}
		for parent in tree.iter():
			for child in parent:
				if "item" in child.tag:
					item_parent_map[child.attrib["identifier"]] = parent.attrib["identifier"]

		return item_parent_map


	def read_organizations(self, root, item_parent_map):
		"""
		Get identifier, title, items of each organization
		and pass these attributes to organization builder.

		Args: 	
			root - root of entire imsmanifest's document tree 
				   which is an instance of the ElementTree wrapper class 
			item_parent_map - dictionary with item ids as keys
								 and their parents' ids as values 

		"""

		organizations_element = root.find("default:organizations", self.XMLNAMESPACES)
		organization_elements = organizations_element.findall("default:organization", self.XMLNAMESPACES)
		for organization in organization_elements:
			org_id = organization.attrib["identifier"]
			title = organization.find("default:title", self.XMLNAMESPACES).text
			self._builder.add_organization(org_id, title)
			self.read_items(org_id, organization, item_parent_map)

	def read_items(self, org_id, parent_node, item_parent_map):
		"""
		Get identifier, title, parent item identifier,
		and other attributes of each item, pass these
		features to item builder

		Args: org_id - parent organization id
			  parent_node - parent of item (organization or item)
			  item_parent_map - dictionary with item ids as keys and their parents' 
								ids as values

		"""
		item_elements = parent_node.findall("default:item", self.XMLNAMESPACES)

		for item in item_elements:
			item_identifier = item.attrib["identifier"]

			item_info = {}
			for key, value in item.attrib.items():
				if key != "identifier":
					item_info[key] = value

			item_info["title"] = item.find("default:title", self.XMLNAMESPACES).text
			item_info["parent identifier"] = item_parent_map[str(item.attrib["identifier"])]

			self._builder.add_item(item_identifier, item_info, org_id)

			# #check for subitems
			if item.attrib["identifier"] in item_parent_map.values():
				self.read_items(org_id, item, item_parent_map)



	def read_resources(self, root):
		"""
		Get identifier, type, href, dependencies,
		metadata, files of each resource
		and pass these attributes to resource builder.

		Args: 	
			root - root of entire imsmanifest's document tree 
				   which is an instance of the ElementTree wrapper class 
		"""

		resources_element = root.find("default:resources", self.XMLNAMESPACES)
		resource_elements = resources_element.findall("default:resource", self.XMLNAMESPACES)

		for resource in resource_elements:
			resource_id = resource.attrib["identifier"]

			#type, href are attributes of each resource element
			resource_info = {}
			for key, value in resource.attrib.items():
				if key != "identifier":
					resource_info[key] = value

			self._builder.add_resource(resource_id, resource_info)

		# 	#check for dependencies
			dependency = resource.find("default:dependency", self.XMLNAMESPACES)
			if dependency != None:
				self.read_dependencies(resource_id, resource)

		# 	#check for files
			file = resource.find("default:file", self.XMLNAMESPACES)
			if file != None:
				self.read_files(resource_id, resource)

		# 	#check for metadata
			metadata = resource.find("default:metadata", self.XMLNAMESPACES)
			if metadata != None:
				self.read_document_metadata(resource_id, resource)



	def read_dependencies(self, resource_identifier, resource_node):
		"""
		Get all identifier references of dependencies for a given resource,
		pass resource_identifier and list of dependency identifierrefs to
		builder

		Args: 
			resource_identifier - identifier of parent resource
			resource_node - resource object element to be searched for 
							dependency subelements
		"""
		dependencies = []
		dependency_elements = resource_node.findall("default:dependency", self.XMLNAMESPACES)

		for dependency in dependency_elements:
			identifier_ref = dependency.attrib["identifierref"]
			dependencies.append(identifier_ref)

		self._builder.add_dependencies(resource_identifier, dependencies)


	def read_files(self, resource_identifier, resource_node):
		"""
		Get all hrefs of files for a given resource,
		pass resource_identifier and list of file hrefs to builder

		Args: 
			resource_identifier - identifier of parent resource
			resource_node - resource object element to be searched for 
							dependency subelements
		"""
		files = []

		file_elements = resource_node.findall("default:file", self.XMLNAMESPACES)

		for file in file_elements:
			href = file.attrib["href"]
			files.append(href)

		self._builder.add_files(resource_identifier, files)


	def read_document_metadata(self, resource_identifier, resource):
		"""
		Get metadata for a specified resource and pass to doc metadata builder

		Args: 
			resource_identifier - identifier of parent resource
			resource_node - resource object element to be searched for 
							dependency subelements
		"""
		metadata_element = resource.find("default:metadata", self.XMLNAMESPACES)

		metadata = {}
		namespace = self.XMLNAMESPACES["adlcp"] + "/location"
		metadata = metadata_element.find("adlcp:location", self.XMLNAMESPACES).text

		self._builder.add_doc_metadata(resource_identifier, namespace, metadata)


	def read_subject_metadata(self, root):
		"""
		Get subject level metadata element object
		 and pass to subject metadata builder. 

		Args: root - root of entire imsmanifest's document tree 
				     which is an instance of the ElementTree wrapper class 
		"""
		metadata_element = root.find("default:metadata", self.XMLNAMESPACES)
		stringified_metadata = ElementTree.tostring(metadata_element, encoding="unicode")
		metadata_dict = xmltodict.parse(stringified_metadata, process_namespaces=True)
		
		self._builder.add_subject_metadata(metadata_dict)

	def read_course_name(self, root):
		"""
		Get the course name from metadata and pass it to metadata schema builder

		Args: root - root of entire imsmanifest's document tree 
				     which is an instance of the ElementTree wrapper class 
		"""

		metadata_element = root.find("default:metadata", self.XMLNAMESPACES)
		general_info_element = metadata_element.find("lom:general", self.XMLNAMESPACES)
		title_element = general_info_element.find("lom:title", self.XMLNAMESPACES)
		course_name = title_element.find("lom:string", self.XMLNAMESPACES).text

		self._builder.add_schema_metadata("name", course_name)

	def read_course_code(self, root):
		"""
		Get the course code from metadata and pass it to metadata schema builder

		Args: root - root of entire imsmanifest's document tree 
				     which is an instance of the ElementTree wrapper class 
		"""
		metadata_element = root.find("default:metadata", self.XMLNAMESPACES)
		general_info_element = metadata_element.find("lom:general", self.XMLNAMESPACES)
		identifier_element = general_info_element.find("lom:identifier", self.XMLNAMESPACES)
		course_code = identifier_element.find("lom:entry", self.XMLNAMESPACES).text

		self._builder.add_schema_metadata("courseCode", course_code)

	def read_version(self, root):
		"""
		Get the version of the course from metadata 
		and pass it to metadata schema builder

		Args: root - root of entire imsmanifest's document tree 
				     which is an instance of the ElementTree wrapper class 
		"""
		metadata_element = root.find("default:metadata", self.XMLNAMESPACES)
		lifecycle_element = metadata_element.find("lom:lifecycle", self.XMLNAMESPACES)
		version_element = lifecycle_element.find("lom:version", self.XMLNAMESPACES)
		course_version = version_element.find("lom:string", self.XMLNAMESPACES).text

		self._builder.add_schema_metadata("version", course_version)

	def read_instructor(self, root):
		"""
		Get the instructor of the course from metadata 
		and pass it to metadata schema builder

		Args: root - root of entire imsmanifest's document tree 
				     which is an instance of the ElementTree wrapper class 
		"""
		metadata_element = root.find("default:metadata", self.XMLNAMESPACES)
		lifecycle_element = metadata_element.find("lom:lifecycle", self.XMLNAMESPACES)
		contribute_element = lifecycle_element.find("lom:contribute", self.XMLNAMESPACES)
		author = contribute_element.find("lom:entity", self.XMLNAMESPACES).text


		self._builder.add_schema_metadata("Instructor", author)



def main():
	for course_folder in config.COURSE_FOLDERS:

		director = Director(SchemaBuilder(), config, course_folder)
		director.construct()

if __name__ == '__main__':
	main()
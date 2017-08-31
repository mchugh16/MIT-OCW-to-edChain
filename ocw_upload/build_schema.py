import schema_dict 
import json

class SchemaBuilder():
	"""
	Construct and assemble parts of the product by implementing the
	Builder interface.
	Define and keep track of the representation it creates.
	Provide an interface for retrieving the product.

	
	"""
	def __init__(self):
		self._product = Product()


	def add_organization(self, org_identifier, org_title):

		"""
		Add to dictionary of organizations with the organization's
		identifier as the key and a dictionary as the value 
		(with 'title' and 'items' as keys of this dictionary)

		Args:
			org_identifier - identifier of organization provided by imsmanifest
			org_title - title of organization specified in imsmanifest
		"""
		info = {
			"title" : org_title,
			"items" : {}
		}

		self._product.organizations[org_identifier] = info

	def add_item(self, item_identifier, item_info, org_id):

		"""
		Add item and its associated info to 'items' within
		its parent organization in the dictionary of 
		organizations.

		Args:
			item_identifier - identifier of item provided by imsmanifest
			item_info - other info (the item's title, parent identifier, 
						other attributes such as an identifierref, 
						a sectionTemplateTag, etc.) 
			org_id - parent organization of item
		"""

		item_dict = {}
		item_dict[item_identifier] = item_info
		self._product.organizations[org_id]['items'].update(item_dict)

	def add_resource(self, resource_identifier, resource_info):
		"""
		Add a resource to dictionary of resources 
		with the resource's identifier as the key
		and any other attributes as values.
		
		Args:
			resource_identifier - identifier of resource provided by imsmanifest
			resource_info - dict of other info (including the resource's type, hrefs)
							with the name of attributes as keys 
							and associated info as values

		"""
		self._product.resources[resource_identifier] = resource_info

	def add_dependencies(self, resource_identifier, dependencies):
		"""
		Add key-value pair of dependencies of specified resource 
		to resource dictionary.

		Args:
			resource_identifier : identifier of resource provided by imsmanifest
			dependencies: list of identifierrefs for dependencies of specified resource
		"""
		self._product.resources[resource_identifier]["dependencies"] = dependencies

	def add_files(self, resource_identifier, files):
		"""
		Add key-value pair of files for specified resource 
		to resource dictionary ("files" as key and list of
		hrefs of files as the value)

		Args:
			resource_identifier : identifier of resource provided by imsmanifest
			files: list of hrefs for files of specified resource
		"""
		self._product.resources[resource_identifier]["files"] = files

	def add_doc_metadata(self, resource_identifier, namespace, metadata):
		"""
		Add key-value pair of metadata for specified resource
		to resource dictionary ("metadata" as key 
		and {namespace: metadata text} as value)

		Args: 
			resource_identifier : identifier of resource provided by imsmanifest
			namespace: full namespace of metadata (adlcp + location)
			metadata: text of metadata element
		"""
		metadata_dict = {
				namespace : metadata
			}

		self._product.resources[resource_identifier]["metadata"] = metadata_dict

	def add_subject_metadata(self, metadata):
		"""
		Assign subject level metadata element (its subelements 
		and attributes) to an ordered dictionary of metadata.

		Args: metadata - ordered dictionary generated from
						 metadata element object 
						 (information includes metadata elements tag, 
						  subelement tags, attributes, text)
		"""
		self._product.metadata = metadata

	def add_schema_metadata(self, key, data):
		"""
		Add key-value pair of metadata to dictionary of schema data.

		Args:
			key - Corresponds to key in schema with same name
			data - metadata bound to type
		"""
		self._product.schema_data[key] = data

	def get_product(self):
		self._product.to_schema()
		self._product.schema_to_file()



class Product:
	def __init__(self):
		self.organizations = {}
		self.resources = {}
		self.metadata = {}
		self.schema_data = {}
		self.schema = schema_dict.schema

	def to_schema(self):
		#pass resources, organizations, metadata into schema
		self.schema["resources"] = self.resources
		self.schema["organizedMaterial"] = self.organizations
		self.schema["courseSpecifications"] = self.metadata

		#pass specific metadata (metadata common to every course) into schema
		self.course_name_to_schema()
		self.course_code_to_schema()
		self.version_to_schema()
		self.instructor_to_schema()

	def course_name_to_schema(self):
		course_name = self.schema_data["name"]
		self.schema["name"] = course_name

	def course_code_to_schema(self):
		course_code = self.schema_data["courseCode"]
		self.schema["courseCode"] = course_code

	def version_to_schema(self):
		version = self.schema_data["version"]
		self.schema["version"] = version

	def instructor_to_schema(self):
		instructor = self.schema_data["Instructor"]
		self.schema["hasCourseInstance"]["Instructor"]["name"] = instructor

	def schema_to_file(self):
		with open('mit_ocw_test.json', 'w') as outfile:
			json.dump(self.schema, outfile)




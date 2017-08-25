
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
		Turn subject level metadata element (its subelements 
		and attributes) into an ordered dictionary.

		Args: metadata - ordered dictionary generated from
						 metadata element object 
						 (information includes metadata elements tag, 
						  subelement tags, attributes, text)
		"""
		self._product.metadata = metadata

class Product:
	"""
	Represent the complex object (for now just a dict) under construction.
	"""
	def __init__(self):
		self.organizations = {}
		self.resources = {}
		self.metadata = {}

	def to_schema(self):



# def main():
# 	# concrete_builder = ConcreteBuilder()
# 	# director = Director()
# 	# director.construct(concrete_builder)
# 	# product = concrete_builder.product
# 	schema_builder = SchemaBuilder(Builder())


# if __name__ == "__main__":
# 	main()
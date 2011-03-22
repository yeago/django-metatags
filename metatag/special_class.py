list_of_subclasses = []

class MetaMetatag(type):
	def __init__(cls, name, bases, dict):
		super(MetaMetatag,cls).__init__(name,bases,dict)
		if cls.__name__ != "Metatag":
			list_of_subclasses.append(cls)

class Metatag(type):
	__metaclass__ = MetaMetatag

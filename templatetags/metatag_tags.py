from django import template

from metatag.models import URLMetatags

register = template.Library()

class MetatagNode(template.Node):
	def render(self, context):
		request = context['request']
		instance = context.get('object')
		try:
			context['metatag'] = URLMetatags.objects.get(path=request.path).as_dict()
		except URLMetatags.DoesNotExist:
			if not instance:
				return ''

			"""
			Below we only touch all the 'metatags' files.
			"""
			from django.conf import settings
			for i in settings.INSTALLED_APPS:
				try:
					module = __import__('%s.metatags' % i)
					for count, app in enumerate(i.split('.')):
						if count == 0:
							continue
					module = getattr(module,app)

					module = getattr(module,'metatags')
				except ImportError:
					pass

			from metatag.special_class import list_of_subclasses
			for sub in list_of_subclasses:
				if sub.model == instance.__class__:
					context['metatag'] = sub.get_dict(instance)
					break
		return '' 
	
@register.tag()
def metatag_populate(parser,token):
	return MetatagNode()

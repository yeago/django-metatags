from django import template
from django.template import Template
from django.core.urlresolvers import resolve

from metatag.models import URLMetatags

from metatag.resolve_to_name_snippet import resolve_to_name

register = template.Library()

class URLMetatagsNode(template.Node):
	def render(self, context):
		request = context['request']
		meta = None
		try:
			url = resolve_to_name(request.path)
			meta = URLMetatags.objects.get(url=url)
		except URLMetatags.DoesNotExist:
			try:
				meta = URLMetatags.objects.get(url=request.path)
			except URLMetatags.DoesNotExist:
				pass


		if meta:
			meta_dict = {'title': meta.title, 'description': meta.description, 'keywords': meta.keywords }

			for key in meta_dict:
				meta_dict[key] = Template(meta_dict[key])
				meta_dict[key] = meta_dict[key].render(context)

			context['metatag'] = meta_dict
		return '' 
	
@register.tag()
def metatag_populate(parser,token):
	return URLMetatagsNode()

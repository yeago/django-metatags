from django import template
from django.db.models import Q
from django.template import Template
from django.core.urlresolvers import resolve

from django.core.cache import cache

from metatag.models import URLMetatags

from metatag.resolve_to_name_snippet import resolve_to_name

register = template.Library()

class URLMetatagsNode(template.Node):
    def render(self, context):
        request = context['request']
        in_cache = cache.get("metatag-%s" % request.path)

        if in_cache:
            context['metatag'] = in_cache
            return ''

        try:
            url = resolve_to_name(request.path)
            meta = URLMetatags.objects.get(Q(url=url)|Q(url=request.path))

        except URLMetatags.DoesNotExist:
            return ''

        meta_dict = {}

        for key in URLMetatags._meta.get_all_field_names():
            att = getattr(meta,key,None)
            if att:
                t = Template(att)
                meta_dict[key] = t.render(context)

        cache.set("metatag-%s" % request.path,meta_dict,300)

        context['metatag'] = meta_dict
        return '' 
    
@register.tag()
def metatag_populate(parser,token):
    return URLMetatagsNode()

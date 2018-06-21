from django import template
from django.db.models import Q
from django.template import Template
from django.core.urlresolvers import resolve

from metatag.models import URLMetatags

from metatag.resolve_to_name_snippet import resolve_to_name

register = template.Library()


class URLMetatagsNode(template.Node):
    def render(self, context):
        request = context['request']
        try:
            url = resolve_to_name(request.path)
            meta = URLMetatags.objects.get(Q(url=url) | Q(url=request.path))

        except URLMetatags.DoesNotExist:
            return ''

        meta_dict = {}
        all_names = [f.name for f in URLMetatags._meta.get_fields()]
        for key in all_names:
            att = getattr(meta, key, None)
            if att:
                t = Template(att)
                meta_dict[key] = t.render(context)

        context['metatag'] = meta_dict
        return ''


@register.tag()
def metatag_populate(parser, token):
    return URLMetatagsNode()

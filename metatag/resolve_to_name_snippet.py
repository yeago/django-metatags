# http://djangosnippets.org/snippets/1378/

from django.urls import URLResolver as RegexURLResolver, URLPattern as RegexURLPattern, Resolver404, get_resolver

__all__ = ('resolve_to_name',)

def get_regex(resolver_or_pattern):
    """Utility method for django's deprecated resolver.regex"""
    try:
        regex = resolver_or_pattern.regex
    except AttributeError:
        regex = resolver_or_pattern.pattern.regex
    return regex

def _pattern_resolve_to_name(self, path):
    match = get_regex(self).search(path)
    if match:
        name = ""
        if self.name:
            name = self.name
        elif hasattr(self, '_callback_str'):
            name = self._callback_str
        else:
            name = "%s.%s" % (self.callback.__module__, self.callback.func_name)
        return name

def _resolver_resolve_to_name(self, path):
    tried = []
    match = get_regex(self).search(path)
    if match:
        new_path = path[match.end():]
        for pattern in self.url_patterns:
            try:
                name = pattern.resolve_to_name(new_path)
            except Resolver404 as e:
                tried.extend([(pattern.regex.pattern + '   ' + t) for t in e.args[0]['tried']])
            else:
                if name:
                    return name
                tried.append(pattern.regex.pattern)
	#raise Resolver404, {'tried': tried, 'path': new_path}


# here goes monkeypatching
RegexURLPattern.resolve_to_name = _pattern_resolve_to_name
RegexURLResolver.resolve_to_name = _resolver_resolve_to_name


def resolve_to_name(path, urlconf=None):
    return get_resolver(urlconf).resolve_to_name(path)

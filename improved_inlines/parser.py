from django.template import TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import ast
import datetime


INLINE_ATTRS = ['ids', 'id', 'filter', ]

def get_inline_attr(inline):
    """
    Tries all the attributes in INLINES_ATTRS in order, returning the first
    one it finds. If the tag isn't <inline>, it searches for those attributes
    with a given prefix.

    Returns the attribute + value as a dict, or raises ValueError if it can't
    find the right attributes.
    """
    prefix = 'data-inline-' if (inline.name != 'inline') else ''
    for attr in INLINE_ATTRS:
        attr_val = inline.get(prefix + attr, None)
        if attr_val:
            return { attr: attr_val }
    if settings.DEBUG:
        raise ValueError, "Inline %s does not have any of the appropriate attributes: %s" % (inline, INLINE_ATTRS)
    return None

def is_inline(tag):
    """
    A filter function, made to be used with BeautifulSoup.

    Makes sure the tag is `inline`, or has both data-inline-type
    and at least one of data-inline-{id,ids,filter} attributes.
    """
    check_type  = lambda attr: attr[0] == 'data-inline-type'
    check_attrs = lambda attr: attr[0] == 'data-inline-id' \
                            or attr[0] == 'data-inline-ids' \
                            or attr[0] == 'data-inline-filter'
    checks_out = filter(check_type, tag.attrs) and filter(check_attrs, tag.attrs)
    return checks_out or tag.name == 'inline'

def inlines(value, return_list=False):
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from beautifulsoup import BeautifulSoup

    content = BeautifulSoup(value, selfClosingTags=['inline','img','br','input','meta','link','hr'])
    inline_list = []

    if return_list:
        for inline in content.findAll(is_inline):
            rendered_inline = render_inline(inline)
            inline_list.append(rendered_inline['context'])
        return inline_list
    else:
        for inline in content.findAll(is_inline):
            rendered_inline = render_inline(inline)
            if rendered_inline:
                inline.replaceWith(render_to_string(rendered_inline['template'], rendered_inline['context']))
            else:
                inline.replaceWith('')
        return mark_safe(content)

def render_inline(inline):
    """
    Replace inline markup with template markup that matches the
    appropriate app and model.

    """
    # Look for inline model type, 'app.model'
    if inline.name == 'inline':
        model_string = inline.get('type', None)
    else:
        model_string = inline.get('data-inline-type', None)

    if not model_string:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Couldn't find a model attribute in the <%s> tag." % inline.name
        else:
            return ''
    app_label, model_name = model_string.split('.')

    # Look for content type
    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        model = content_type.model_class()
    except ContentType.DoesNotExist:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Inline ContentType not found for '%s.%s'." % (app_label, model_name)
        else:
            return ''

    # Check for an inline class attribute
    inline_class = smart_unicode(inline.get('class', ''))

    inline_attr = get_inline_attr(inline)

    if not inline_attr:
        return ''

    if inline_attr.get("ids", None):
        # The tag has the 'ids' attribute, process accordingly...
        id_list = [int(i) for i in inline_attr["ids"].split(',')]
        obj_list = model.objects.in_bulk(id_list)
        obj_list = list(obj_list[int(i)] for i in id_list)
        context = { 'object_list': obj_list, 'class': inline_class }
    elif inline_attr.get("id", None):
        # The tag has the 'id' attribute, process accordingly...
        try:
            obj = model.objects.get(pk=inline_attr["id"])
        except model.DoesNotExist:
            if settings.DEBUG:
                raise model.DoesNotExist, "%s with pk of '%s' does not exist" % (model_name, inline_attr["id"])
            else:
                return ''
        context = { 'content_type':"%s.%s" % (app_label, model_name), 'object': obj, 'class': inline_class, 'settings': settings }
    elif inline_attr.get("filter", None):
        # The tag has the 'filter' attribute, process accordingly...
        try:
            l = inline_attr["filter"].split(',')
            filterdict = dict()
            for item in l:
                try:
                    # This is just here to raise a ValueError if there is no '='
                    item.index('=')
                    parts = item.split('=')
                    ## This should work for text, Need to test for all sorts of values
                    # Note: Potentially dangerous use of eval
                    filterdict[str(parts[0])] = eval(parts[1])
                except ValueError:
                    pass
            obj_list = list(model.objects.filter(**filterdict))
            context = { 'object_list': obj_list, 'class': inline_class }
        except KeyError:
            if settings.DEBUG:
                raise TemplateSyntaxError, "The <inline> filter attribute is missing or invalid."
            else:
                return ''
        except ValueError:
            if settings.DEBUG:
                raise TemplateSyntaxError, inline_attr["filter"] + ' is bad, dummy.'
            else:
                return ''
    else:
        raise ValueError

    # Set Default Template
    template = list()
    try:
        template.insert(0, inline['template'])
    except KeyError:
        pass
    template.extend(["inlines/%s_%s.html" % (app_label, model_name), "inlines/default.html"])

    rendered_inline = {'template': template, 'context': context}

    return rendered_inline
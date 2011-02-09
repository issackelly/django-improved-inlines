from django.template import TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import ast
import datetime

def is_inline(tag):
    """
    A filter function, made to be used with BeautifulSoup.

    In order to match, a tag must be an `inline` or have either a
    "data-inline-model" attribute or a "data-inline-id" attribute.
    """
    check_attrs = lambda attr: attr[0] == 'data-inline-model' or attr[0] == 'data-inline-id' or attr[0] == 'data-inline-ids'
    return tag.name == 'inline' or filter(check_attrs, tag.attrs)


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
        model_string = inline.get('data-inline-model', None)

    if not model_string:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Couldn't find the appropriate attribute in the <%s> tag." % inline.name
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

    if inline.name == 'inline':
        id_list = inline.get('ids', None)
    else:
        id_list = inline.get('data-inline-ids', None)
    if not id_list:
        if inline.name == 'inline':
            obj_id = inline.get('id', None)
        else:
            obj_id = inline.get('data-inline-id', None)
        if not obj_id:
            filters = inline.get('filter', None)
            if not filters:
                raise ValueError, "Could not find any of the right attributes in %s" % inline
            else:
                # We have filters
                try:
                    l = inline['filter'].split(',')
                    filterdict = dict()
                    for item in l:
                        try:
                            # This is just here to throw a ValueError if there is no '='
                            item.index('=')
                            parts = item.split('=')
                            ## This should work for text, Need to test for all sorts of values
                            # Note: Potentially dangerous use of eval
                            filterdict[parts[0]] = eval(parts[1])
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
                        raise TemplateSyntaxError, inline['filter'] + ' is bad, dummy.'
                    else:
                        return ''
        else:
            # We have obj_id
            try:
                obj = model.objects.get(pk=obj_id)
            except model.DoesNotExist:
                if settings.DEBUG:
                    raise model.DoesNotExist, "%s with pk of '%s' does not exist" % (model_name, inline['id'])
                else:
                    return ''
            context = { 'content_type':"%s.%s" % (app_label, model_name), 'object': obj, 'class': inline_class, 'settings': settings }
    else:
        # We have id_list
        id_list = [int(i) for i in id_list.split(',')]
        obj_list = model.objects.in_bulk(id_list)
        obj_list = list(obj_list[int(i)] for i in id_list)
        context = { 'object_list': obj_list, 'class': inline_class }

    # Set Default Template
    template = list()
    try:
        template.insert(0, inline['template'])
    except KeyError:
        pass
    template.extend(["inlines/%s_%s.html" % (app_label, model_name), "inlines/default.html"])

    rendered_inline = {'template': template, 'context': context}

    return rendered_inline
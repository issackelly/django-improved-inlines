=======================
Django Improved Inlines
=======================

Django improved inlines is a version of the inlines app from `django-basic-apps`_  that has a few specific features that I needed:

* filter="" instead of just ids= and id=
* template="" instead of just inlines/<app>_<model>.html
* Support for non-<inline> tags by prefixing "data-inline-" to type, ids, id, filter
	
Thanks to nathanborror for the initial code.

Dependancies
============

* BeautifulSoup_ is required to use the inlines app.

Usage
=====

Install in INSTALLED_APPS so the templates can be found

"improved_inlines"

Inlines is a template filter that can be used in
conjunction with inline markup to insert content objects
into other pieces of content. An example would be inserting
a photo into a blog post body.

Drop-in replacement for django-basic-inlines/inlines

An example of the markup is::
    <inline type="calendar.event" filter="date__gte=datetime.date.today()" template="calendar/event_inline.html" />

other attribute options are::
	<inline type="app.model" id="<some pk>"  class="some_class_passed_to_template"/>
	<inline type="app.model" ids="<some pk>,<some other pk>" />

examples with other tags::
	<div data-inline-type="app.model" data-inline-id="<some pk>"></div>
	<ul data-inline-type="app.model" data-inline-ids="<some pk>,<some other pk>"></ul>
	<p data-inline-type="app.model" data-inline-filter="title__containts='title-string'"></p>


The type attribute is app_name.model_name and the id is
the object id. Pretty simple.

In your template you would say::
   {% load inlines %}
   {{ post.body|render_inlines }}


.. _django-basic-apps: http://github.com/nathanborror/django-basic-apps/
.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
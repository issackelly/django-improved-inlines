Django Improved Inlines
=======================

Django improved inlines is a version of the inlines app from (django-basic-apps)[http://github.com/nathanborror/django-basic-apps/] that has two specific features that I needed:

filter="" instead of just ids
and template="" instead of just inlines/<app>_<model>.html
	
That's it. Thanks to nathanborror for the initial code.

Dependancies
------------

* BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/) is required to use the blog and, subsequently, the inlines app.

Usage
-----

Inlines is a template filter that can be used in
conjunction with inline markup to insert content objects
into other pieces of content. An example would be inserting
a photo into a blog post body.

Drop-in replacement for django-basic-inlines/inlines

An example of the markup is:
  <inline type="calendar.event" filter="date__gte=today" template="calendar/event_inline.html" />


The type attribute is app_name.model_name and the id is
the object id. Pretty simple.

In your template you would say:
  {% load inlines %}

  {{ post.body|render_inlines }}
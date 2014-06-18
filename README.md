django-placeholder
==================

Yes, another project to create placeholders (inline editable content). The goal of this project is to be a simple (and stupid) tool to use placeholders on your project. It uses the default `django admin` (compatible with grappelli, suit and others) so you can reuse everything from admin. (forms, fields, widgets...)

Installation
------------

 1. Install the python library:
```sh
pip install django-placeholder
```
2. Put `placeholder` on **INSTALLED_APPS**
```python
INSTALLED_APPS = (
    'app1',
    'placeholder',
    'app2',
)
```

Demo Project
------------

There is a example project on the directory `django-placeholder/example` you can test it following these steps:

```sh
mkvirtualenv demo
pip install django django-classy-tags
git clone git@github.com:mauler/django-placeholder.git
cd django-placeholder/example
python manage runserver
```
Goto URL http://localhost:8000/admin/ and do login with username `admin` and password `admin`.

After access the URL http://localhost:8000/ to see the editable content press **CTRL+SHIFT+X**, after some icon will be shown click on then to edit that element. After editing, close popup and that part of page will be reloaded (Invaliding any cache).

To see how that was done check `django-placeholder/example/content/templates/home.html`

It's simple stupid :)


How it works
------------

Using [jQuery][1] and [Fancybox][2] we search for elements defined as placeholders on page if the user is authenticated e has permissions to edit those elements (Model instances).

For each element a hidden button is created on the page (hidden), those elements opens the pop-up (Fancybox) when clicked. This pop-up when closed reload that part of the page.

So, any changes you on the admin (Inside the pop-up) will be available at that part.


Basic Usage
-----------

1. You need [jQuery][1] on your project, if you don'. Add it:
```html
<script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
```

2. Add this include with the javascript, css and icons necessary to use django-placeholder (They are loaded only for authenticated users that has staff permission):  
```html
{% extends "placeholder/includes.html" %}
```

3. To make a element act as a placeholder you need to load the template tag library `placeholder_tags` and use the template tag `ph_instance_tag_attrs`:

```html
{% load placeholder_tags %}

<div {% ph_instance_tagattrs post %}>
    <h4>{{ post.title }}</h4>
    {{ post.text|linebreaks }}
</div>
```
This template tag will return the tag attributes: `data-placeholder-instance` and `data-placeholder-md5hash` that contains all data needed to manipulate the placeholder.

4. Being authenticated and having the permissions necessary (is_staff) press ctrl+shift+x to show the elements that can be edited.

5. Click on the icon, edit, save changes and close the pop-up. :)

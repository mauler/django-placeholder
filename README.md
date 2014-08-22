django-placeholder
==================

[![Test Status](https://travis-ci.org/mauler/django-placeholder.png?branch=master)](https://travis-ci.org/mauler/django-placeholder)

[![Code Health](https://landscape.io/github/mauler/django-placeholder/master/landscape.png)](https://landscape.io/github/mauler/django-placeholder/master)

[![Latest PyPI version](https://pypip.in/v/django-placeholder/badge.png)](https://crate.io/packages/django-placeholder/)

[![Number of PyPI downloads](https://pypip.in/d/django-placeholder/badge.png)](https://crate.io/packages/django-placeholder/)

Yes, another project to create placeholders (inline editable content). The goal of this project is to be a simple (and stupid) tool to use placeholders on your project. It uses the default `django admin` (compatible with grappelli, suit and others) so you can reuse everything from admin. (forms, fields, widgets...)

Installation
------------

 1. Install with pip the django-placeholder python library:
```sh
pip install django-placeholder
```
2. Put `placeholder` on **INSTALLED_APPS**
```python
INSTALLED_APPS = (
    # ...
    'placeholder',
)
```

How it works
------------

Using [jQuery](http://jquery.com/) and [Fancybox](http://fancybox.net/) we search for elements defined as placeholders on page if the user is authenticated e has permissions to edit those elements (Model instances).

For each element a hidden button is created on the page (hidden), those elements opens the pop-up (Fancybox) when clicked. This pop-up when closed reload that part of the page.

So, any changes you on the admin (Inside the pop-up) will be available at that part.

Basic Usage
-----------

1. You need [jQuery](http://jquery.com/) on your project, if you don'. Add it:
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

4. Being authenticated and having the permissions necessary (is_staff) press **CTRL+SHIFT+X** to show the elements that can be edited.

5. Click on the icon, edit, save changes and close the pop-up. :)

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
Go to URL http://localhost:8000/admin/ and login with username and password `admin`.

To see the editable content press **CTRL+SHIFT+X** on URL http://localhost:8000/ and some icon will be shown. Click on the icon to edit the element. After edit, close the popup and that part of page will be reloaded (invalidating any cache).

![Posts](https://raw.githubusercontent.com/mauler/django-placeholder/master/docs/usage1.png)

----

To see the editable content press **CTRL+SHIFT+X** on URL http://localhost:8000/ and some icon will be shown. Click on the icon to edit the element.

![Placeholder Icons](https://raw.githubusercontent.com/mauler/django-placeholder/master/docs/usage2.png)

----

A Pop-up will open with admin edit form of that model instance:

![Admin change form](https://raw.githubusercontent.com/mauler/django-placeholder/master/docs/usage3.png)

----

Lets edit that content, change the texts and the image:

![Admin change form](https://raw.githubusercontent.com/mauler/django-placeholder/master/docs/usage4.png)

----

After changing, you will see the change list page with success message

![Admin change form](https://raw.githubusercontent.com/mauler/django-placeholder/master/docs/usage5.png)

----

And your new content will be available:

![Admin change form](https://raw.githubusercontent.com/mauler/django-placeholder/master/docs/usage6.png)

----

To see how that was done check `./django-placeholder/example/content/templates/home.html`

It's simple stupid :)


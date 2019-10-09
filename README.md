# Django Security Headers Example

Example project to show the implementation of various security headers in Django.

**Requirements**: Python 3.7+

## Quick Start

1. Clone the repository
2. Create a new virtual environment: `python3 -m venv venv`
3. Activate your new virtual environment
4. Install the dependencies: `pip install -r requirements.txt`
5. Run the development server: `./manage.py runserver`
6. Make an HTTP request to `localhost:8000` to view the headers `curl -I localhost:8000`

## Overview

Inside the `config/settings`, you'll see a `base.py` and a `prod.py`. The `base.py` is
intended as local development settings, and the `prod.py` is intended as the production
settings.

In `base.py` starting on line 115, you will find the start of the security header
configuration as well as links to the proper documentation.

`prod.py` sets the security headers that depend on an HTTPS connection such as
`Strict-Transport-Security`. Developing using `localhost` does not come with a valid TLS
certificate for an HTTPS connection. Keeping all settings that depend on an HTTPS connection
in `prod.py` allows us to develop locally and still deploy with the correct settings for
an HTTPS connection in production.


## Python Packages

Django has built in support for a lot of the security headers. Additionally,
[Django 3.0](https://docs.djangoproject.com/en/dev/releases/3.0/#security) adds support for
`Referrer-Policy`. However, sending all of the headers requires a few additional packages
and a custom middleware.

* [django-csp](https://github.com/mozilla/django-csp) provides the `Content-Security-Policy`
* [django-feature-policy](https://github.com/adamchainz/django-feature-policy) provides the
`Feature-Policy`
* The custom middleware in `django_security_headers_example/core/middleware.py` provides
`Expect-CT` and `Referrer-Policy` for Django versions before 3.0
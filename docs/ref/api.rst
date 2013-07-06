RESTful API
=============

**django-admin2** comes with a builtin REST-API for accessing all the
resources you can get from the frontend via JSON.

The API can be found at the URL you choose for the admin2 and then append
``api/v0/``.

If the API has changed in a backwards-incompatible way we will increase the
API version to the next number. So you can be sure that you're frontend code
should keep working even between updates to more recent django-admin2
versions.

However currently we are still in heavy development, so we are using ``v0``
for the API, which means is subject to change and being broken at any time.

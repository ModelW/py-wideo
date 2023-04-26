# API

This handles the API and back-office admin.

All the URLs pointing to this are prefixed by `/back`.


> **Note** &mdash; There is one exception to this, which is the Wagtail previous
> system. They are fairly complex, and it's the proxy middleware in Nuxt taking
> care of this. Check [`*.vue`](../front/pages/*.vue) and
> [`nuxt.config.js`](../front/nuxt.config.js) for more info.


## Components

You'll find the following apps:

-   [people](./watch_this/apps/people) &mdash; The user model and
    authentication.



-   [cms](./watch_this/apps/cms) &mdash; All the page models for
    Wagtail


## OpenAPI

When the app is in development mode, you can access the OpenAPI documentation at
`/back/api/schema/redoc/`.

This documentation is auto-generated using
[drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/). As you
create more APIs, make sure that they render nicely in OpenAPI format.

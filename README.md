# Variant Explorer

A web application for searching and exploring genetic variants, built with
Django server-rendered templates, [HTMX](https://htmx.org/), and
[Alpine.js](https://alpinejs.dev/). A Django REST Framework JSON API is also
exposed under `/api/`.

## Setup and run the project locally

### Prerequisites

[Docker](https://docs.docker.com/engine/install/) is recommended.

### Build and launch the application

In a terminal window:

- `cd` to the top project directory.
- Build the image with `docker compose build`.
- Start the app with `docker compose up`.

### Verify the application is running

Once the database is finished loading:

- The UI is available at <http://localhost:8000/>.
- The DRF browsable API is available at <http://localhost:8000/api/>
  (e.g. <http://localhost:8000/api/variants/>, <http://localhost:8000/api/genes/>).

### Cleaning up

- Stop the container with ctrl+C in the terminal running `docker compose up`.
- Tear down with `docker compose down -v --remove-orphans`.

## Project layout

```
variant-explorer-htmx/
  data/                                 # variants TSV fixtures
  backend/
    Dockerfile
    docker-entrypoint.sh                # migrate + loadvariants + runserver
    requirements.txt
    manage.py
    variant_explorer/
      settings.py
      urls.py                           # SSR routes + DRF router under /api/
      views.py                          # index_view, variant_rows_view, DRF viewsets
      models.py / serializers.py
      management/commands/loadvariants.py
      templates/variant_explorer/
        base.html                       # loads htmx + alpine via CDN
        index.html                      # full-page shell
        _variant_rows.html              # HTMX partial: <tbody> + pagination
      static/variant_explorer/app.css
```

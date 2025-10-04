import os

SPECTACULAR_SETTINGS = {
    'TITLE': os.environ.get('TITLE_API', 'BaseDRFApp'),
    'DESCRIPTION': os.environ.get('DESCRIPTION_API', ''),
    'VERSION': os.environ.get('VERSION_API', '0.1'),
    'SERVE_INCLUDE_SCHEMA': False,
    'TAGS': [],
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

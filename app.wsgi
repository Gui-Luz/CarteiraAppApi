import sys

project_home = '/var/www/CarteiraAppApi/'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from api.main import app as application
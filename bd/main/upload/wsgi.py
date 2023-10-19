import os

__FILEPATH__ = os.path.dirname(os.path.dirname(os.path.dirname((os.path.dirname(os.path.abspath(__file__))))))

activate_this = os.path.join(__FILEPATH__, 'env/bin/activate')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from post_image import app as application

from sys import path 
from shutil import copy

master_doc = 'index'

html_theme = "alabaster"

extensions = ['sphinx.ext.autodoc']

autodoc_class_signature = "separated"


def setup(app):

    path.append('../../')
    
    #app.add_css_file('custom.css')  # may also be an URL
    try:
        copy('../../app/custom.css', '../../doc/_static/custom.css')
    except:
        ()
    #copy('custom.css', '../doc/_static/custom.css')

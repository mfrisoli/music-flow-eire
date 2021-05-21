from flask import render_template
from . import library

@library.route('/')
def library_home():
    return render_template('library/library_index.html')
    
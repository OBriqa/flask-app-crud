from flask import render_template

def page_not_found(error, redirect = 'index'):
    return render_template('errors/page_not_found.html', redirect = redirect)

def internal_server_error(error, redirect = 'index', param = None):
    return render_template('errors/internal_server_error.html', error = error, redirect = redirect, param = param)
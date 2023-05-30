from flask import render_template
from . import bp


SOURCE = "/errors/"


@bp.app_errorhandler(400)
def token_error(e):
    return render_template(f"{SOURCE}400.html"), 400


@bp.app_errorhandler(503)
def access_forbidden(e):
    return render_template(f"{SOURCE}403.html"), 403


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template(f"{SOURCE}404.html"), 404


@bp.app_errorhandler(500)
def internal_error(e):
    return render_template(f"{SOURCE}500.html"), 500

from flask import render_template
from . import bp


SOURCE = "/errors/"


@bp.app_errorhandler(400)
def bad_request(e):
    return render_template(f"{SOURCE}400.html"), 400


@bp.app_errorhandler(403)
def access_forbidden(e):
    return render_template(f"{SOURCE}403.html"), 403


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template(f"{SOURCE}404.html"), 404


@bp.app_errorhandler(405)
def method_not_allowed(e):
    return render_template(f"{SOURCE}404.html"), 405


@bp.app_errorhandler(500)
def internal_error(e):
    return render_template(f"{SOURCE}500.html"), 500

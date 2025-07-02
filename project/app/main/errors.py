"""
Module: main/errors.py
Description: Registers custom error handlers for the application.
"""

def register_error_handlers(app):
    """
    Attach 404 and 500 error handlers to the Flask app.
    """
    from flask import render_template

    @app.errorhandler(404)
    def not_found(e):
        """Custom 404 Not Found handler."""
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        """Custom 500 Internal Server Error handler."""
        return render_template("500.html"), 500

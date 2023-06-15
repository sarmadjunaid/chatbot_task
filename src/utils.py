from flask import redirect, url_for, session


def login_required(func):
    def secure_function():
        if session:
            if "email" not in session.get('userinfo', {}):
                return redirect(url_for("login"))
        return func()

    return secure_function

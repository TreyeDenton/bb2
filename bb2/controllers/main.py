from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from bb2.extensions import cache
from bb2.forms import LoginForm, NewProjectForm
from bb2.models import User, Project, db

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200

@main.route("/projects", methods=['GET', 'POST'])
def projects():
    projects = Project.query.order_by(Project.name)
    form = NewProjectForm(request.form)

    if form.validate_on_submit():
        new_project = Project(form.name.data)
        db.session.add(new_project)
        db.session.commit()
        redirect(url_for(".projects"))

    return render_template("projects.html", projects=projects, form=form)

@main.route("/new_project", methods=['GET', 'POST'])
def new_project():
    form = NewProjectForm(request.form)

    if form.validate_on_submit():
        new_project = Project(form.name.data)
        db.session.add(new_project)
        db.session.commit()
        redirect(url_for(".projects"))

    return render_template("new_project.html", form=form)

# Make Project names available to base.html
@main.context_processor
def inject_project():
    return dict(projects=Project.query.order_by(Project.name))


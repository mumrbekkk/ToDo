from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import *
from app.models import *

"""Additional functions that will be used during rendering"""
def get_all_rows_by_attribute(table, attribute, value):
    table_list = db.session.execute(db.select(table).where(getattr(table, attribute) == value)).scalars().all()
    return table_list

def get_row_by_attribute(table, attribute, value):
    return db.session.execute(db.select(table).where(getattr(table, attribute) == value)).scalar()

def get_all_rows(table):
    query = db.select(table)
    return db.session.execute(query).scalars().all()

def delete_row_by_id(table, id):
    select_query = db.select(table).where(table.id == id)
    row = db.session.execute(select_query).scalar()
    if row:
        db.session.delete(row)
        db.session.commit()
        return True

    return False

def register_routes(app):
    """Register routes with the Flask app."""
    # --------------- HOME --------------- #
    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template("index.html")


    @app.route('/task_actions/<int:template_id>/<int:task_id>', methods=['GET', 'POST'])
    def task_action(template_id, task_id):
        task = Task.query.get(task_id)
        if task and request.method == 'POST':
            if request.form['action'] == "in-process":
                task.status = 1
                db.session.commit()
            elif request.form['action'] == "delete":
                delete_row_by_id(Task, task_id)
            elif request.form['action'] == "todo":
                task.status = 0
                db.session.commit()
            elif request.form['action'] == "complete":
                task.status = 2
                db.session.commit()
            elif request.form['action'] == "in-process":
                task.status = 1
                db.session.commit()


        return redirect(url_for('my_template', template_id=template_id))

    # --------------- TEMPLATE --------------- #
    @app.route('/my_template/<int:template_id>', methods=['GET', 'POST'])
    def my_template(template_id):
        tasks = get_all_rows_by_attribute(Task, "template_id", template_id)
        template = get_row_by_attribute(Template, "id", template_id)

        return render_template("my-template.html",
                               tasks=tasks,
                               template=template,)


    # --------------- TEMPLATES --------------- #
    @app.route('/my_templates', methods=['GET', 'POST'])
    def my_templates():
        if request.method == "POST":
            template_id = request.form['template_id']
            action = request.form['action']
            if action == "edit":
                return redirect(url_for('edit_template', template_id=template_id))

            elif action == "delete":
                delete_row_by_id(Template, template_id)
                flash("Template has been successfully deleted!")
                return redirect(url_for('my_templates'))

        if current_user.is_authenticated:
            return render_template("my-templates.html",
                                   templates = get_all_rows_by_attribute(Template, "user_id", current_user.id))
        return render_template("my-templates.html")

    # --------------- EDIT TEMPLATE --------------- #
    @app.route('/edit_template/<int:template_id>', methods=['GET', 'POST'])
    def edit_template(template_id):
        form = EditTemplateForm()
        template = Template.query.get(template_id)

        if form.validate_on_submit():
            template.name = form.name.data
            template.description = form.description.data
            db.session.commit()
            flash("Template has been successfully updated!")
            return redirect(url_for('my_templates'))
        if template:
            form.process(obj=template)
            form.submit.label.text = "Update"
            return render_template("edit-template.html", edit_form=form)

    # --------------- ADD TEMPLATE --------------- #
    @app.route('/add_template', methods=['GET', 'POST'])
    def add_template():
        add_template_form = AddTemplateForm()
        if not current_user.is_authenticated:
            flash("Please log in to add a template.", "login_error")
            return redirect(url_for('login'))

        if add_template_form.validate_on_submit():
            new_template = Template(
                user_id=current_user.id,
                name=add_template_form.name.data,
                description=add_template_form.description.data,
            )
            db.session.add(new_template)
            db.session.commit()

            flash("Template has been successfully added!")
            return redirect(url_for('my_templates'))

        return render_template("add-template.html",
                               add_template_form=add_template_form)

    # --------------- ADD TASK --------------- #
    @app.route('/add_task/<int:template_id>', methods=['GET', 'POST'])
    def add_task(template_id):
        add_task_form = AddTask()

        if add_task_form.validate_on_submit():
            new_task = Task(
                template_id=template_id,
                name=add_task_form.name.data,
                description=add_task_form.description.data,
                start_date=add_task_form.start_date.data,
                end_date=add_task_form.end_date.data
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('my_template', template_id=template_id))

        return render_template('add-task.html',
                               add_task_form=add_task_form)

    # --------------- REGISTER --------------- #
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        register_form = RegisterForm()

        if register_form.validate_on_submit():
            existing_user = get_row_by_attribute(User, 'email', register_form.email.data)
            if existing_user:
                flash("That email is already registered!", "register_error")
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = User(
                name=register_form.name.data,
                email=register_form.email.data,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash(f"Hello {current_user.name}, welcome to ToDo application")
            return redirect(url_for('my_templates'))

        return render_template("register.html", register_form=register_form)

    # --------------- LOGIN --------------- #
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user = get_row_by_attribute(User, 'email', login_form.email.data)
            if not user:
                flash("Invalid email", "login_error")
                return redirect(url_for('login'))
            elif not check_password_hash(user.password, login_form.password.data):
                flash("Invalid password", "login_error")
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('my_templates'))

        return render_template("login.html", login_form=login_form)

    # --------------- LOGOUT --------------- #
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        return redirect(url_for('login'))

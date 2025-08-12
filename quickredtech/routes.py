from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .extensions import db, login_manager
from .models import User, Project

# In-memory storage for contact messages (for demo; use DB in production)
contact_messages = []

from .forms import LoginForm, SignupForm, ProjectForm, ContactForm

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_routes(app):
    # Create default admin user if not present
    with app.app_context():
        admin_email = 'admin@quickredtech.com'
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_user = User(name='admin ceo', email=admin_email, is_admin=True)
            admin_user.set_password('ceo quick red tech')
            db.session.add(admin_user)
            db.session.commit()
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            flash('Message sent! We will contact you soon.', 'success')
            return redirect(url_for('contact'))
        return render_template('contact.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Invalid email or password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already registered. Please log in or use a different email.', 'danger')
                return render_template('signup.html', form=form)
            user = User(name=form.name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('signup.html', form=form)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        projects = Project.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', projects=projects)

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')

    @app.route('/settings')
    @login_required
    def settings():
        return render_template('settings.html')

    @app.route('/databases')
    @login_required
    def databases():
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        users = User.query.all()
        projects = Project.query.all()
        return render_template('databases.html', users=users, projects=projects)

    @app.route('/faqs')
    def faqs():
        return render_template('faqs.html')

    @app.route('/submit-project', methods=['GET', 'POST'])
    @login_required
    def submit_project():
        form = ProjectForm()
        if form.validate_on_submit():
            project = Project(
                user_id=current_user.id,
                title=form.title.data,
                description=form.description.data,
                service_type=form.service_type.data,
                status='Pending',
            )
            db.session.add(project)
            db.session.commit()
            flash('Project submitted successfully!', 'success')
            return redirect(url_for('dashboard'))
        return render_template('submit_project.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/admin-login', methods=['GET', 'POST'])
    def admin_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data) and user.is_admin:
                login_user(user)
                return redirect(url_for('admin_panel'))
            flash('Invalid admin credentials.', 'danger')
        return render_template('admin_login.html', form=form)

    @app.route('/admin')
    @login_required
    def admin_panel():
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        users = User.query.all()
        projects = Project.query.all()
        # Find user IDs with at least one project
        active_user_ids = {p.user_id for p in projects}
        return render_template('admin_panel.html', users=users, contacts=contact_messages, projects=projects, active_user_ids=active_user_ids)

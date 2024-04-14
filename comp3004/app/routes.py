from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import db, User, TrainingSession, Trainer,Equipment, Rooms
from werkzeug.security import generate_password_hash
from datetime import datetime


# Initialize your Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  
        health_info = request.form['health_info']
        fitness_goals = request.form['fitness_goals']

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another one.', 'error')
            return redirect(url_for('main.trainer_dashboard'))

        # Create new User instance without hashing the password
        new_user = User(username=username, email=email, password=password, health_info=health_info, fitness_goals=fitness_goals)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/schedule', methods=['GET', 'POST'])
def schedule():
    # Fetch all available trainers and rooms from the database for the form
    if request.method == 'GET':
        trainers = Trainer.query.all()
        rooms = Rooms.query.filter_by(is_available=True).all()
        return render_template('schedule.html', trainers=trainers, rooms=rooms)
    
    elif request.method == 'POST':
        # Get form data
        trainer_id = request.form['trainer_id']
        datetime = request.form['date_time']
        room_id = request.form['room_id']  
        
        user_id = session.get('user_id') 
        
        # Create a new TrainingSession object with all necessary data
        new_session = TrainingSession(
            member_id=user_id,
            trainer_id=trainer_id,
            datetime=datetime,
            room_id=room_id  
        )
        
        # Add the new session to the database and commit the changes
        db.session.add(new_session)
        db.session.commit()

        # Notify the user of the successful scheduling
        flash('Your training session has been scheduled!', 'success')
        return redirect(url_for('main.schedule'))

@main.route('/trainer_dashboard', methods=['GET', 'POST'])
def trainer_dashboard():
    if 'is_trainer' in session and session['is_trainer']:
        trainer_id = session['user_id']
        trainer = Trainer.query.get(trainer_id)
        sessions = TrainingSession.query.all()
        members = []
    

        if request.method == 'POST':
            if 'update_availability' in request.form:
                # Update availability logic
                available_times = request.form['available_times']
                trainer.available_times = available_times
                db.session.commit()
                flash('Your availability has been updated.', 'success')

            elif 'search_members' in request.form:
                # Search members logic
                search_name = request.form['search_name']
                members = User.query.filter(User.username.ilike(f'%{search_name}%')).all()
    


        return render_template('trainer_dashboard.html', trainer=trainer, members=members, sessions=sessions)
    else:
        flash('You must be logged in as a trainer to view this page.', 'error')
        return redirect(url_for('main.login'))



    
@main.route('/dashboard', methods=['GET'])
def admin_dashboard():
    if 'username' in session and session['username'] == "Admin":
        return render_template('admin_dashboard.html')
    else:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.home'))
    
@main.route('/admin/rooms')
def list_rooms():
    rooms = Rooms.query.all()
    return render_template('list_rooms.html', rooms=rooms)

@main.route('/admin/rooms/edit/<int:id>', methods=['GET', 'POST'])
def edit_room(id):
    room = Rooms.query.get_or_404(id)
    if request.method == 'POST':
        room.name = request.form['name']
        room.capacity = int(request.form['capacity'])
        room.is_available = 'is_available' in request.form
        db.session.commit()
        flash('Room updated successfully.')
        return redirect(url_for('main.list_rooms'))
    return render_template('edit_room.html', room=room)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # First check if the user is a trainer
        trainer = Trainer.query.filter_by(username=username).first()
        if trainer and trainer.password == password:  # Assuming trainers have a password field now
            session['username'] = username
            session['user_id'] = trainer.id
            session['is_trainer'] = True  # Set a flag to indicate a trainer is logged in
            session['logged_in'] = True
            return redirect(url_for('main.register'))  # Correct endpoint

        # If not a trainer, check if the user is a regular user
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            session['user_id'] = user.id
            session['is_trainer'] = False  # Indicate that a regular user is logged in
            session['logged_in'] = True
            return redirect(url_for('main.profile'))

        # If neither, flash an invalid login message
        flash('Invalid username or password')
    
    return render_template('login.html')

@main.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('main.login'))

        # Fetch all training sessions for this user
        sessions = TrainingSession.query.filter_by(member_id=user_id).all()

        return render_template('profile.html', user=user, sessions=sessions)
    else:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('main.login'))
    

@main.route('/admin/room-booking')
def manage_room_booking():
    return render_template('manage_room_booking.html')

@main.route('/admin/equipment-maintenance')
def manage_equipment():
    print("hello world")
    all_equipment = Equipment.query.all()
    for equipment in all_equipment:
        print(f'Equipment Name: {equipment.name}, Status: {equipment.status}')
    return render_template('manage_equipment.html', equipment_list=all_equipment)


@main.route('/edit_equipment/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    # Assuming you want to fetch and possibly edit the equipment with this id
    equipment = Equipment.query.get_or_404(id)
    if request.method == 'POST':
        # Process your form data here and update the equipment
        equipment.name = request.form['name']
        equipment.status = request.form['status']
        db.session.commit()
        flash('Equipment updated successfully!')
        return redirect(url_for('main.manage_equipment'))

    # Show the form with existing equipment data for GET request
    return render_template('edit_equipment.html', equipment=equipment)


@main.route('/admin/class-schedule')
def update_class_schedule():
    return render_template('update_class_schedule.html')

@main.route('/admin/billing')
def manage_billing():
    return render_template('manage_billing.html')

@main.route('/logout')
def logout():
    session.clear()  # Clears all data from the session
    flash('You have been logged out.')
    return redirect(url_for('main.home'))
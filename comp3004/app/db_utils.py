# db_utils.py
from models import db, Trainer

def add_trainers():
    trainer_a = Trainer(name="Trainer A", available_times="Monday to Friday, 9 AM to 5 PM")
    trainer_b = Trainer(name="Trainer B", available_times="Weekends, 10 AM to 4 PM")
    
    db.session.add(trainer_a)
    db.session.add(trainer_b)
    
    try:
        db.session.commit()
        print("Trainers added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to add trainers: {e}")



add_trainers()

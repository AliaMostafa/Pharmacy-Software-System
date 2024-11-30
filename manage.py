# manage.py
from flask.cli import FlaskGroup
from app import app, db
from models import User, Medicine

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    """Loads initial data from CSV"""
    from app import load_medicines_from_csv
    load_medicines_from_csv()

if __name__ == "__main__":
    cli()
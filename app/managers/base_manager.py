from app import db

class BaseManager:
    model = None

    def __init__(self, model=None):
        if model:
            self.model = model

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()

    def find_by_id(self, _id):
        return db.session.query(self.model).get(_id)

    def find_first_by(self, **filters):
        return db.session.query(self.model).filter_by(**filters).first()

    def find_all(self, **filters):
        return db.session.query(self.model).filter_by(**filters).all()

    def update(self, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

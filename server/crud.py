from server.common import get_db
from sqlalchemy.orm import Session


def create(model, db:Session):
    new = model
    db.add(new)
    db.commit()

# def get(model, param, db:Session):
#     filter_attr = getattr(model, param, None)
#     get_result = db.query(model).filter(filter_attr == param).first()
#     return get_result


def delete(model, db:Session):
    remove = model
    db.delete(remove)
    db.commit()

    

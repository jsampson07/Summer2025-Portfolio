from typing import Optional
from flask_macro_app import db
import sqlalchemy as sa  # Used for fundamental building blocks for the database schema i.e. defining data types
import sqlalchemy.orm as so  # Used for functions and types that are part of the ORM's mapping proces (mapping objects)
import enum

class GoalEnum(enum.Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTAIN = "maintain"
    CASUAL = "casual"

class User(db.Model):
    # so.Mapped[int]/so.Mapped[float] - defines the type of the column (required)
    # so.Mapped[Optional[str]] - defines type of the column should there be a value (not required)
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    age: so.Mapped[int] = so.mapped_column()
    weight: so.Mapped[float] = so.mapped_column()
    goal: so.Mapped[GoalEnum] = so.mapped_column(sa.Enum(GoalEnum))

    def __repr__(self):
        return f"<User {self.username}>"
"""models module

-- User database model
-- Directories database model 
"""

from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so 

from app import db 


class User(db.Model):
    """Represents users stored in the database"""

    __tablename__ = "user" 

    user_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(255), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) 
    
    dated: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    is_deleted: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    entries: so.WriteOnlyMapped['Directories'] = so.relationship(back_populates='author')

    def __repr__(self):
        """Represents objects from this class for print statements"""
        return f"User {self.username}>"
    

class Directories(db.Model): 
    """Represents directory information stored in the database"""

    __tablename__ = "directories"

    directories_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    financial_year: so.Mapped[str] = so.mapped_column(sa.String(4))
    category: so.Mapped[str] = so.mapped_column(sa.String(50))
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    filepath: so.Mapped[str] = so.mapped_column(sa.String(4000))
    
    dated: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    is_deleted: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.user_id),index=True)
    author: so.Mapped[User] = so.relationship(back_populates='entries')

    def __repr__(self): 
        """Represents objects from this class for print statements"""
        return f"Directory {self.financial_year}/{self.category}>"






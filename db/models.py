from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

engine = create_engine('sqlite:///server.db')


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    last_login: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    active_users: Mapped['ActiveUsers'] = relationship(back_populates='user')
    login_history: Mapped['LoginHistory'] = relationship(back_populates='user')


class ActiveUsers(Base):
    __tablename__ = 'active_users'
    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(String)
    port: Mapped[str] = mapped_column(String)
    login_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user_id = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship(back_populates='active_users')


class LoginHistory(Base):
    __tablename__ = 'login_history'
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    ip: Mapped[str] = mapped_column(String)
    port: Mapped[str] = mapped_column(String)
    user_id = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship(back_populates='login_history')

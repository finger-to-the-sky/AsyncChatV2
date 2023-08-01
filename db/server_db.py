import datetime
from sqlalchemy import create_engine
from .models import Base, Users, ActiveUsers, LoginHistory
from sqlalchemy.orm import Session


class ServerStorage:
    def __init__(self):
        self.engine = create_engine('sqlite:///./server.db')
        Base.metadata.create_all(bind=self.engine)
        self.session = Session(bind=self.engine)
        self.session.query(ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username: str, ip_address: str, port: str):
        user = self.session.query(Users).filter_by(name=username)
        if user.count():
            user = user.first()
            user.last_login = datetime.datetime.now()
        else:
            user = Users(name=username,
                         active_users=ActiveUsers(ip_address=ip_address, port=port),
                         login_history=LoginHistory(ip=ip_address, port=port))
            self.session.add(user)
            self.session.commit()

    def user_logout(self, username: str):
        user = self.session.query(Users).filter_by(name=username).first()
        self.session.query(ActiveUsers).filter_by(user_id=user.id).delete()
        self.session.commit()

    def users_list(self):
        return self.session.query(Users.name,
                                  Users.last_login).all()

    def active_users_list(self):
        return self.session.query(Users.name,
                                  ActiveUsers.ip_address,
                                  ActiveUsers.port,
                                  ActiveUsers.login_time).join(Users).all()

    def login_history(self):
        return self.session.query(Users.name,
                                  LoginHistory.ip,
                                  LoginHistory.port,
                                  LoginHistory.date_time).join(Users).all()


if __name__ == '__main__':
    database = ServerStorage()
    database.user_login(username='John', ip_address='1213', port='12312')
    database.user_login(username='Richard', ip_address='127.0.0.1', port='8000')
    database.user_logout(username='John')
    print(database.users_list())
    print(database.active_users_list())
    print(database.login_history())
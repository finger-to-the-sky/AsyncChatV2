from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import Base, Contacts, KnownUsers, MessageHistory


class ClientDatabase:

    def __init__(self, name):
        self.name = name
        self.engine = create_engine(f'sqlite:///./{name}.db')
        Base.metadata.create_all(bind=self.engine)
        self.session = Session(self.engine)
        self.session.query(Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        if not self.session.query(Contacts).filter_by(name=contact).count():
            new_contact = Contacts(name=contact)
            self.session.add(new_contact)
            self.session.commit()

    def del_contact(self, contact):
        self.session.query(Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        self.session.query(KnownUsers).delete()
        for user in users_list:
            self.session.add(KnownUsers(username=user))
        self.session.commit()

    def save_message(self, from_user, to_user, message):
        new_message = MessageHistory(from_user=from_user, to_user=to_user, message=message)
        self.session.add(new_message)
        self.session.commit()

    def get_contacts(self):
        return [contact[0] for contact in self.session.query(Contacts.name).all()]

    def get_users(self):
        return [user[0] for user in self.session.query(KnownUsers.username).all()]

    def check_user(self, user):
        if self.session.query(KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        if self.session.query(Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, from_who=None, to_who=None):
        query = self.session.query(MessageHistory)
        if from_who:
            query = query.filter_by(from_user=from_who)
        if to_who:
            query = query.filter_by(to_user=to_who)
        return [(history_row.from_user, history_row.to_user, history_row.message, history_row.date)
                for history_row in query.all()]


if __name__ == '__main__':
    test_db = ClientDatabase('test1')
    for i in ['test3', 'test4', 'test5']:
        test_db.add_contact(i)
    test_db.add_contact('test4')
    test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    test_db.save_message('test1', 'test2', f'Привет! я тестовое сообщение от {datetime.now()}!')
    test_db.save_message('test2', 'test1', f'Привет! я другое тестовое сообщение от {datetime.now()}!')
    print(test_db.get_contacts())
    print(test_db.get_users())
    print(test_db.check_user('test1'))
    print(test_db.check_user('test10'))
    print(test_db.get_history('test2'))
    print(test_db.get_history(to_who='test2'))
    print(test_db.get_history('test3'))
    test_db.del_contact('test4')
    print(test_db.get_contacts())

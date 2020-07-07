from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_today_tasks(db_session):
    print(f'\nToday {datetime.today().day} {datetime.today().strftime("%b")}:')
    tasks = db_session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if len(tasks) == 0:
        print('Nothing to do!\n')
    else:
        for index, doing in enumerate(tasks):
            print(str(index + 1) + '. ' + doing.task + '\n')


def get_tasks(db_session, date):
    print(f'\n{week_days[date.weekday()]} {date.day} {date.strftime("%b")}:')
    tasks = db_session.query(Table).filter(Table.deadline == date).all()
    if len(tasks) == 0:
        print('Nothing to do!\n')
    else:
        for index, doing in enumerate(tasks):
            print(str(index + 1) + '. ' + doing.task)
        print()


def get_weekly_tasks(db_session):
    start_date = datetime.today().date()
    for i in range(7):
        get_tasks(db_session, start_date + timedelta(days=i))


def get_all_tasks(db_session):
    print('\nAll tasks:')
    for index, task in enumerate(db_session.query(Table).order_by(Table.deadline)):
        print(f'{index + 1}. {task}. {task.deadline.day} {task.deadline.strftime("%b")}')
    print()


def get_missed_tasks(db_session):
    print('\nMissed tasks:')
    tasks = db_session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    if len(tasks) == 0:
        print('Nothing is missed!')
    else:
        for index, task in enumerate(tasks):
            print(f'{index + 1}. {task}. {task.deadline.day} {task.deadline.strftime("%b")}')
    print()


def delete_task(db_session):
    tasks = db_session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    if len(tasks) == 0:
        print('Nothing to delete')
    else:
        print('\nChose the number of the task you want to delete:')
        for index, task in enumerate(tasks):
            print(f'{index + 1}. {task}. {task.deadline.day} {task.deadline.strftime("%b")}')
        number = int(input())
        db_session.delete(tasks[number - 1])
        db_session.commit()
        print('The task has been deleted!\n')


def add_task(db_session):
    print('Enter task')
    task_text = input()
    print('Enter deadline')
    deadline = input()
    new_task = Table(task=task_text, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
    db_session.add(new_task)
    db_session.commit()
    print('The task has been added!\n')


menu_text = ('1) Today\'s tasks\n'
             '2) Week\'s tasks\n' 
             '3) All tasks\n'
             '4) Missed tasks\n'
             '5) Add task\n'
             '6) Delete task\n'
             '0) Exit')
print(menu_text)
command = input()
while command != '0':
    if command == '1':
        get_today_tasks(session)
    elif command == '2':
        get_weekly_tasks(session)
    elif command == '3':
        get_all_tasks(session)
    elif command == '4':
        get_missed_tasks(session)
    elif command == '5':
        add_task(session)
    elif command == '6':
        delete_task(session)
    print(menu_text)
    command = input()
print('\nBye!')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    i_d = Column(Integer, name="id", primary_key=True, autoincrement=True)
    task = Column(String, name="task")
    deadline = Column(Date, name="deadline", default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


class TodoList:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def show_today(self):
        rows = self.session.query(Task).filter(Task.deadline == datetime.today().date()).all()
        return rows

    def add_task(self, descr, deadline):
        row = Task(task=descr, deadline=deadline)
        self.session.add(row)
        self.session.commit()

    def week_tasks(self):
        tod = datetime.today().date()
        rows = self.session.query(Task).filter(Task.deadline <= tod + timedelta(days=7)).order_by(Task.deadline).all()
        return rows

    def all_tasks(self):
        rows = self.session.query(Task).order_by(Task.deadline).all()
        return rows

    def missed_tasks(self):
        tod = datetime.today().date()
        rows = self.session.query(Task).filter(Task.deadline < tod).order_by(Task.deadline).all()
        return rows

    def delete_task(self, row):
        self.session.delete(row)
        self.session.commit()


def all_tasks(tasks):
    print("All tasks:")
    if not tasks:
        print("Nothing to do!")
    else:
        for i in range(len(tasks)):
            print(f"{i + 1}) {tasks[i]}. {tasks[i].deadline.strftime('%d %b')}".replace(' 0', ' '))


if __name__ == "__main__":
    todo = TodoList()
    while True:
        print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
""")
        n = int(input())
        if n == 1:
            print(f"Today {datetime.today().strftime('%d %b')}")
            today = todo.show_today()
            if not today:
                print("Nothing to do!")
            else:
                for i in range(len(today)):
                    print(f"{i + 1})", today[i])
        elif n == 2:
            tasks = todo.week_tasks()
            curr = datetime.today().date()
            for _i in range(7):
                print()
                to_tasks = [x for x in tasks if x.deadline == curr]
                print(curr.strftime("%A %d %b"))
                if not to_tasks:
                    print("Nothing to do!")
                else:
                    for i in range(len(to_tasks)):
                        print(f"{i + 1})", to_tasks[i])
                curr += timedelta(days=1)
        elif n == 3:
            tasks = todo.all_tasks()
            all_tasks(tasks)
        elif n == 4:
            tasks = todo.missed_tasks()
            print("Missed tasks:")
            if not tasks:
                print("Nothing is missed!")
            else:
                for i in range(len(tasks)):
                    print(f"{i + 1}) {tasks[i]}. {tasks[i].deadline.strftime('%d %b')}".replace(' 0', ' '))
        elif n == 5:
            task = input("Enter task\n")
            deadline = datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")
            todo.add_task(task, deadline)
            print("The task has been added!")
        elif n == 6:
            tasks = todo.all_tasks()
            if not tasks:
                print("Nothing to delete")
            else:
                print("Choose the number of task you want to delete:")
                all_tasks(tasks)
                t = int(input())
                todo.delete_task(tasks[t - 1])
        else:
            break
        print()
print('Bye!')

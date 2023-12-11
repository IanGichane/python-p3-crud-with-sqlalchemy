#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.orm import declarative_base,sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'),
        UniqueConstraint(
            'email',
            name='unique_email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12')
    )

    Index('index_name', 'name')

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    session = sessionmaker(bind=engine)
    session = session()

    #CREATE
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    # session.add(albert_einstein)
    session.bulk_save_objects([albert_einstein,alan_turing])



    #READ
    # students = session.query(Student)
    students = session.query(Student).all()

    # Selecting Only Certain Columns

    names = [name for name in session.query(Student.name)]
    print(names)

    # Ordering

    students_by_name = [student for student in session.query(
            Student.name).order_by(
            Student.name)]

    print(students_by_name)

    #To sort results in descending order, we need to use the desc()

    students_by_grade_desc = [student for student in session.query(
            Student.name, Student.grade).order_by(
            desc(Student.grade))]

    print(students_by_grade_desc)


    #To limit your result set to the first x records, you can use the limit() method:

    oldest_student = [student for student in session.query(
            Student.name, Student.birthday).order_by(
            desc(Student.grade)).limit(1)]

    print(oldest_student)

    # The first() method is a quick and easy way to execute a limit(1) statement and does not require a list interpretation:

    oldest_student2 = session.query(
            Student.name, Student.birthday).order_by(
            desc(Student.grade)).first()

    print(oldest_student2)

    # Importing func from sqlalchemy gives us access to common SQL operations through functions like sum() and count(). As these operations act upon columns, we carry them out through wrapping a Column object passed to the query() method:

    student_count = session.query(func.count(Student.id)).first()

    print(student_count)


    # Filtering
    # Retrieving specific records requires use of the filter() method. A typical filter() statement has a column, a standard operator, and a value. It is possible to chain multiple filter() statements together, though it is typically easier to read with comma-separated clauses inside of one filter() statement.

    query = session.query(Student).filter(
        Student.grade <= 7)

    for record in query:
        print(record.name)
    

    # Updating Data
    # There are several ways to update data using SQLAlchemy ORM. The simplest is to use Python to modify objects directly and then commit those changes through the session. For instance, let's say that a new school year is starting and our students all need to be moved up a grade:
    # for student in session.query(Student):
    #     student.grade += 1

    # print([(student.name,
    #     student.grade) for student in session.query(Student)])

    


    # The update() method allows us to update records without creating objects beforehand. Here's how we would carry out the same statement with update():


    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

    session.commit()

    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")
    # # read
    # # print([student for student in students])
    # print(students)

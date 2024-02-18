from atexit import _clear
from cgitb import reset
from turtle import onclick
import streamlit as st

class Student:
    def __init__(self, name, father_name, age, class_):
        self.name = name
        self.father_name = father_name
        self.age = age
        self.class_ = class_

students = []
total_students = 0
seats = {
    1: 20, 2: 20, 3: 20, 4: 20, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20, 10: 20, 11: 20, 12: 20
}

def add_student():
    
    st.write(seats)
    with st.form(key='add_student_form', clear_on_submit = True):
        invalid = False
        name = st.text_input("Enter the student's name:")
        father_name = st.text_input("Enter the student's father's name:")
        age = st.number_input("Enter the student's age:", min_value=6, max_value=120, step=1)

        if age >= 6 and age <= 9:
            options = [f"Grade {class_} (seats available: {seats[class_]})" for class_ in range(1, 5)]
            class_index = st.selectbox("Select the class:", options)
            class_ = int(class_index.split()[1])  # Extracting class number from the selected option
            seats[class_] -= 1
            st.write(seats)
        elif age < 14 and age >= 10:
            options = [f"Grade {class_} (seats available: {seats[class_]})" for class_ in range(5, 9)]
            class_index = st.selectbox("Select the class:", options)
            class_ = int(class_index.split()[1])  # Extracting class number from the selected option
            seats[class_] -= 1
        elif age < 18 and age > 10:
            options = [f"Grade {class_} (seats available: {seats[class_]})" for class_ in range(9, 11)]
            class_index = st.selectbox("Select the class:", options)
            class_ = int(class_index.split()[1])  # Extracting class number from the selected option
            if class_ == 9 or class_ == 10:
                seats[class_] -= 1
            else:
                st.error("Invalid Class number")
                return
        elif age <= 22 and age >= 18:
            options = [f"Grade {class_} (seats available: {seats[class_]})" for class_ in range(11, 13)]
            class_index = st.selectbox("Select the class:", options)
            class_ = int(class_index.split()[1])  # Extracting class number from the selected option
            seats[class_] -= 1
        else:
            st.error("There are no classes available for the entered age.")
            return

        submit_button = st.form_submit_button(label='Add Student')
        if submit_button == True:
            if name == "" or father_name == "":
                if name == "" and father_name == "":
                    invalid = st.error("You have not entered the father's name correctly")
                    invalid = st.error("You have not entered the name correctly")
                elif name == "":
                    invalid = st.error("You have not entered the name correctly")
                else:
                    invalid = st.error("You have not entered the father's name correctly")
            else:
                if submit_button:
                    if age >= 6 and age <= 9:
                        seats[class_] -= 1
                    elif age >= 10 and age < 14:
                        seats[class_] -= 1
                    elif age >= 14 and age < 18:
                        seats[class_] -= 1
                    elif age >= 18 and age <= 22:
                        seats[class_] -= 1
                new_student = Student(name, father_name, age, class_)
                students.append(new_student)
                global total_students
                total_students += 1
                st.success(f"Student {name} has been added to Class: {class_}!, with the GR number: {total_students}")
                



                

def view_student():
    gr_no = st.number_input("Enter the GR number of the student:", min_value=1, max_value=total_students, step=1)

    if st.button("View Student"):
        if gr_no < 1 or gr_no > total_students:
            st.error("Invalid GR number.")
            return

        student = students[gr_no - 1]

        st.write(f"Student name: {student.name}")
        st.write(f"Student father's name: {student.father_name}")
        st.write(f"Student age: {student.age}")
        st.write(f"Student class: {student.class_}")

def main():
    st.title("Student Registration Application")
    st.write("Welcome to the Student Registration Application!")

    option = st.selectbox("Select an option:", ["Add a student", "View a student's data"])

    if option == "Add a student":
        add_student()
    elif option == "View a student's data":
        view_student()

if __name__ == "__main__":
    main()

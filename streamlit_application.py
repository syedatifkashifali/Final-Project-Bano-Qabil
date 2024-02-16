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
    1: 20, 2: 20, 3: 20, 4: 20,
    5: 20, 6: 20, 7: 20, 8: 20,
    9: 20, 10: 20, 11: 20, 12: 20
}

def add_student(name1, father_name1, age1, class_):
    global total_students
    valid_classes = []
    if age1 >= 6 and age1 <= 9:
        valid_classes = list(range(1, 5))
    elif age1 < 14 and age1 >= 10:
        valid_classes = list(range(5, 9))
    elif age1 < 18 and age1 > 10:
        valid_classes = list(range(9, 11))
    elif age1 <= 22 and age1 >= 18:
        valid_classes = [11, 12]

    if class_ in valid_classes:
        if seats[class_] > 0:
            total_students += 1
            new_student = Student(name1, father_name1, age1, class_)
            students.append(new_student)
            seats[class_] -= 1  # Corrected line
            st.success(f"Student {name1} has been added to Class: {class_}!, with the GR number: {total_students}")
            return True
        else:
            st.error("No available seats for this class.")
    else:
        st.error("Invalid Class number")
    return False
def view_student(gr_no):
    if gr_no <= total_students:
        student = students[gr_no - 1]
        st.write(f"GR number: {gr_no}")
        st.write(f"Student name: {student.name}")
        st.write(f"Student father's name: {student.father_name}")
        st.write(f"Student age: {student.age}")
        st.write(f"Student class: Grade {student.class_}")
    else:
        st.error("Invalid GR number.")

def main():
    st.title("Student Management System")

    option = st.selectbox("Select an option:", ["Add a student", "View a student's data"])

    if option == "Add a student":
        name = st.text_input("Enter the student's name:")
        father_name = st.text_input("Enter the student's father's name:")
        age = st.number_input("Enter the student's age:", min_value=1, max_value=22, value=1)
        
        valid_classes = []
        if age >= 6 and age <= 9:
            valid_classes = list(range(1, 5))
        elif age < 14 and age >= 10:
            valid_classes = list(range(5, 9))
        elif age < 18 and age > 10:
            valid_classes = list(range(9, 11))
        elif age <= 22 and age >= 18:
            valid_classes = [11, 12]

        class_options = [f"Grade {class_} (seats available: {seats[class_]})" for class_ in valid_classes]
        class_ = st.selectbox("Select the student's class:", class_options)
        if st.button("Add Student"):
            if add_student(name, father_name, age, int(class_.split()[1])):
                name = ""
                father_name = ""
                age = 1
    elif option == "View a student's data":
        if total_students > 0:
            gr_no = st.number_input("Enter the GR number of the student:", min_value=1, max_value=total_students, value=1)
            if st.button("View Student"):
                view_student(int(gr_no))
        else:
            st.warning("No students registered yet.")

if __name__ == "__main__":
    main()

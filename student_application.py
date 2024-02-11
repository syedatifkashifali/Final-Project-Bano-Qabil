#Hi, I am Syed Atif Ali, a student at Bano-Qabil-CIT-PYTHON
#I have created student data manipulating application as my final project by using OOP, loops, and if-else

class Student:
    name = "";
    age = 0;
    def inside (self, name1, age1):
        self.name = name1
        self.age = age1;

students = []
total_students = 0

while True:
    if total_students == 0:
        print("No students registered yet.")
    else:
        print(f"We currently have {total_students} registered students in our application")
    print("")
    print("Enter an option: ")
    print("1. Add a student")
    print("2. View a student's data")
    print("3. Exit the program")
    print("")

    option = int(input())

    if option == 1:
        name1 = input("Enter the student's name: ")
        age1 = int(input("Enter the student's age: "))
        new_student = Student();
        new_student.inside(name1, age1)
        students.append(new_student)
        total_students += 1
        print(f"Student {name1} has been added!, with the roll no: {total_students}")
        print("")

    elif option == 2:
        roll_no = int(input("Enter the roll number of the student: "))
        if roll_no > total_students or roll_no < 1:
            print("Invalid roll number.")
            print("")
        else:
            student = students[roll_no - 1]
            print(f"Student name: {student.name}")
            print(f"Student age: {student.age}")
            print("")

    elif option == 3:
        print("Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")
        print("")


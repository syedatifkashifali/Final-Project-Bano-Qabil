import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_lottie as st_lottie
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import requests



def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def home():
    
    st.markdown("""
    <style>
        .centered-title {
            text-align: center;
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

    # Display the centered and underlined title
    st.markdown("<h1 class='centered-title'>WELCOME 👋</h1>", unsafe_allow_html=True)
    
    
    lottie_hello = load_lottieurl("https://lottie.host/9ac568aa-70c3-4de6-a428-723d7e94497f/Pi0BW1dNnf.json")

    st.lottie(lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        height=400,
        width=None,
        key=None,
    )
    


    # Function to create a SQLite database and tables if they don't exist
    def create_database():
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()
    
        cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        father_name TEXT,
                        age INTEGER,
                        class TEXT
                    )''')
    
        conn.commit()
        conn.close()

    # Function to insert student information into the database
    def insert_student(name, father_name, age, selected_class):
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()
    
        cursor.execute('''INSERT INTO Students (name, father_name, age, class) 
                        VALUES (?, ?, ?, ?)''', (name, father_name, age, selected_class))
        conn.commit()
        conn.close()
    #Function to delete student from database
    def delete_student(student_id):
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM Students WHERE id = ?''', (student_id,))
        conn.commit()
        conn.close()

    #Function to check the if student available in database by id
    def student_exists(student_id):
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student is not None

   
    # Function to get available seats for a selected class
    def get_available_seats(selected_class):
        seats = {1: 20, 2: 20, 3: 30, 4: 40, 5: 50, 6: 50, 7: 50, 8: 50, 9: 50, 10: 50, 11: 50, 12: 50}
        if selected_class == "Grade 10" or "Grade 11" or "Grade 12":
            last_two_keys = sorted(seats.keys())[-2:]  # Get the last two keys of the dictionary
            getseats = seats.get(int(selected_class[-2:]), 0)
        else:
            getseats = seats.get(int(selected_class[-1]), 0)
        return getseats

    # Function to get available seats for all classes
    def get_available_seats_all():
        seats = {1: 20, 2: 20, 3: 30, 4: 40, 5: 50, 6: 50, 7: 50, 8: 50, 9: 50, 10: 50, 11: 50, 12: 50}
        return seats #this function to get seats of all classes


    #Function to get updated live seats
    def current_seats(selected_grade):
        # Connect to the SQLite database
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()

        # Execute SQL query to count occurrences of selected grade
        cursor.execute("SELECT COUNT(*) FROM Students WHERE class = ?", (selected_grade,))
        count = cursor.fetchone()[0]#selecting an updating all seats in class

        # Fetch available seats for the selected grade (assuming get_available_seats is defined elsewhere)
        available_seats = get_available_seats(selected_grade)#updating and returning the selected seats

        # Calculate and return current seats
        current_seats = available_seats - count
        return current_seats #returning updated live seats

    
    
    #Function to update seats in graph
    def update_graph_seats():    
        # Connect to the SQLite database
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()

        # Execute SQL query to count occurrences of each unique grade
        cursor.execute("SELECT class, COUNT(*) FROM Students GROUP BY class")

        # Fetch all results
        grade_counts = cursor.fetchall()
        getseats = get_available_seats_all()
        
        # Print the grade counts
        for grade, count in grade_counts:
            get_available_seats(grade)
            # Split the string by space and take the last part
            numeric_part = int(grade.split()[-1])
            # Convert the numeric part to an integer
            getseats[numeric_part] -= count
        return getseats
    
        # Close the connection
        conn.close()
    
    
    
    # Function to Get basic student information form
    def basic_info():
        with st.form(key="basicform", clear_on_submit = True):#creating form
            std_name = st.text_input("Enter Student Name")
            std_fname = st.text_input("Enter Student's Father Name")
            std_age = st.slider("Enter Student's Age", min_value=6, max_value=22)#creating slider with minimum age 6 and maximum age 22
            if st.form_submit_button("Check Available Seats"):#if button is pressed evaluate
                if std_name == "" or std_fname == "" or std_age == "":#if any of the field empty
                    st.error("Please fill all the input fields.")
                else:
                    st.success("All fields are correct. Proceed to check the seats.")
        return std_name, std_fname, std_age#returning name, father name, and age to get executed further

    # Function to display class selection based on value returned from basic function
    def complex_info(age):
        if 5 < age < 11:
            avail_classes = ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 6"]
        elif 10 < age < 14:
            avail_classes = ["Grade 7", "Grade 8"]
        elif 13 < age < 18:
            avail_classes = ["Grade 9", "Grade 10"]
        else:
            avail_classes = ["Grade 11", "Grade 12"]
        selected_class = st.selectbox(options=["Select an option"] + avail_classes, index=0, label="Select Class")
        return selected_class

    # Create database tables if they don't exist
    create_database()

    # Streamlit UI option menu horizontal
    selected = option_menu(
        menu_title = "Bano-Qabil Student Registration Application",
        options = ["Add Student", "View Student", "Delete Student", "All Records"],
        icons = ["house", "person-lines-fill", "person-x", "journal-bookmark-fill"],
        orientation = "horizontal",
    )

    #decribing first option of menu
    if selected == "Add Student":
        st.write("**Add Student**")#Bold text of selected option
        name, father_name, age = basic_info()#calling and getting returned value from basic function to variables
        if name and father_name and age:#this block will execute when all values are present
            selected_class = complex_info(age)#getting returned value from complex function to variable
            if selected_class != "Select an option":#it's basically execute when any option is selected rather than placeholder
                #calling current seats and getting returned value
                current_seats = current_seats(selected_class)
                st.warning(f"Seats Available for Selected Grade: {current_seats}")#awaring about seats before adding
                if st.button("Add"):
                    if current_seats == 0:
                        st.error("Seats are full")
                    else:
                        st.success("Student Added Succesfully!")#giving success message
                        insert_student(name, father_name, age, selected_class)#inserting students data
                
    #Second option of menu
    elif selected == "View Student":
        st.write("**View Student by Grade Number**")
        with st.form(key="viewform"):
            grade_number = st.number_input("Enter Grade Number", min_value=1, max_value=12)
            if st.form_submit_button("View Students"):
                conn = sqlite3.connect("student_database.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Students WHERE class = ?", (f"Grade {grade_number}",))#% representing string constant variable
                students = cursor.fetchall()
                conn.close()
                if not students:#this block execute when there is no available students in provided grade
                    st.warning("No Students Found For The Entered Grade Number.")
                else:
                    st.success("Students Found:")
                    # Display students in a table with customized column headings
                    st.write("**Student Records**")#title basically
                    table_data = [["Gr no", "Student Name", "Father Name", "Student Age", "Student Grade"]]#making first row for heading
                    table_data.extend(students)#adding heading row to database table
                    st.table(table_data)#showing database table

    #Third option of menu
    elif selected == "Delete Student":
        st.write("**Delete Student**")
        with st.form(key="deleteform"):
            student_id = st.number_input("Enter Student ID to delete", value = 0, step = 1, format = "%d")#value is default zero and step means increment 1 format %d means integer type
            if st.form_submit_button("Delete"):
                if not student_id:
                    st.error("Please enter a valid Student ID.")
                elif not student_exists(student_id):
                    st.error("No student found with the entered ID.")
                else:
                    delete_student(student_id)
                    st.success("Student deleted successfully.")  
    
    
    #Fourth function of menu    
    else:#Function to display all data
        conn = sqlite3.connect("student_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, father_name, age, class FROM Students")
        students = cursor.fetchall()
        conn.close()
    
    

        if not students:
            st.write("No students found.")
        else:
            # Display students in a table with customized column headings
            st.write("**Student Records**")#title basically
            table_data = [["Gr no", "Student Name", "Father Name", "Student Age", "Student Grade"]]#making first row for heading
            table_data.extend(students)#adding heading row to database table
            st.table(table_data)#showing database table
        
            # Provide option to download CSV file of student records
        csv_export = pd.DataFrame(students, columns=["Gr no", "Student Name", "Father Name", "Student Age", "Student Grade"])
        st.download_button(
            label="Download Student Records (CSV)",
            data=csv_export.to_csv(index=False),
            file_name="student_records.csv",
            mime="text/csv" #Multipurpose internet mail extension used to specify type of file which will be downloaded
        )

        # Update available seats data
        getseats = update_graph_seats()

        # Plot the bar graph with precise settings
        plt.figure(figsize=(10, 6))  # Set the figure size for better visibility

        bars = plt.bar(getseats.keys(), getseats.values(), color='skyblue', edgecolor='black', linewidth=1.5)

        # Add data labels above each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.2, f'{height}', ha='center', va='bottom', fontsize=10)

        # Add labels and title with precise font sizes
        plt.xlabel('Class', fontsize=12)
        plt.ylabel('Seats Available', fontsize=12)
        plt.title('Available Seats for All Classes', fontsize=14)

        # Add grid lines for better readability
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation=45, fontsize=10)

        # Show the plot in Streamlit
        st.pyplot(plt)
    

        # Provide button to download graph as PNG image
        st.markdown("""---""")

        # Save the plot to a bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Convert the plot to a base64 string
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Create a download button for the plot image
        st.download_button(
            label="Download Graph as PNG Image",
            data=buffer,
            file_name="available_seats.png",
            mime="image/png"
        )


    

def about():
    
    # Load Lottie animation
    lottie_about = load_lottieurl("https://lottie.host/a4b50922-dc97-428c-95d7-7d549638ee62/iRpe1oQzk2.json")

    # Display Lottie animation
    st.lottie(lottie_about, speed=1, reverse=False, loop=False, quality="medium", height=400, width=None)

    # Add your content
    st.write("""
        Hey there! 👋 I'm Syed Atif Ali, a passionate secondary student from Pakistan with a keen interest in programming and technology. Programming has always been my playground, and I find joy in exploring various programming languages, including Python, C#, and C++.

        ###Our Members
        - **Mubashir** Contact no: 0336-3352993
        - **Hammad:** Contact no: 0340-0246683


        ### Skills & Expertise
        - **Python:** Python is my go-to language for its simplicity and versatility. I love how I can use it for anything from web development to data analysis.
        - **C#:** As a versatile language, C# allows me to develop robust applications, especially for the Windows platform.
        - **C++:** I enjoy diving into the intricacies of C++ for high-performance applications and system-level programming.

        ### Journey & Aspirations
        My journey in programming started at a young age, fueled by curiosity and a desire to create. I'm currently honing my skills as a secondary student while exploring new avenues in technology.

        While I don't have a specific goal in mind, my mindset is geared towards continuous growth. I believe in setting milestones rather than fixed goals, always striving to learn, adapt, and innovate. My bucket list includes becoming a data scientist, leveraging my programming skills to extract insights from vast datasets and make data-driven decisions.

        ### Why Programming?
        Programming, for me, is more than just writing code. It's about problem-solving, creativity, and the thrill of turning ideas into reality. I'm fascinated by the endless possibilities that technology offers and the impact it can have on the world.

        ### Let's Connect!
        If you share a passion for programming or want to explore the exciting world of technology together, feel free to reach out. Let's collaborate, learn, and grow together!
    """)


def contact():
    st.title("Contact Page")
    
    # Load Lottie animation
    lottie_contact = load_lottieurl("https://lottie.host/6953afeb-c2b3-4ed8-8f20-33614a276a9b/bSaAZy50gu.json")
    lottie_mail = load_lottieurl("https://lottie.host/8f76b3be-1fbc-40a0-a4ae-adc137378bce/5yHOlUSOM6.json")
    lottie_sm = load_lottieurl("https://lottie.host/a6c0db26-9df7-4672-ac97-7832b7286946/Hgg5Grnn8O.json")
    lottie_phone = load_lottieurl("https://lottie.host/804c12e5-4869-49b7-9cf4-b22edd305840/uiHWLfWRvV.json")
    
    # Display Lottie animation
    st.lottie(lottie_contact, speed=1, reverse=False, loop=True, quality="medium", height=400, width=None)

    st.subheader("Contact Me:")
    st.write("Feel free to reach out to me via any of the methods above. I'm always open to discussing new opportunities, projects, or just having a chat!")
    st.markdown("<hr></hr>", unsafe_allow_html = True)
    
    st.subheader("Email:")
    st.lottie(lottie_mail, speed=1, reverse=False, loop=True, quality="medium", height=200, width=None)
    st.markdown("[atif@fastcompk.com](mailto:atif@fastcompk.com) <h5>(FastcomPK Webmail)</h5>", unsafe_allow_html = True)
    st.markdown("[corruptedgamerz977@gmail.com](mailto:corruptedgamerz977@gmail.com) <h5>(Gmail)</h5>", unsafe_allow_html = True)
    st.markdown("<hr></hr>", unsafe_allow_html = True)

    st.subheader("Social Media:")
    st.lottie(lottie_sm, speed=1, reverse=False, loop=True, quality="medium", height=200, width=None)
    st.markdown("[<h5>LinkedIn</h5>](https://www.linkedin.com/in/atif-ali-3b23812b4)", unsafe_allow_html = True)
    st.markdown("[<h5>Twitter</h5>](https://twitter.com/s_atifkashifali)", unsafe_allow_html = True)
    st.markdown("[<h5>Thread</h5>](https://twitter.com/syedatifkashifali)", unsafe_allow_html = True)
    st.markdown("<hr></hr>", unsafe_allow_html = True)

    st.subheader("Phone/WhatsApp:")
    st.lottie(lottie_phone, speed=1, reverse=False, loop=True, quality="medium", height=200, width=None)
    st.write("<h5>0315-2849277</h5>", unsafe_allow_html = True)
    st.markdown("<hr></hr>", unsafe_allow_html = True)
    

def main():
    
    # Company logo
    st.sidebar.image("download.png", use_column_width=True)
    
    # Create a navigation bar
    nav = st.sidebar.radio("Navigation", ["Home", "About", "Contact"])

    # Display the selected page
    if nav == "Home":
        home()
    elif nav == "About":
        about()
    elif nav == "Contact":
        contact()
        

if __name__ == "__main__":
    main()

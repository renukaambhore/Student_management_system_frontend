import requests
import gradio as gr


# FastAPI URL
API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# STUDENT CLASS
# --------------------------------------------------

class Student:

    def __init__(self, student_id, name, course, marks):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.marks = marks

    def display_student(self):

        return (
            f"Student ID : {self.student_id}\n"
            f"Name       : {self.name}\n"
            f"Course     : {self.course}\n"
            f"Marks      : {self.marks}"
        )


# --------------------------------------------------
# STUDENT MANAGEMENT SYSTEM
# --------------------------------------------------

class StudentManagementSystem:

    # CREATE
    def create_student(self, name, course, marks):

        if not name:
            return "Please enter Student Name."

        if not course:
            return "Please enter Course."

        if marks is None:
            return "Please enter Marks."

        try:

            response = requests.post(
                f"{API_URL}/students",
                params={
                    "name": name,
                    "course": course,
                    "marks": int(marks)
                }
            )

            if response.status_code == 200:
                return "Student created successfully! "

            return f"Error: {response.text}"

        except requests.exceptions.ConnectionError:
            return " FastAPI server is not running."


    # READ
    def read_students(self):

        try:

            response = requests.get(
                f"{API_URL}/students"
            )

            if response.status_code != 200:
                return f"Error: {response.text}"

            result = response.json()

            students = result["data"]

            if not students:
                return "No students found."

            output = ""

            for student in students:

                student_object = Student(
                    student["id"],
                    student["name"],
                    student["course"],
                    student["marks"]
                )

                output += (
                    student_object.display_student()
                    + "\n"
                    + "-" * 35
                    + "\n"
                )

            return output

        except requests.exceptions.ConnectionError:
            return " FastAPI server is not running."


    # UPDATE
    def update_student(
        self,
        student_id,
        name,
        course,
        marks
    ):

        if not student_id:
            return "Please enter Student ID."

        if not name:
            return "Please enter Name."

        if not course:
            return "Please enter Course."

        if marks is None:
            return "Please enter Marks."

        try:

            response = requests.put(
                f"{API_URL}/students/{int(student_id)}",
                params={
                    "name": name,
                    "course": course,
                    "marks": int(marks)
                }
            )

            if response.status_code == 200:
                return "Student updated successfully! "

            return f"Error: {response.text}"

        except requests.exceptions.ConnectionError:
            return " FastAPI server is not running."


    # DELETE
    def delete_student(self, student_id):

        if not student_id:
            return "Please enter Student ID."

        try:

            response = requests.delete(
                f"{API_URL}/students/{int(student_id)}"
            )

            if response.status_code == 200:
                return "Student deleted successfully!"

            return f"Error: {response.text}"

        except requests.exceptions.ConnectionError:
            return " FastAPI server is not running."


# Create object
system = StudentManagementSystem()


# --------------------------------------------------
#  CSS
# --------------------------------------------------

custom_css = """

.gradio-container {
    background-color: #FFF7F8 !important;
    font-family: Arial, sans-serif;
}

.header {
    background-color: #F4C2C2;
    padding: 22px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
}

.header h1 {
    color: #6B3E45 !important;
    font-size: 32px;
}

.header p {
    color: #7D4B54 !important;
}

button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.pink-button {
    background-color: #F4C2C2 !important;
    color: #5C343A !important;
    border: 1px solid #E8A9AD !important;
}

.pink-button:hover {
    background-color: #E8A9AD !important;
    color: white !important;
}

.delete-button {
    background-color: #E8A9AD !important;
    color: white !important;
}

input,
textarea {
    border: 1px solid #F4C2C2 !important;
    border-radius: 10px !important;
    background-color: white !important;
}

label {
    color: #6B3E45 !important;
    font-weight: 600 !important;
}

"""


# --------------------------------------------------
# GRADIO UI
# --------------------------------------------------

with gr.Blocks(
    title="Student Management System",
    css=custom_css,
    theme=gr.themes.Soft()
) as app:

    gr.HTML(
        """
        <div class="header">
            <h1>Student Management System</h1>
        
        </div>
        """
    )


    # --------------------------------------------------
    # CREATE TAB
    # --------------------------------------------------

    with gr.Tab("Create"):

        create_name = gr.Textbox(
            label="Student Name",
            placeholder="Enter Student Name"
        )

        create_course = gr.Textbox(
            label="Course",
            placeholder="Enter Course"
        )

        create_marks = gr.Number(
            label="Marks",
            placeholder="Enter Marks",
            precision=0
        )

        create_button = gr.Button(
            "Create Student ",
            elem_classes="pink-button"
        )

        create_output = gr.Textbox(
            label="Result"
        )

        create_button.click(
            fn=system.create_student,
            inputs=[
                create_name,
                create_course,
                create_marks
            ],
            outputs=create_output
        )


    # --------------------------------------------------
    # READ TAB
    # --------------------------------------------------

    with gr.Tab(" Read"):

        read_button = gr.Button(
            "Show All Students ",
            elem_classes="pink-button"
        )

        read_output = gr.Textbox(
            label="Students",
            lines=10
        )

        read_button.click(
            fn=system.read_students,
            inputs=[],
            outputs=read_output
        )


    # --------------------------------------------------
    # UPDATE TAB
    # --------------------------------------------------

    with gr.Tab("Update"):

        update_id = gr.Number(
            label="Student ID",
            precision=0
        )

        update_name = gr.Textbox(
            label="New Name"
        )

        update_course = gr.Textbox(
            label="New Course"
        )

        update_marks = gr.Number(
            label="New Marks",
            precision=0
        )

        update_button = gr.Button(
            "Update Student ✏️",
            elem_classes="pink-button"
        )

        update_output = gr.Textbox(
            label="Result"
        )

        update_button.click(
            fn=system.update_student,
            inputs=[
                update_id,
                update_name,
                update_course,
                update_marks
            ],
            outputs=update_output
        )


    # --------------------------------------------------
    # DELETE TAB
    # --------------------------------------------------

    with gr.Tab(" Delete"):

        delete_id = gr.Number(
            label="Student ID",
            precision=0
        )

        delete_button = gr.Button(
            "Delete Student ",
            elem_classes="delete-button"
        )

        delete_output = gr.Textbox(
            label="Result"
        )

        delete_button.click(
            fn=system.delete_student,
            inputs=delete_id,
            outputs=delete_output
        )


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    app.launch()
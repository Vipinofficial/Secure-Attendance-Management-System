import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import hashlib
from io import StringIO

# File names
USER_CREDENTIALS_FILE = "user_credentials.json"
UNIVERSITY_CODES_FILE = "university_codes.json"
JSON_FILE = "secure_data.json"
CSV_FILE = "dataofmonth.csv"
ADMIN_CREDENTIALS_FILE = "admin_credentials.json"  # File to store admin credentials

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load user credentials
def load_credentials():
    if os.path.exists(USER_CREDENTIALS_FILE):
        with open(USER_CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

# Save user credentials
def save_credentials(credentials):
    with open(USER_CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

# Load university codes
def load_university_codes():
    if os.path.exists(UNIVERSITY_CODES_FILE):
        with open(UNIVERSITY_CODES_FILE, "r") as file:
            return json.load(file)
    else:
        return []

# Save university codes
def save_university_codes(codes):
    with open(UNIVERSITY_CODES_FILE, "w") as file:
        json.dump(codes, file)

# Load admin credentials (predefined)
def load_admin_credentials():
    return {"admin": "admin123"}  # Hardcoded admin credentials for simplicity

# Load attendance data
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    else:
        return {"institution": "", "students": [], "subjects": [], "timetable": {}, "attendance": {}, "holidays": []}

# Save attendance data
def save_data(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file)

# Function to calculate attendance percentage
def calculate_attendance_percentage(data):
    percentages = {}
    total_classes = len(data["attendance"])
    for student in data["students"]:
        total_attended = 0
        for date, subjects in data["attendance"].items():
            for subject, records in subjects.items():
                if student in records and records[student] == "Present":
                    total_attended += 1
        percentages[student] = (total_attended / total_classes) * 100 if total_classes > 0 else 0
    return percentages

# Function to export attendance to CSV and create a downloadable file
def export_attendance_to_csv(data):
    attendance_records = []
    for date, subjects in data["attendance"].items():
        for subject, records in subjects.items():
            for student, status in records.items():
                attendance_records.append({"Date": date, "Subject": subject, "Student Name": student, "Status": status})

    if attendance_records:
        df_attendance = pd.DataFrame(attendance_records)

        # Create a CSV in memory
        csv_buffer = StringIO()
        df_attendance.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        # Provide a download button for the CSV
        st.download_button(
            label="Download Attendance as CSV",
            data=csv_data,
            file_name="attendance.csv",
            mime="text/csv"
        )
        st.success(f"Attendance data prepared for download.")
    else:
        st.warning("No attendance records to export.")

# Main app
st.title("Secure Attendance Management System")

# Initialize data
credentials = load_credentials()
university_codes = load_university_codes()
data = load_data()

# User authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# Admin login state
admin_credentials = load_admin_credentials()

# Login and Signup
if not st.session_state.authenticated and not st.session_state.admin_authenticated:
    menu = st.sidebar.radio("Menu", ["Login", "Signup", "Admin Login", "View Attendance"])

    if menu == "Signup":
        st.header("Signup")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        university_code_input = st.text_input("University Code")  # New field for university code

        if st.button("Create Account"):
            if username in credentials:
                st.error("Username already exists. Choose a different one.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif university_code_input not in university_codes:
                st.error("Invalid university code. Please enter the correct code.")
            else:
                credentials[username] = hash_password(password)
                save_credentials(credentials)
                st.success("Account created successfully. Please log in.")

    elif menu == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            hashed_password = hash_password(password)
            if username in credentials and credentials[username] == hashed_password:
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")

    elif menu == "Admin Login":
        st.header("Admin Login")
        admin_username = st.text_input("Admin Username")
        admin_password = st.text_input("Admin Password", type="password")

        if st.button("Login as Admin"):
            if admin_username == "admin" and admin_password == admin_credentials["admin"]:
                st.session_state.admin_authenticated = True
                st.success("Admin login successful.")
            else:
                st.error("Invalid admin credentials.")

else:
    # Display logout and the authenticated user
    st.sidebar.write(f"Logged in as: {st.session_state.current_user if st.session_state.authenticated else 'Admin'}")
    st.sidebar.button("Logout", on_click=lambda: [st.session_state.pop("authenticated", None), st.session_state.pop("current_user", None), st.session_state.pop("admin_authenticated", None)])

    # Admin menu options
    menu = st.sidebar.radio(
        "Menu", 
        ["Mark Attendance", "View Attendance", "Add Students", "Add Subjects", "Manage Timetable"] + 
        (["Manage University Codes"] if st.session_state.admin_authenticated else [])
    )

    # Manage University Codes (Admin only)
    if menu == "Manage University Codes" and st.session_state.admin_authenticated:
        st.header("Manage University Codes")
        st.write("### Current Codes")
        st.write(university_codes)

        new_code = st.text_input("Enter New University Code")
        if st.button("Add Code"):
            if new_code and new_code not in university_codes:
                university_codes.append(new_code)
                save_university_codes(university_codes)
                st.success(f"University code '{new_code}' added successfully.")
            else:
                st.error("Code is invalid or already exists.")

        remove_code = st.selectbox("Select Code to Remove", university_codes)
        if st.button("Remove Code"):
            if remove_code in university_codes:
                university_codes.remove(remove_code)
                save_university_codes(university_codes)
                st.success(f"University code '{remove_code}' removed successfully.")

    # Mark Attendance
    elif menu == "Mark Attendance":
        st.header("Mark Attendance")
        date = st.date_input("Select Date", datetime.now())
        day = date.strftime("%A")
        subjects = data["timetable"].get(day, [])
        st.write(f"### Subjects for {day}")
        if subjects:
            subject = st.selectbox("Select Subject", subjects)
            attendance = {}
            for student in data["students"]:
                status = st.radio(f"{student}", ["Present", "Absent"], key=f"{student}_{subject}_{date}")
                attendance[student] = status
            if st.button("Submit Attendance"):
                date_str = date.strftime("%Y-%m-%d")
                if date_str not in data["attendance"]:
                    data["attendance"][date_str] = {}
                data["attendance"][date_str][subject] = attendance
                save_data(data)
                st.success(f"Attendance for {subject} on {date_str} marked successfully.")

    # View Attendance
    elif menu == "View Attendance":
        st.header("View Attendance")
        if not data["attendance"]:
            st.warning("No attendance records found.")
        else:
            # Option to filter by date
            filter_date = st.date_input("Filter by Date (optional)")
            filter_date_str = filter_date.strftime("%Y-%m-%d") if filter_date else None

            # Option to filter by subject
            subjects = data["subjects"]
            filter_subject = st.selectbox("Filter by Subject (optional)", ["All"] + subjects)

            # Display attendance percentages
            percentages = calculate_attendance_percentage(data)
            st.write("### Attendance Percentages")
            df_percentages = pd.DataFrame(list(percentages.items()), columns=["Student Name", "Attendance Percentage"])
            st.table(df_percentages)

            # Display detailed attendance records
            st.write("### Detailed Attendance Data")
            attendance_records = []
            for date, subjects in data["attendance"].items():
                if filter_date_str and date != filter_date_str:
                    continue
                for subject, records in subjects.items():
                    if filter_subject != "All" and subject != filter_subject:
                        continue
                    for student, status in records.items():
                        attendance_records.append({"Date": date, "Subject": subject, "Student Name": student, "Status": status})

            if attendance_records:
                df_attendance = pd.DataFrame(attendance_records)
                st.dataframe(df_attendance)
            else:
                st.info("No matching attendance records found.")

            # Export attendance to CSV with download button
            export_attendance_to_csv(data)

    # Add Students
    elif menu == "Add Students":
        st.header("Add Students")
        new_student = st.text_input("Enter Student Name")
        if st.button("Add Student"):
            if new_student:
                data["students"].append(new_student)
                save_data(data)
                st.success(f"Student '{new_student}' added successfully.")

    # Add Subjects
    elif menu == "Add Subjects":
        st.header("Add Subjects")
        new_subject = st.text_input("Enter Subject Name")
        if st.button("Add Subject"):
            if new_subject:
                data["subjects"].append(new_subject)
                save_data(data)
                st.success(f"Subject '{new_subject}' added successfully.")

    # Manage Timetable
    elif menu == "Manage Timetable":
        st.header("Manage Timetable")
        day = st.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        # Dropdown for selecting subjects
        if data["subjects"]:
            subjects = st.multiselect("Select Subjects for the Day", data["subjects"])
        else:
            subjects = st.text_input("Enter Subjects for the Day (comma separated)").split(',')
        
        if st.button("Save Timetable"):
            if subjects:
                data["timetable"][day] = [subject.strip() for subject in subjects]
                save_data(data)
                st.success(f"Timetable for {day} updated successfully.")
            else:
                st.error("Please select or enter at least one subject.")

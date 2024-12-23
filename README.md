# Attendance and Project Management System

This is a web-based application built using Streamlit that facilitates efficient management of employees, projects, attendance, and HR functionalities for a company. It includes modules like Core HR, Payroll, Time and Attendance, Performance Management, Hiring, Analytics, and PSA (Professional Services Automation).

## Features

### Core HR
- Manage employee details and personal information.
- Create and update employee credentials.

### Payroll
- Manage employee salaries and generate pay slips.
- Maintain salary records in JSON format and export as CSV.

### Time and Attendance
- Punch in/out functionality for attendance tracking.
- Manual entry of working hours.
- Weekly, detailed, and summarized attendance reports.

### Performance Management
- Track employee performance metrics.
- Generate performance reports.

### Hire
- Manage the recruitment process, including job postings and applicant tracking.

### Analytics
- Generate analytics dashboards for visualizing key metrics.

### PSA (Professional Services Automation)
- Manage project details with filters like active clients and custom tags.
- Track project progress and assigned resources.

### Team Management
- Create groups for collaborative work.
- Assign and manage team members.

### Admin and HR Roles
- Admins have full access to all functionalities.
- HRs can manage employees, teams, work, salary, and time details.

## Data Storage
- All data is stored in JSON format.
- Data can be exported as CSV files for reporting purposes.

## Prerequisites
- Python 3.10 or higher
- Streamlit 1.10.0 or higher

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/attendance-management-system.git
   cd attendance-management-system
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Data Files**:
   Ensure that the following directories and files exist in the `backend/data` folder:
   - `users.json`: Stores user credentials.
   - `attendance.json`: Stores attendance records.
   - `projects.json`: Stores project details.
   - `teams.json`: Stores team information.
   
   Example JSON structures can be found in the `backend/data` folder of the repository.

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**:
   Open your browser and go to `http://localhost:8501/`.

## Usage

### Admin Login
- Use the hardcoded admin credentials to log in.
- Admins can create new HR and employee credentials.

### HR Login
- HRs can manage employee details, attendance, and salary information.

### Employee Login
- Employees can log their attendance, track project progress, and view assigned tasks.

## File Structure
```
attendance-management-system/
|
├── app.py                    # Main application entry point
├── components/               # Frontend components for different modules
│   ├── core_hr.py
│   ├── payroll.py
│   ├── time_tracker.py
│   ├── performance.py
│   ├── hire.py
│   ├── analytics.py
│   └── psa.py
|
├── backend/                  # Backend logic and data handling
│   ├── data/
│   │   ├── users.json
│   │   ├── attendance.json
│   │   ├── projects.json
│   │   └── teams.json
│   ├── json_handler.py       # JSON read/write utility
│   └── authentication.py    # User authentication logic
|
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- Streamlit for simplifying web app development.
- Open-source contributors for supporting Python libraries used in this project.

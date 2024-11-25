
***Interview Scheduling API***

This project provides an API to help schedule interviews by enabling candidates and interviewers to register their availability and then querying for potential interview time slots that work for both parties.

***Features***
  1. User Registration: Register candidates and interviewers with their username.
  2. Availability Registration: Register available time slots for both candidates and interviewers.
  3. Get User Details: Fetch details of all registered users.
  4. Get Available Interview Slots: Fetch possible interview time slots based on candidate and interviewer availability.


***Prerequisites***
    Python 3.x
    Django
    Django Rest Framework (DRF)
    PostgreSQL (or any other database)


***Installation***

1. Local Setup

    Clone the repository:


    git clone https://github.com/vysakhprakash7328/interview_scheduler.git
    cd interview-scheduling-api
    
    Create a virtual environment and activate it:


    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate


    Install required dependencies:

    pip install -r requirements.txt
    Set up the database (If using PostgreSQL, ensure the settings in settings.py are correct):


    python manage.py migrate

    Run the development server:


    python manage.py runserver
    The server should now be running at http://127.0.0.1:8000.

2. Docker Setup

    If you prefer running the application using Docker, follow the steps below to get the containers up and running.

    Clone the repository:


    git clone https://github.com/vysakhprakash7328/interview_scheduler.git
    cd interview-scheduling-api
    Build and run containers using Docker Compose:

    Build and start the containers:


    docker-compose up --build
    
    Stop and remove the containers:


    docker-compose down

    This will start two containers:

    postgres_db for PostgreSQL.
    django_app for the Django application.
    The Django application will be accessible at http://localhost:8000.

3. Docker-Compose Details
    The docker-compose.yml file configures two services:

    db: Uses the official PostgreSQL image to provide the database.
    web: Builds the Django app container, connects it to the PostgreSQL container, and exposes port 8000.
    Volumes: Docker volumes are used to persist data for PostgreSQL (postgres_data volume).

    Networks: Both the db and web services are part of the same custom network, backend, to allow communication between the Django app and the PostgreSQL database.

***API Endpoints***

1. Register User

    Endpoint: /api/register_user/
    Method: POST
    Request Body:
    
    {
        "name": "username",
        "user_type": "Interviewer" or "Candidate"
    }
    Response:
    
    {
        "id": 1,
        "name": "username",
        "user_type": "usertype"
    }

    Description: Registers a new user (Candidate or Interviewer). The user is identified by the name field.

3. Get Users

    Endpoint: /api/get_users/
    Method: GET

    Response:
    
    [
        {
            "id": 1,
            "name": "username",
            "user_type": "usertype"
        }
    ]
    Description: Retrieves a list of all registered users.

4. Register Availability

Endpoint: /api/register_availability/

    Method: POST
    Request Body:
    
    {
        "user": 1,
        "date": "2024-11-25",
        "start_time": "10:00 AM",
        "end_time": "2:00 PM"
    }
    Response:
   
    {
        "user": 1,
        "date": "2024-11-25",
        "start_time": "10:00 AM",
        "end_time": "2:00 PM"
    }
    Description: Registers an available time slot for the user. The user field is required, which corresponds to a previously registered user ID.

4. Get Available Time Slots

    Endpoint: /api/get_available_timeslots/
    Method: GET
    Query Parameters:
    candidate: The ID of the candidate
    interviewer: The ID of the interviewer
    Response:
    
    {
        "success": true,
        "possible_slots": {
            "2024-05-02": [
                ["10:00 AM", "11:00 AM"],
                ["11:00 AM", "12:00 PM"]
            ]
        }
    }
    Description: Returns a list of possible interview slots between the specified candidate and interviewer. The available slots are calculated based on their overlapping time ranges.

***Assumptions***

The time format used is HH:MM AM/PM.
Each interview slot is of 1-hour duration.
The user can either be a candidate or an interviewer.
The candidate's and interviewer's availability can be different, but the system will return only the common available slots.
Improvements
If I had more time, I would consider implementing the following:

Time zone support: Handle time zones to support users from different regions.
Authentication: Implement JWT authentication to secure the API and restrict access to certain endpoints.
UI/UX: Build a frontend application using React or another framework to allow users to interact with the API more easily.
Performance optimizations: Improve the query performance for fetching large amounts of data using pagination or caching mechanisms.
License

***Suggestion for a better solution to the above-mentioned interview scheduling problem***

A prioritized interview scheduling system can be implemented to handle complex requirements effectively. The system can address different time slot durations, urgency of roles, and dynamic rescheduling needs. Below are the key improvements that make this solution better:

1. Priority-Based Scheduling

  Introduce a priority flag for interview requests based on the urgency of the role (e.g., high, medium, low).
  Schedule higher-priority interviews first when overlapping slots are available.
  
2. Flexible Time Slot Durations

  Allow interview durations to vary (e.g., 30 minutes, 1 hour, or custom).
  Calculate overlapping slots dynamically based on these flexible durations.
  
3. Dynamic Rescheduling

  Handle last-minute changes by dynamically rescheduling interviews when interviewers have urgent meetings.
  Notify both the candidate and interviewer immediately with new proposed slots.
  
4. Automated Scheduling with HR Approval

  Automate the scheduling process by proposing optimal slots based on availability and role priority.
  Provide HR managers with the ability to approve or override the schedule before confirmation.

5. Notification and Communication

  Send email or SMS notifications to candidates and interviewers for:
  Initial slot confirmation.
  Rescheduling updates, including the reason for changes.
  Include calendar invites in notifications for seamless tracking.
  
6. Self-Service Options

  Enable candidates and interviewers to view and manage their schedules through a portal.
  Allow them to propose alternate slots, making the process collaborative.
  Integration with Calendars


Docker Commands Recap:

Build and run the app with Docker:

docker-compose up --build
Stop and remove containers:

docker-compose down


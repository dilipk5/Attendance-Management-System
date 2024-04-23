**1. Login System:**
  Users can log in as either a student or a teacher.
  Student login requires entering a student ID, which is then used to fetch attendance data from the Firebase database.
  Teacher login requires entering a username and password, which are verified against pre-defined credentials.

**2. User Interfaces:**
  The GUI includes frames for displaying student or teacher information, actions, and dynamic content.
  For students, it shows their attendance-related information such as total classes, attended classes, and current attendance percentage.
  For teachers, it provides options for marking student attendance, adding CSV files containing attendance data, and viewing all student data.

**3. Attendance Management:**
  Students can view their attendance data for different subjects, including the number of attended classes and total classes.
  Teachers can mark student attendance manually or import data from CSV files. They can also view all student data and update it in the Firebase database.

**4. Additional Features:**
  The system includes features like generating graphs and statistics based on attendance data, calculating leave options for students, suggesting attendance improvement strategies, and displaying a leaderboard based on attendance ratios.

**5. Data Handling:**
  The system uses Firebase Realtime Database to store and retrieve attendance-related information fo

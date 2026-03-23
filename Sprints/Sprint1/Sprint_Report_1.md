# Sprint 1 Report 
Video Link: 
## What's New (User Facing)
 * FEAT-101 (Omar Adil) - Dynamic Inventory Dashboard

 Displays the list of lab tools, using colored badges (Green/Red) and buttons that change automatically based on the equipment's status.
 
 * FEAT-102 (Omar Adil) - Authentication Interface
   
 Page that collects user credentials and provides the entry point to the rest of the application.
 
 * FEAT-103 (Omar Adil) - UI Framework
   
 Provides the main navigation bar and styling for the entire site, using logic to hide or show tabs based on whether a user is logged in.
 
 * FEAT-104 (Omar Adil) - URL Routing & Mock Data
   
 Connects the URLs to the HTML files and provides the placeholder data used to test the website before the database is finished.
 
 * FEAT-106 (Eli Lawrence) - Database Schema Execution
   
 Tables are created and ready to store data in MySQL Workbench from the SQL setup script.
 
 * FEAT-107 (Eli Lawrence) - Database Connection
   
 Implements a live connection so backend can communicate with the SQL database to get and store information.
 
 * FEAT-105 (Zachary Mullin) - User Registration
   
 Frontend of registration allowing newcomers to enter information to sign up.
 
 * FEAT-108 (Zachary Mullin) - User Registration Logic
   
 Write the code to take form data from register.html and INSERT it into the users table.
 
 * FEAT-109 (Zachary Mullin) - Authentication Logic
   
 Update the login and registration route to verify emails and passwords against the database instead of just redirecting.
 
 * FEAT-110 (Zachary Mullin) - Password Security
   
 Hash passwords so they aren't stored as plain text in your database.

## Work Summary (Developer Facing)
We started off by brainstorming the features the final product would need. Then we move forward by implementing these features on at a time. We started with frontend implmentation such as a base page and built off of that. By the end of sprint 1, our application had a login page, registration page, and equipment feed page. We then added the backend logic so that our frontend would display and send information from the database. With that being said, our foundation for the project has been completed. 


## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

 * URL of FEAT-101: https://github.com/omaradil28/CPTS451-Project/issues/1
 * URL of FEAT-102: https://github.com/omaradil28/CPTS451-Project/issues/2
 * URL of FEAT-103: https://github.com/omaradil28/CPTS451-Project/issues/20
 * URL of FEAT-104: https://github.com/omaradil28/CPTS451-Project/issues/21
 * URL of FEAT-106: https://github.com/omaradil28/CPTS451-Project/issues/4
 * URL of FEAT-107: https://github.com/omaradil28/CPTS451-Project/issues/5
 * URL of FEAT-105: https://github.com/omaradil28/CPTS451-Project/issues/3
 * URL of FEAT-108: https://github.com/omaradil28/CPTS451-Project/issues/6
 * URL of FEAT-109: https://github.com/omaradil28/CPTS451-Project/issues/7
 * URL of FEAT-110: https://github.com/omaradil28/CPTS451-Project/issues/8

 Desirables (Remove this section when you save the file):
  * Each issue should be assigned to a milestone
  * Each completed issue should be assigned to a pull request
  * Each completed pull request should include a link to a "Before and After" video
  * All team members who contributed to the issue should be assigned to it on GitHub
  * Each issue should be assigned story points using a label
  * Story points contribution of each team member should be indicated in a comment
 
## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * [app.py](https://github.com/omaradil28/CPTS451-Project/blob/main/backend/app.py)
 * [base.html](https://github.com/omaradil28/CPTS451-Project/blob/main/frontend/templates/base.html)
 * [equipment.html](https://github.com/omaradil28/CPTS451-Project/blob/main/frontend/templates/equipment.html)
 * [login.html](https://github.com/omaradil28/CPTS451-Project/blob/main/frontend/templates/login.html)
 * [pwsecurity.py](https://github.com/omaradil28/CPTS451-Project/blob/main/backend/pwsecurity.py)
 * [register.html](https://github.com/omaradil28/CPTS451-Project/blob/main/frontend/templates/register.html)
 * [database.py](https://github.com/omaradil28/CPTS451-Project/blob/main/backend/database.py)
 
## Retrospective Summary
Here's what went well:
  * Using a UI framework early on prevents us from having to fix navigation and styling inconsistencies later.
  * Database setup using MySQL was relatively easy and painless.
  * Tasks were divided into manageable chunks to make progress visible.
 
Here's what we'd like to improve:
   * Distributing tasks amongst ourselves should be done early on in the sprint.
  
Here are changes we plan to implement in the next sprint:
   * Expand the Live Database Queries using more SQL tables.
   * Distribute tasks properly

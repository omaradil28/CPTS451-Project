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
 * FEAT-108 (Zachary Mullin) - User Registration
 Frontend of registration allowing newcomers to enter information to sign up.
 * FEAT-109 (Zachary Mullin) - User Registration Logic
 Write the code to take form data from register.html and INSERT it into the users table.
 * FEAT-110 (Zachary Mullin) - Authentication Logic
 Update the login and registration route to verify emails and passwords against the database instead of just redirecting.
 * FEAT-111 (Zachary Mullin) - Password Security
 Hash passwords so they aren't stored as plain text in your database.

## Work Summary (Developer Facing)
Provide a one paragraph synposis of what your team accomplished this sprint. Don't repeat the "What's New" list of features. Instead, help the instructor understand how you went about the work described there, any barriers you overcame, and any significant learnings for your team.

## Unfinished Work
If applicable, explain the work you did not finish in this sprint. For issues/user stories in the current sprint that have not been closed, (a) any progress toward completion of the issues has been clearly tracked (by checking the checkboxes of  acceptance criteria), (b) a comment has been added to the issue to explain why the issue could not be completed (e.g., "we ran out of time" or "we did not anticipate it would be so much work"), and (c) the issue is added to a subsequent sprint, so that it can be addressed later.

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

 * URL of FEAT-101: https://github.com/users/omaradil28/projects/6/views/1?pane=issue&itemId=164712906&issue=omaradil28%7CCPTS451-Project%7C1
 * URL of FEAT-102: https://github.com/users/omaradil28/projects/6/views/1?pane=issue&itemId=164713179&issue=omaradil28%7CCPTS451-Project%7C2
 * URL of FEAT-103: https://github.com/users/omaradil28/projects/6/views/1?pane=issue&itemId=164718476&issue=omaradil28%7CCPTS451-Project%7C20
 * URL of FEAT-104: https://github.com/users/omaradil28/projects/6/views/1?pane=issue&itemId=164718679&issue=omaradil28%7CCPTS451-Project%7C21

 Desirables (Remove this section when you save the file):
  * Each issue should be assigned to a milestone
  * Each completed issue should be assigned to a pull request
  * Each completed pull request should include a link to a "Before and After" video
  * All team members who contributed to the issue should be assigned to it on GitHub
  * Each issue should be assigned story points using a label
  * Story points contribution of each team member should be indicated in a comment
 
 ## Incomplete Issues/User Stories
 Here are links to issues we worked on but did not complete in this sprint:
 
 * URL of issue 1 <<One sentence explanation of why issue was not completed>>
 * URL of issue 2 <<One sentence explanation of why issue was not completed>>
 * URL of issue n <<One sentence explanation of why issue was not completed>>
 
 Examples of explanations (Remove this section when you save the file):
  * "We ran into a complication we did not anticipate (explain briefly)." 
  * "We decided that the feature did not add sufficient value for us to work on it in this sprint (explain briefly)."
  * "We could not reproduce the bug" (explain briefly).
  * "We did not get to this issue because..." (explain briefly)

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * [app.py](https://github.com/omaradil28/CPTS451-Project/blob/main/backend/app.py)
 * [base.html](https://github.com/omaradil28/CPTS451-Project/blob/main/frontend/templates/base.html)
 * [equipment.html](https://github.com/omaradil28/CPTS451-Project/blob/main/frontend/templates/equipment.html)
 * [login.html](https://github.com/omaradil28/CPTS451-Project/blob/main/frontend/templates/login.html)
 
## Retrospective Summary
Here's what went well:
  * Using a UI framework early on prevents us from having to fix navigation and styling inconsistencies later.
  * Item 2
  * Item x
 
Here's what we'd like to improve:
   * Distributing tasks amongst ourselves should be done early on in the sprint.
   * Item 2
   * Item x
  
Here are changes we plan to implement in the next sprint:
   * Expand the Live Database Queries using more SQL tables.
   * Item 2
   * Item x

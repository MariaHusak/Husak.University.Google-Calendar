## Husak.University.Google-Calendar
## Author
Mariia Husak FEP-21

husakmaria74@gmail.com

https://t.me/@gusakmary
## Getting Started
### Getting Started with Local Setup for Google Calendar
Welcome to Google Calendar! This guide will walk you through the process of setting up Google Calendar locally on your computer.
#### Prerequisites
Before you begin, ensure you have the following:
- A Google account
- A computer with internet access
- A web browser (Google Chrome, Mozilla Firefox, Safari, etc.)
#### Steps to Setup Google Calendar Locally
##### Step 1: Sign in to Google Account

1. Open your preferred web browser.
2. Go to Google Calendar.
3. Sign in with your Google account credentials (email and password).
   
##### Step 2: Access Calendar Settings

1. Once logged in, click on the gear icon located in the top right corner of the screen.
2. From the dropdown menu, select "Settings".

##### Step 3: Configure Calendar Settings

1. In the Settings page, navigate to the "General" tab.
2. Adjust settings such as time zone, working hours, and default event duration according to your preferences.
3. Click on the "Save" button to apply the changes.

##### Step 4: Explore Calendar Features

1. Familiarize yourself with the various features of Google Calendar, including creating events, setting reminders, and sharing calendars.
2. Navigate through the different views (day, week, month, etc.) to understand how your schedule will appear.
## Project Documentation
### Introduction
Welcome to the documentation for project, a comprehensive and user-friendly calendar application built on the Django framework. This documentation serves as a guide for developers, testers providing insights into its architecture, features, deployment process, and more.
### Architecture Diagram 
You can see the architecture diagram here:

https://lucid.app/lucidchart/0ff30275-670c-47aa-bb2e-8bbd726d1bc8/edit?invitationId=inv_75e9b6ef-4c50-456e-846e-496b8b10d010&page=0_0#
### Infrastructure Diagram
You can see the infrastructure diagram here:

https://miro.com/app/board/uXjVKb2V8W0=/

### Azure deployment process
##### 1. Prepare Django Application
Ensure that your Django application is properly configured and works correctly on your local development machine. Make sure all dependencies are listed in requirements.txt or Pipfile, and your application can run using python manage.py runserver without any errors.

##### 2. Set Up Azure Account
If you haven't already, sign up for an account on Azure. You may need to provide payment information, but Azure often offers free trials and credits for new users.

##### 3. Deploy to Azure App Service
Assuming you choose Azure App Service:

Install the Azure CLI on your local machine if you haven't already.
Log in to Azure CLI using az login command.
Navigate to your Django project directory.
Run az webapp up --sku F1 --name <your-app-name> to deploy your Django application to Azure App Service. Replace <your-app-name> with a unique name for your application.
Azure CLI will guide you through the deployment process and provide a URL where your application will be accessible.

##### 4. Configure Environment Variables
Ensure that your Django application's environment variables, such as database credentials and secret keys, are properly configured on Azure App Service. You can set them using Azure Portal or Azure CLI.

##### 5. Set Up Database
If you're using a database with your Django application, set up the database on Azure. Azure offers managed database services like Azure Database for PostgreSQL or Azure Database for MySQL.

##### 6. Configure Static Files and Media Storage
For static files and media storage, consider using Azure Blob Storage or Azure CDN (Content Delivery Network) to serve static assets efficiently.

##### 7. Set Up SSL/TLS Certificates
Enable HTTPS for your Django application to ensure secure communication. You can use Azure's built-in support for SSL/TLS certificates or bring your own certificate.

##### 8. Test Application
Once deployed, thoroughly test your Django application on Azure to ensure everything works as expected. Check for any configuration issues, performance bottlenecks, or compatibility problems.

##### 9. Monitor and Maintain
Monitor your application's performance and resource usage on Azure. Use Azure's monitoring tools to identify and address any issues promptly. Regularly update your application and dependencies to keep it secure and up-to-date.

## Project Task Decomposition
### Week 1:
- Implement feature: User authentication with Google Account (OAuth 2.0) ✔️
- Set up Azure deployment environment ✔️
- Create project structure on GitHub repository ✔️
- Define initial project architecture
- Write Getting Started documentation for local setup ✔️

### Week 2:
- Implement feature: Calendar View with Monthly Layout ✔️
- Set up Continuous Integration/Continuous Delivery (CI/CD) pipeline 
- Write Project Documentation: Architecture Diagram ✔️
- Write Unit Tests for User Authentication ✔️
- Create Postman collection for testing OAuth endpoints

### Week 3:
- Implement feature: Event Creation functionality ✔️
- Configure Azure deployment settings
- Write Project Documentation: Infrastructure Diagram
- Write Unit Tests for Event Creation functionality ✔️
- Write documentation for Azure deployment process ✔️

### Week 4:
- Implement feature: Reminder Notifications via Email
- Implement automated deployment using CI/CD pipeline
- Write Project Tasks Decomposition ✔️
- Write Unit Tests for Reminder Notifications
- Create Postman collection for testing Reminder endpoints

### Week 5:
- Implement feature: Invite Attendees to Events
- Optimize Azure deployment for performance
- Write documentation for CI/CD process
- Write Unit Tests for Invite Attendees functionality
- Conduct unit testing for OAuth endpoints

### Week 6:
- Implement feature: Recurring Events
- Perform load testing on Azure deployment
- Update Project Documentation based on feedback
- Write Unit Tests for Recurring Events
- Conduct unit testing for Event Creation endpoints

### Week 7:
- Implement feature: Event Editing
- Perform security testing on Azure deployment
- Review and refine Project Tasks Decomposition
- Write Unit Tests for Event Editing
- Conduct unit testing for Reminder endpoints

### Week 8:
- Implement feature: Guest RSVP for Events
- Perform scalability testing on Azure deployment
- Review and refine documentation
- Write Unit Tests for Guest RSVP functionality
- Conduct unit testing for Invite Attendees endpoints

### Week 9:
- Implement feature: Sharing Calendars
- Perform stress testing on Azure deployment
- Address any outstanding issues in documentation
- Write Unit Tests for Sharing Calendars
- Conduct unit testing for Recurring Events endpoints

### Week 10:
- Implement feature: Search Functionality
- Conduct user acceptance testing (UAT)
- Finalize documentation for release
- Write Unit Tests for Search Functionality
- Conduct unit testing for Event Editing endpoints

### Week 11:
- Implement feature: Sync Across Devices
- Prepare for project deployment
- Conduct final round of testing and bug fixes
- Write Unit Tests for Sync Across Devices
- Conduct unit testing for Guest RSVP endpoints

### Week 12:
- Finalize deployment and release
- Conduct post-release monitoring and support
- Conduct retrospective meeting for project review
- Write Unit Tests for remaining functionalities
- Conduct unit testing for Sharing Calendars endpoints

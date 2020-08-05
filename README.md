# ToDo-list

This app will help you keep track of things that the user want to do. Using **momentJS** to create an alarm clock system to let the user know how much time they have left to complete each task. Users also have the ability to mark completed task from the currently active, and overdue tasks.

Inside **"todo/static/todo.js"** is where the logics are stored. This is where the app makes requests to the backend and dynamically update what the users see. 

Inside **"todo/templates/todo"** is where the public data are store. This folder contain the html templates for the project. 

Inside **todo/models.py** is the template for two models objects, User and Tasks. User stores the user's data. Tasks is where all the information for each task's deadline get stored.
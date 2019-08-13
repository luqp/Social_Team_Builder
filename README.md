# Social Team Builder
In this site users are able to create a brief profile for themselves after they sign up with an avatar, 
a bio, and pick their skills from a list. Users can post a project, too, giving it a title and description. 
They also can list the positions that they need for a job with a brief description.
Users are able to find a project and ask to join it. 
The project owner can approve or deny the person asking to join.

## To install
Create a new Python virtual environment and activate it

### Install Requirements
This project uses some requirements located on requirements.txt file, to install:
```
(env) $ pip install -r requirements.txt
```

## Run app
To run the application you need to enter to `social_team` folder and load migrations:
```
(env) $ python manage.py migrate
```
### Load sample data
If you want to test the application with sample data, enter the following command:
```
(env) $ python manage.py loaddata .\fixtures\fixtures.json
```
### Run server
To run server enter the following command:
```
(env) $ python manage.py runserver
```
Make `ctrl + click` in `http://127.0.0.1:8000/` this open a new window in your browser
```
Django version 2.2.4, using settings 'social_team.settings'
Starting development server at http://127.0.0.1:8000/      
Quit the server with CTRL-BREAK.
```

## What you can do with the project

#### Can see the profile and edit it, you also add multiple skills for your profile.

<p align="center">
  <img src="https://github.com/luqp/Social_Team_Builder/blob/master/social_team/media/images%20readme/Profile.png">
</p>

#### Create a project.

<p align="center">
  <img src="https://github.com/luqp/Social_Team_Builder/blob/master/social_team/media/images%20readme/New_project.png">
</p>

#### Create multiple positions for a project. Positions relate to a particular skill.

<p align="center">
  <img src="https://github.com/luqp/Social_Team_Builder/blob/master/social_team/media/images%20readme/New_position.png">
</p>

### Can see the project detail and you can approve or reject an applicant in your project. A email is sent when approved/rejected for a position.

<p align="center">
  <img src="https://github.com/luqp/Social_Team_Builder/blob/master/social_team/media/images%20readme/Project.png">
</p>

### Can see all available projects and needs

<p align="center">
  <img src="https://github.com/luqp/Social_Team_Builder/blob/master/social_team/media/images%20readme/Projects_list.png">
</p>

### Can filter projects by name, description or position skills needed.

<p align="center">
  <img src="https://github.com/luqp/Social_Team_Builder/blob/master/social_team/media/images%20readme/Search.png">
</p>

### Can apply for a position and see your all applications

<p align="center">
  <img src="https://github.com/luqp/Social_Team_Builder/blob/master/social_team/media/images%20readme/applications.png">
</p>


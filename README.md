

# Profile-Portal
* Consolidated profile portal for the members of an organisation.
* The portal is intended for IT/CS based orgs. where the data is grabbed from common websites like SPOJ, Codechef, GitHub, Codeforces, Codebuddy etc. and displayed in a consolidated form.

## How does it work ?
* The details of every member of the organisation is stored in the data base(sqlite3 here).
* The details include the CP profiles and Codechef,Hackerearth,SPOJ, Codebuddy, Codeforces and also social coding platforms like Github and Behance
* Python scripts scrapes the data from the profiles and displays it in the portal.
* Flexibility : Any user can view the profile of another using the unique ID (Roll no.)

## Building on your machine

### Setup an environment:
```
git clone https://github.com/RavicharanN/proj-profilePortal
cd proj-Profileportal
virtualenv venv
source venv/bin/activate
```
### Installation: 
```
pip install -r requirements.txt
```
### Run project: 
```
cd sprofileportal 
python manage.py runserver
```


## What does it use ?
* Beautiful soup module for scraping the data.
* Sqlite3 as the database
* Django as the web-framework

## Database-Schema
* Built-in User model for user registration.
* Student Model which has a foreign key of User model and contains basic info of the user.
* Site model contains all the sites that are available for scraping data.
* StudentSite model contains a forignKey of User model and also of Site model. 
* GithubRank model that contains various language work and ranking of users.

## Working of the app info
* A user registers/logins he/she can fill a Student table form(only once) to enter his/her basic profile data which can be updated later.
* Then a user can see his/her profile, see their records from different websites, add a new website details, update the details of the filled websites just with a click.
* User can search for other users by voice-recognition feature using their roll-no.
* Also there is a ranking page where users are ranked according to criterias set for the different sites.
* See the language wise work done and ranking for github users.

## To-Do
* Start improving the frontend design.
* Add paginators for the index page.
* Add scraping scripts for Hackerearth and Behance.
* Improve github rank view critetion.
* Collection of the data from the students and creating the actual database.
* Rigorous testing of the website.


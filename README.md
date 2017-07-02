
#### (Look into the sprofileportal folder for source files)

# Profile-Portal
* Automatic profile portal for the members of an organisation.
* The portal is intended for IT/CS based orgs. where the data is grabbed from common websites like SPOJ, Codechef, GitHub, etc. and displayed in a consolidated form.

## How does it work ?
* The details of every member of the organisation is stored in the data base(sqlite3 here).
* The details include the CP profiles and Codechef,Hackerrank,Hackerearth,SPOJ and also social coding platforms like Github and Behance
* A python script scrapes the data from the profiles and displays it in the portal.
* Flexibility : Any user can view the profile of another using the unique ID (Roll no.)

## Building on you machine

### Setup an environment
```
git clone https://github.com/RavicharanN/proj-profilePortal
cd proj-Profileportal
virtualenv .
source bin/activate

```
### Installation 
```
pip install django 
pip install BeautifulSoup4
pip install requests 
pip install urllib3

```
### Run project 
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

## Working of the app info
* A user registers/logins he/she can fill a Student table form(only once) to enter his/her basic profile data which can be updated later.
* Then a user can see his/her profile, see their records from different websites, add a new website details, update the details of the filled websites just with a click.
* User can search for other users by voice-recognition feature using their roll-no.
* Also there is a ranking page where users are ranked according to criterias set for the different sites.

## To-Do
* Come up with the critetion to filter out the top performers in the respective fields.
* Implement it.
* Start improving the frontend design.
* Collection of the data from the students and creating the actual database.
* Rigorous testing of the website.

## To-Do Frontend Design
* use django templates
* make it responsive for mobile applications
* mainly use bootstrap for the designing

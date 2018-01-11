
Join our [gitter channel](https://gitter.im/ProfilePortal/) for any queries.

# Profile-Portal
* Consolidated profile portal for the members of an organisation.
* The portal is intended for IT/CS based orgs. where the data is grabbed from common websites like SPOJ, Codechef, GitHub, Codeforces, Codebuddy etc. and displayed in a consolidated form.
<br>
[Important guidelines for Opencode participants](#resources)

## How does it work ?
* The details of every member of the organisation is stored in the data base(sqlite3 here).
* The details include the CP profiles and Codechef,Hackerearth,SPOJ, Codebuddy, Codeforces and also social coding platforms like Github and Behance
* Python scripts scrapes the data from the profiles and displays it in the portal.
* Flexibility : Any user can view the profile of another using the unique ID (Roll no.)
* One can know where he/she stands among the registered users.

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

## Building on your machine

### Requirments
* Python2.7
* pip 9.0.1
* virtualenv/venvwrapper to setup virtual environment on your system.

### Setup an environment:
```
git clone https://github.com/GitHubCommunity-IIITAllahabad/ProfilePortal-Beta
cd proj-Profileportal
virtualenv venv
source venv/bin/activate
```
### Installation: 
```
pip install -r requirements.txt
```
### Run project: (Usage - Python2.7)

```
python manage.py runserver
```
## Important Guidelines for OpenCode participants

### Resources 
* [Click Here](https://virtualenv.pypa.io/en/stable/installation/) for the guidlines to install virtualenv on your machine.
* [Click Here](https://pip.pypa.io/en/stable/installing/) for the guidlines to install pip on your machine.

**Note:** Register functionality has been currently disbaled. And all the opencode participants are requested to login using the following credentials : <br>
**Username:** user1, user2, user3, user4 (Anyone can be used).<br>
**Password:** test1234


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


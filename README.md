# proj-profilePortal
* Automatic profile portal for the members of an organisation.
* The portal is intended for IT/CS based orgs. where the data is grabbed from common websites like SPOJ, Codechef, GitHub, etc. and displayed in a consolidated form.

## How does it work ?
* The details of every member of the organisation is stored in the data base(Mongodb here).
* The details include the CP profiles and Codechef,Hackerrank,Hackerearth,SPOJ and also social coding platforms like Github and Behance
* A python script scrapes the data from the profiles and displays it in the portal.
* Flexibility : Any user can view the profile of another using the unique ID (Roll no.)

## What does it use ?
* Beautiful soup module for scraping the data.
* Mongodb as the database
* Django as the web-framework

## To-Do Database-Schema
* Yet to be done

## To-Do
* Write the scripts to scrape the Data from the mentioned websites.
* Displaying the data in the webpage.
* Decide the Database Schema.
* Create a dummy database (that contatains the details of a few users)
* Scrape the data of a specified student by looping through the database and displaying them in the portal.
* Come up with the critetion to filter out the top performers in the respective fields.
* Implement it.
* Start improving the frontend design.
* Collection of the data from the students and creating the actual database.
* Rigorous testing of the website.

## To-Do Frontend Design
* use django templates
* make it responsive for mobile applications
* mainly use bootstrap for the designing

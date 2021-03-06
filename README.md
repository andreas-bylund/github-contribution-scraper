# Github Contribution Scraper 
Suggestion how a scraper for downloading user contribution for the course "Projekt i software engineering G1F, 15 hp" at University of Skövde can look like. 

# Functionality 
+ Fetches data from the Github API and stores it to a Sqlite database 
+ Uses an array that contains usernames of participants on the course 
+ If the script have used all the API calls the script will go to sleep and wait until the script have API calls to use again.

# Limitations
+ This scripts follows Github's API limitations. This means that the script can use as much as 60 requests per hour. But can go up to 5000 requests per hour if you authenticate yourself (authenticate functionality does not exists at the moment)
# Example output
![Example output](http://andreasbylund.se/img/git-contribution-scraper/exempel_1.png)

![Example output](http://andreasbylund.se/img/git-contribution-scraper/exempel_2.png)

![Example output](http://andreasbylund.se/img/git-contribution-scraper/exempel_3.png)

# License
Open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)

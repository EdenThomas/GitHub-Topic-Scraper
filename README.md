# GitHub-Topic-Scraper
This Python program is designed to retrieve and download data on a range of topics from GitHub. 

For each topic, it collects the topic's title, its URL, and a description. 

Then it retrieves the top repositories available for each topic from their respective pages, getting info such as the repository name, the username of the repository owner, the number of stars, and the repository's URL. 

The data for each topic is then saved into a csv file.

The scraper works by fetching the main topics page from GitHub, then it extracts information about each topic and iterates through them to fetch details about the top repositories under each topic.

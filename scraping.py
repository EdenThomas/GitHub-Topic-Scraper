import requests
import pandas as pd
from bs4 import BeautifulSoup
from config import TOPICS_URL, BASE_URL
from utils import extract_star_count

def get_main_topics_page():
    # Fetches the main topics page from github and returns its html content
    response_data = requests.get(TOPICS_URL)
    if response_data.status_code != 200:
        raise Exception(f'Error loading page {TOPICS_URL}')
    return BeautifulSoup(response_data.text, 'html.parser')

def get_topic_titles(content):
    # Extracts and returns a list of topic titles from parsed html content
    title_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    return [tag.text for tag in content.find_all('p', {'class': title_class})]

def get_topic_descs(content):
    # Extracts and returns a list of descriptions for each topic from parsed html content
    desc_class = 'f5 color-fg-muted mb-0 mt-1'
    return [tag.text.strip() for tag in content.find_all('p', {'class': desc_class})]

def get_topic_links(content):
    # Extracts and returns a list of urls for each topic
    return [BASE_URL + tag['href'] for tag in content.find_all('a', {'class': 'no-underline flex-1 d-flex flex-column'})]

def get_topic_html(topic_url):
    # Fetches and returns the html content of a specific topic page from github
    response_data = requests.get(topic_url)
    if response_data.status_code != 200:
        raise Exception(f'Error loading page {topic_url}')
    return BeautifulSoup(response_data.text, 'html.parser')

def get_repo_data(repo_name_tag, repo_stars_tag):
    # Extracts data about a single repository including owner, repo name, star count and url
    a_tags = repo_name_tag.find_all('a')
    return {
        'username': a_tags[0].text.strip(),
        'repo_name': a_tags[1].text.strip(),
        'stars': extract_star_count(repo_stars_tag.text.strip()),
        'repo_url': BASE_URL + a_tags[1]['href']
    }

def get_topic_repos(topic_content):
    # Extract and return data about all repositories
    repo_name_tags = topic_content.find_all('article', {'class': 'border rounded color-shadow-small color-bg-subtle my-4'})
    repo_stars_tags = topic_content.find_all('span', {'id': 'repo-stars-counter-star'})
    return pd.DataFrame([get_repo_data(repo_name_tags[i], repo_stars_tags[i]) for i in range(len(repo_name_tags))])

def get_topics_data():
    # Joins all topic related data into a single dataframe
    content = get_main_topics_page()
    topics_data = {
        'title': get_topic_titles(content),
        'description': get_topic_descs(content),
        'url': get_topic_links(content)
    }
    return pd.DataFrame(topics_data)
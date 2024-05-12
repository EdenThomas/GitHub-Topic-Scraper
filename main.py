import os
from scraping import get_main_topics_page, get_topic_repos, get_topics_data
from utils import file_needs_update

def scrape_topic_repo(topic_page_url, save_path):
    # Check if the data file already exists and is updated to skip this part
    if os.path.exists(save_path) and not file_needs_update(save_path):
        print(f"The file {save_path} is already up-to-date.")
        return

    # Fetches the main topics page and retrieves repositories data for the specified topic
    topics = get_main_topics_page()
    topic_data_df = get_topic_repos(topics)

    # Save the dataframe containing the topic's repository data to csv file.
    topic_data_df.to_csv(save_path, index=False)
    print(f"Data saved to {save_path}")

def scrape():
        print('Scraping list of topics')
        scraped_topics_df = get_topics_data()
        os.makedirs('data', exist_ok=True)
        # Iterates over each topic, scrapes its top repositories and saves them to a csv file
        for index, row in scraped_topics_df.iterrows():
            print(f'Scraping top repositories for "{row["title"]}"')
            save_path = f'data/{row["title"].replace(" ", "_").replace("/", "_")}.csv'
            scrape_topic_repo(row["url"], save_path)

if __name__ == "__main__":
    scrape()

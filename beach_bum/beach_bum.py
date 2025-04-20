from bs4 import BeautifulSoup
import requests
from crawler_scraper_common_by_yuvch import Crawler
from crawler_scraper_common_by_yuvch import utils
import os
import inspect


class BeachBum(Crawler):
    def __init__(self):
        super().__init__(utils.websites['beach_bum'])
        self.collection_name = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]

    def get_r_d_link(self) -> str:
        # Query parameters
        url = self.url + "careers-category/?c=rd-qa"
        return url

    def get_data_link(self) -> str:
        url = self.url + "careers-category/?c=data-analytics"
        return url

    def query(self):
        data_url = self.get_data_link()
        r_d_url = self.get_r_d_link()
        links = [data_url, r_d_url]
        for link in links:
            response = requests.get(link)
            if response.status_code == 200:
                try:
                    html_content = response.text  # Get the HTML content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    job_links = soup.find_all('a',
                                              class_="jsAnimation")  # Adjust the class name based on the actual HTML structure
                    job_names = soup.find_all('li',
                                              class_="categories__item")
                    for i in range(len(job_links)):
                        url = job_links[i].get('href')
                        self.data[url] = {}
                        self.data[url]['title'] = job_names[i].get_text().strip()
                except (ValueError, KeyError) as e:
                    print(f"Error parsing the response: {e}")
            else:
                print(f"Failed to retrieve data: {response.status_code}")

    def extract_data_from_job(self):
        self.query()
        for url in self.data.keys():
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    html_content = response.text  # Get the HTML content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    information = soup.find('div',
                                            class_='vacancy__content')
                    responsibility = information.get_text().strip()
                    requirements = information.find_next('div').get_text().strip()

                    self.data[url]['Responsibilities'] = responsibility
                    self.data[url]['Requirements'] = requirements
                    self.data[url]['location'] = "Raanana, Israel"
                except (ValueError, KeyError) as e:
                    print(f"Error parsing the response: {e}")
            else:
                print("status code wasn't 200 - failed to perfectly connect with the server")

    def run(self):
        self.extract_data_from_job()
        self.move_to_mongo()
        self.update_mongo()

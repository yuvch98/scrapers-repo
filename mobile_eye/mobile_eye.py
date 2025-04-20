from bs4 import BeautifulSoup
import requests
from crawler_scraper_common_by_yuvch import Crawler
from crawler_scraper_common_by_yuvch import utils
import os
import inspect


class MobileEye(Crawler):
    def __init__(self):
        super().__init__(utils.websites['mobile_eye'])
        self.collection_name = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]

    def query(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            try:
                html_content = response.text  # Get the HTML content
                soup = BeautifulSoup(html_content, 'html.parser')
                job_name = soup.find_all('h3')
                for job in job_name:
                    name = job.text
                    location = job.find_next().get_text().strip()
                    url = "https://careers.mobileye.com" + job.find_previous('a').get('href')
                    if 'Israel' not in location:
                        continue
                    if "FILTER" in name:
                        continue
                    else:
                        self.data[url] = {}
                        self.data[url]['title'] = name
                        self.data[url]['location'] = location

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
                                            class_='list_box')
                    requirements = information.find_next('div')
                    responsibility = information.get_text().strip()
                    requirements = requirements.get_text().strip()
                    self.data[url]['Responsibilities'] = responsibility
                    self.data[url]['Requirements'] = requirements

                except (ValueError, KeyError) as e:
                    print(f"Error parsing the response: {e}")

                except IndexError:
                    print("Index out of bounds")
                    print(url)
            else:
                print("status code wasn't 200 - failed to perfectly connect with the server")

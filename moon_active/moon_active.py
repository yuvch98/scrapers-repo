from bs4 import BeautifulSoup
import requests
from crawler_scraper_common_by_yuvch import Crawler
from crawler_scraper_common_by_yuvch import utils
import os
import inspect


class MoonActive(Crawler):
    def __init__(self):
        super().__init__(utils.websites['moon_active'])
        self.collection_name = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]
    def get_r_d(self) -> (dict[str:str], dict[str:str]):
        # Query parameters
        params = {
            'dept': 'r-d',
            'loc': 'tel-aviv,-israel'
        }

        # Headers to mimic the browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Referer': self.url + 'careers/?dept=r-d&loc=tel-aviv,-israel',
            'X-Requested-With': 'XMLHttpRequest',
        }
        return params, headers

    def get_data(self) -> (dict[str:str], dict[str:str]):
        # Query parameters
        params = {
            'dept': 'data---analytics',
            'loc': 'tel-aviv,-israel'
        }

        # Headers to mimic the browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Referer': self.url + 'careers/?dept=data---analytics&loc=tel-aviv,-israel',
            'X-Requested-With': 'XMLHttpRequest',
        }
        return params, headers

    def query(self, params, headers):
        # Send the GET request
        response = requests.get(self.url, params=params, headers=headers)

        # Check if the response is successful
        if response.status_code == 200:
            try:
                # Assuming the response is a JSON object containing HTML
                data = response.json()
                html_content = data.get('html')  # Get the HTML content

                # Parse the HTML using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract job details from the HTML (update selectors based on actual structure)
                job_names = soup.find_all('span',
                                          class_='job-name')  # Adjust the class name based on the actual HTML structure

                job_url = soup.find_all('a')

                job_loc = soup.find_all('span',
                                        class_='job-city')
                for i in range(len(job_names)):
                    self.data["https://www.moonactive.com" + job_url[i].get('href')] = {}
                    self.data["https://www.moonactive.com" + job_url[i].get('href')]['title'] = job_names[
                        i].get_text().strip()
                    self.data["https://www.moonactive.com" + job_url[i].get('href')]['location'] = job_loc[
                        i].text.strip()

            except (ValueError, KeyError) as e:
                print(f"Error parsing the response: {e}")
        else:
            print(f"Failed to retrieve data: {response.status_code}")

    def extract_data_from_job(self):
        params, headers = self.get_data()
        self.query(params, headers)
        params, headers = self.get_r_d()
        self.query(params, headers)
        for url in self.data.keys():
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    html_content = response.text  # Get the HTML content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    headers = soup.find_all('div',
                                            class_='detail-name')
                    information = soup.find_all('div',
                                                class_='detail-value')
                    for i in range(len(headers)):
                        self.data[url][headers[i].get_text().strip()] = information[i].get_text().strip()

                except (ValueError, KeyError) as e:
                    print(f"Error parsing the response: {e}")
            else:
                print("status code wasn't 200 - failed to perfectly connect with the server")

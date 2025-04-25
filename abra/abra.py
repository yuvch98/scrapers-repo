import inspect
import os
from crawler_scraper_common_by_yuvch import Crawler, utils, cleaners
import requests
import re
import json


class Abra(Crawler):
    def __init__(self):
        super().__init__(utils.websites['abra'])
        self.collection_name = os.path.basename(inspect.getfile(inspect.currentframe())).split('.')[0]

    def get_data(self) -> bool:
        jobs = []
        res = requests.get(self.url)
        doc = res.text
        regex = utils.commit_regex
        try:
            match = re.search(regex, doc, re.DOTALL)
            if match:
                json_data = match.group(1)
                jobs = json.loads(json_data)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error extracting jobs: {e}")
            return False

        for job in jobs:
            url = (job['url_comeet_hosted_page'])
            self.data[url] = {}
            self.data[url]['title'] = job['name']
            if job['location']:
                self.data[url]['location'] = job['location']['city'] + ', ' + job['location']['country']
            else:
                self.data[url]['location'] = ""
            i = 0
            for detail in job["custom_fields"]["details"]:
                clean_value = (cleaners.clean_html(detail["value"]))
                if i == 0:
                    self.data[url]['Responsibilities'] = clean_value
                else:
                    self.data[url]['Requirements'] = clean_value
                i += 1
        print(self.data)
        return True

    def run(self):
        worked = self.get_data()
        if worked:
            print("it worked successfully.")
            self.move_to_mongo()
            self.update_mongo()
        else:
            print("Task failed. Make sure all requirements are satisfied for mongoDB connection")

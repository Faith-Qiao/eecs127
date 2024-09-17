from bs4 import BeautifulSoup
import json
import sys
from courses.base_course import BaseCourse

class EECS_127(BaseCourse):
    def __init__(self):
        super().__init__("https://classes.berkeley.edu/content/2024-spring-physics-7a-002-lec-002")

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        data_element = soup.find(attrs={'data-enrollment': True})
        if data_element:
            return self.extract_data(data_element['data-enrollment'])
        else:
            print("Could not find the required element on the page.")
            sys.exit(1)

    def extract_data(self, data_json):
        try:
            data = json.loads(data_json)
            enrolled = data.get('available', {}).get('enrollmentStatus', {}).get('enrolledCount', 0)
            available = enrolled < 192
            message = f"{enrolled} enrolled out of 192 spots"
            return available, message
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            sys.exit(1)

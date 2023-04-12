Web Scraping with Yandex Maps

This project is a web scraping project that extracts data from Yandex Maps using Python and Selenium.
Installation

Clone the repository to your local machine using the command:

bash

git clone https://github.com/yourusername/yourrepository.git

Replace 'yourusername' and 'yourrepository' with your account and repository names, respectively.

Install the required packages using the command:

bash

pip install -r requirements.txt

This will install all the necessary packages listed in the requirements.txt file. 
Make sure you have Python 3.x installed on your computer and have access to the command line.
Requirements

Python 3.10
beautifulsoup4==4.12.2
selenium==3.8.3
lxml==4.9.2

How to use

To run the web scraper, navigate to the project directory in the command line and run the following command:

bash

python main.py

Functions

The main function in this project is get_main_page, 
which takes a WebDriver object and returns the HTML of the Yandex Maps page. 
The function uses the following libraries:

    json
    time
    typing.List
    typing.Dict
    typing.Tuple
    bs4.BeautifulSoup
    selenium.webdriver
    selenium.webdriver.ActionChains
    selenium.webdriver.remote.webdriver.WebDriver
    selenium.webdriver.common.by.By

The code starts by setting up Chrome options and a driver, 
then navigates to the Yandex website and sets up cookies for the website. 
It then navigates to Yandex Maps and gets the HTML of the page using the get_main_page function.

Note: The complete code for this project is in main.py.
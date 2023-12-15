import requests
from bs4 import BeautifulSoup
from loguru import logger


def get_sentences(amount_of_random_sentences=10):
    try:
        url = 'https://basicenglishspeaking.com/100-common-phrases-and-sentence-patterns/'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all td elements containing links
        td_elements = soup.find_all('td')

        sentences = [td.find('a').get_text(strip=True)[5:] for td in td_elements if td.find('a')]

        return sentences[:amount_of_random_sentences]
    except Exception as e:
        logger.error(f"Error fetching sentences: {str(e)}")
        return []
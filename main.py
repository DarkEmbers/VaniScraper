import requests
from bs4 import BeautifulSoup
from pathlib import Path

def getTranscripts():
	page = requests.get("https://vanisource.org/wiki/Category:Lectures_-_Bhagavad-gita_As_It_Is")
	soup = BeautifulSoup(page.content, "html.parser")

	pages_container = soup.find("div", class_="mw-content-ltr")
	page_lists = pages_container.find_all("ul")
	page_links = []

	for i in range(1, len(page_lists)):
		page_links.extend(page_lists[i].find_all("a"))

	Path.mkdir(Path("transcripts"), exist_ok=True)

	# For each page, saae the transcript to a txt file
	for link in page_links:
		# Open lecture
		page = requests.get("https://vanisource.org" + link["href"])
		soup = BeautifulSoup(page.content, "html.parser")

		# Get all text after audio
		audio_container = soup.find("audio").parent
		texts = audio_container.find_next_siblings()

		with open("transcripts/" + link["title"] + ".txt", "w", encoding='utf-8') as f:
			for text in texts:
				if text.name == "p":
					f.write(text.text + "\n")

				elif text.name == "dl":
					f.write(text.text + "\n\n")

		break

getTranscripts()
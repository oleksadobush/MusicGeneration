import requests
from bs4 import BeautifulSoup
from rich import print as rich_print
import json

if __name__ == "__main__":
    # url to te main page of the website
    main_url = "https://www.vgmusic.com/"
    section_pages_uls = []

    ## PARSE MAIN PAGE
    r = requests.get(main_url)

    # use BeautifulSoup to extract all the "p" elements with class "menu"
    soup = BeautifulSoup(r.content, "html.parser")
    sections = soup.find_all("p", class_="menu")
    # discard the first section as it is irrelevant
    sections = sections[1:]

    # for each section, get all the links to pages
    for section in sections:
        for link in section.find_all("a"):
            section_pages_uls.append(link["href"][1:])

    ## PARSE THE SUBPAGES
    files_links = dict()

    # iterate over each page
    # TODO: remove :2, used it for testing
    # for url in section_pages_uls[:2]:
    for url in section_pages_uls:
        r = requests.get(main_url + url)
        soup = BeautifulSoup(r.content, "html.parser")
        # extract ouly the first table - it contains all the midi files
        table = soup.find("table")
        # find all links, however there are broken links and empty links
        links = table.find_all("a")

        files = dict()

        # initialize the name of the section for better grouping later
        section = ""
        for link in links:
            try:
                # if the link doesnt have the href, we get exception
                # if the last 4 chars of the link are not ".mid" - we dont need it, it is comments link
                if link["href"][-4:] == ".mid":
                    files[section].append(link["href"])
            except KeyError:
                # if links doesnt have href, it is the section name
                section = link.text
                files[section] = []
                continue
        files_links[url] = files

    with open("midi_files.json", "w") as outfile:
        json.dump(files_links, outfile, indent=2)

    # rich_print(files_links)

    # rich_print(section_pages_uls)

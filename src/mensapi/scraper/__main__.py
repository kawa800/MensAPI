import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
from urllib.parse import urljoin
from Website import Website

BASE_URL = "https://mocca.stw-d.de/mocca.digitalsignage/3500/Speiseplan3500/"

def main():
    website = Website(BASE_URL)
    print(website)

    main_page = website.fetch("Index.html")

    all_iframes = website.get_iframes(main_page)

    for iframe in all_iframes:
        print(iframe)

if __name__ == "__main__":
    main()


# res = requests.get(URL)
# res.encoding="utf-8"
# html = res.text
# soup = BeautifulSoup(html, 'html.parser')
#
# def get_iframe_url() -> list:
#     """ Returns a list of the urls of each iframe """
#     iframes = soup.find_all("iframe")
#
#     iframe_text = []
#     for iframe in iframes:
#         url = urljoin(URL, iframe.attrs['src'])
#         iframe_text.append(url)
#
#     return iframe_text
#
# def get_day(url: str) -> str:
#     """ Returns the day of the specific iframe. Required because the iframes Site_0.html, Site_1.html etc. aren't sorted. 
#     The first iframe stored in Site_0.html always returns the day the user clicks on the page."""
#
#     res = requests.get(url)
#     res.encoding="utf-8"
#     html = res.text
#     soup = BeautifulSoup(html, 'html.parser')
#     h2tags = soup.find('h2')
#     tag = h2tags.text
#     for tag in h2tags:
#         print(tag.text)
#
# def get_date(url: str) -> str:
#
# for url in get_iframe_url():
#     get_day(url)

# def get_daily_meals():
#     frame_text = get_iframe_html()
#
#     for frame in frame_text:
#         soup = BeautifulSoup(frame, 'html-parser')
#         print(soup.select_one('title'))
#
# get_daily_meals()

    # "name"
    # "date"
    # "price" (students, non-students)
    # "nähwerte(kcal, Fett, gesättigte Fettsäuren, Kohlenhydrate, Zucker, Eiweiß, Salz)"
    # Zusatzstoffe: https://www.stw-d.de/kennzeichnungen-zusatzstoffe/

    # // get weekly
    # // get monday
    ## // get b
# Monday
# Speisen
# Preise
# "day"
# "speise"

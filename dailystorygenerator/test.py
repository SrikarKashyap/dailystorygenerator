from  urllib.request import urlopen
from bs4 import BeautifulSoup

page = urlopen("https://www.listchallenges.com/top-100-most-visited-cities-in-the-world")
soup = BeautifulSoup(page)
with open("test.txt", "w") as f:
    f.write(soup.get_text())


import zipfile
import os
import io
from urllib.request import Request, urlopen
import shutil
import requests as R
from bs4 import BeautifulSoup


movie = "Insurgent"
base_link = "https://yts-subs.com"
download_directory = "E:\Quick access\Desktop\Subtitrari"


def find_movie(movie):

    request = Request("https://yts-subs.com/search/" + movie,headers={'User-Agent': 'Mozilla/5.0'})
    file = urlopen(request)
    bites = file.read()
    text = bites.decode("utf-8")

    html = BeautifulSoup(text,'html.parser')
    media_body = html.find_all("div",{"class" : "media-body"})[0]
    link_subtitle = base_link + media_body.find_all('a')[0]['href']
    request = Request(link_subtitle,headers={'User-Agent': 'Mozilla/5.0'})

    # sunt in subtitle "https://yts-subs.com/movie-imdb/tt0816692"
    file = urlopen(request)
    html = BeautifulSoup(file,'html.parser')
    table = html.find_all("div",{"class" : "table-responsive"})[0]

    linkuri_subitrari = []

    for row in table.find_all("tr",{"class" :"high-rating"}):
        flag = row.find_all("td",{"class" : "flag-cell"})[0]
        language = flag.find_all("span",{"class" : "sub-lang"})[0].get_text()
        link = base_link + row.find_all('a')[0]['href']
        if language == "Romanian":
            linkuri_subitrari.append(link)
    for link in linkuri_subitrari:
        request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        file = urlopen(request)
        html = BeautifulSoup(file, 'html.parser')

        clasa_principala = html.find_all('a', {"class": "btn-icon download-subtitle"})[0]
        link_download = clasa_principala['href']
        print(link_download)
        download(link_download)
def download(link):

    path_creaza = download_directory + os.sep + movie
    print(path_creaza)
    if os.path.exists(path_creaza) == False:
        os.mkdir(path_creaza)
    path_sterge = path_creaza + os.sep + "__MACOSX"
    r = R.get(link)
    zip = zipfile.ZipFile(io.BytesIO(r.content))
    zip.extractall(path=path_creaza)
    # sterge macOSX
    if os.path.exists(path_sterge):
        shutil.rmtree(path_sterge)


# download_directory = input("Where to Save Subtitles? : ")
# movie = input("Ce film vrei ?")
find_movie(movie)

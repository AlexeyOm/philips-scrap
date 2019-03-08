from bs4 import BeautifulSoup
import requests
import os

#initial_address = "https://www.philips.ru/p-m-pr/signage-solutions/multi-touch-series/latest#filters=LED_SERIES_SU%2CD_LINE_SERIES_SU%2CP_LINE_SERIES_SU%2CH_LINE_SERIES_SU%2CVIDEOWALL_SERIES_SU%2CL_LINE_SERIES_SU%2CMULTITOUCH_SERIES_SU%2CV_LINE_SERIES_SU&sliders=&support=&price=&priceBoxes=&page=&layout=96.subcategory.p-grid-icon"

links = []

f = open("links.txt", "r")
for line in f:
    link = line.replace("\n", "")
    links.append(link)
f.close()

links = links[0:2]
print(links)

descriptions = []
failed_links = []

for link in links:
    address = link + "/overview"
    print(f"started scraping {address}")
    page = requests.get(address)
    #print("got page")
    content = page.content
    #print(content)
    soup = BeautifulSoup(content, features="html5lib")
    #print("got soup")

    paragraphs = soup.select("div.p-feature-item")
    print(f"got {len(paragraphs)} paragraps")
    if len(paragraphs) == 0:
        failed_links.append(link)
    else:
        model_name = soup.select(".p-type")[0].contents[0]
        print(f"model name is {model_name}")

        safe_name = model_name.replace("/", "_")

        try:
            os.mkdir("tmp/" + safe_name)
        except OSError:
            print ("Creation of the directory failed" )
        else:
            print ("Successfully created the directory " )

        description = []

        f = open(f"tmp/{safe_name}/{safe_name}.html", "w")
        for p in paragraphs:
            f.write(f"<h3>{p.h3.contents[0]}</h3>\n")
            #print(f"h3 : {p.h3.contents[0][0:40]}")
            if p.img:
                src = p.img['src']
                #print(f"img: {src}")
                f.write(f"<img src='{src}'/>\n")
            #print(f"p  : {p.p.contents[0][0:40]}")
            f.write(f"<p>{p.p.contents[0]}</p>\n")



        address = link + "/specifications"
        page = requests.get(address)
        content = page.content
        soup = BeautifulSoup(content, features="html5lib")

        dds = soup.select("dd span")
        dts = soup.select("dt")

        f.write(f"{model_name}: технические характеристики")

        for idx, dt in enumerate(dts):
            print(f"{dt.contents[0]}: {dds[idx].contents[0]}")


        f.close()


'''

result = requests.get(initial_address)
content = result.content

soup = BeautifulSoup(content, features="html5lib")
selection = soup.select("a")

for a in selection:
    print(a.get("href"))

'''
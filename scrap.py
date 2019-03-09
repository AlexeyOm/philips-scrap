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

#links = links[0:1]
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


    '''
    f = open("bs.txt", "w")
    f.write(soup.prettify())
    f.close()
    '''
    paragraphs = soup.select("div.p-feature-item")
    print(f"got {len(paragraphs)} paragraps")
    if len(paragraphs) == 0:
        failed_links.append(link)
    else:
        model_name = soup.select(".p-type")[0].contents[0]
        #print(f"model name is {model_name}")

        safe_name = model_name.replace("/", "_")

        try:
            os.mkdir("tmp/" + safe_name)
        except OSError:
            print ("Creation of the directory failed" )
        else:
            print ("Successfully created the directory " )

        img_url = soup.find(attrs={"name": "ISS_IMAGE"})['content'] + "&wid=1250"
        r = requests.get(img_url, stream=True)
        with open(f"tmp/{safe_name}/{safe_name}.png", 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

        description = []

        f = open(f"tmp/{safe_name}/{safe_name}.html", "w")
        for p in paragraphs:
            #print(p.p)
            if p.h3:
                f.write(f"<h3>{p.h3.contents[0]}</h3>\n")
            #print(f"h3 : {p.h3.contents[0][0:40]}")
            if p.img:
                #print(p.img)
                src = ''
                if p.img.has_attr('src'):
                    src = p.img['src']
                elif p.img.has_attr('data-src') in p.img:
                    src = p.img['data-src']
                #print(f"img: {src}")
                if src:
                    f.write(f"<img src='{src}'/>\n")
            #print(f"p  : {p.p.contents[0][0:40]}")
            if p.p:
                f.write(f"<p>{p.p.contents[0]}</p>\n")



        address = link + "/specifications"
        page = requests.get(address)
        content = page.content
        soup = BeautifulSoup(content, features="html5lib")


        chapters = soup.select("li.p-col-child.p-chapter-to-toggle")

        for chapter in chapters:
            chapter_heading = chapter.select(".p-heading-03.p-spec-title")
            f.write(f"<h4>{chapter_heading[0].contents[0]}</h4>\n")
            #print(f"<h4>{chapter_heading[0].contents[0]}</h4>\n")
            f.write("<ul>\n")
            dts = chapter.select("dt")
            dds = chapter.select("dd")
            for idx, dt in enumerate(dts):
                #print(dt)
                #print(list(dds[idx].children)[1])
                if list(dds[idx].children)[1].name == "ul":
                    #f.write
                    f.write(f"<li>{dt.contents[0]}</li>\n")
                    #print("fdt{dt.contents[0]}</li>\n")
                    f.write("<ul>\n")
                    #print("<ul>")
                    spans = dds[idx].select("span")
                    for span in spans:
                        #print(f"<li>{span.contents[0]}</li>")
                        f.write(f"<li>{span.contents[0]}</li>\n")
                    f.write("</ul>")
                    #print("</ul>")
                    #f.write(f"{dt.contents[0]}: {dt.next_sibling.name.contents[0]}\n")
                else:
                    f.write(f"<li>{dt.contents[0]}: {dds[idx].span.contents[0]}</li>\n")
                    #print(f"{dt.contents[0]}: {dds[idx].span.contents[0]}")
            f.write("</ul>\n")


        '''
        dds = soup.select("dd span")
        dts = soup.select("dt")

        f.write(f"{model_name}: технические характеристики")

        for idx, dt in enumerate(dts):
            print(f"{dt.contents[0]}: {dds[idx].contents[0]}")
        '''

        f.close()


'''

result = requests.get(initial_address)
content = result.content

soup = BeautifulSoup(content, features="html5lib")
selection = soup.select("a")

for a in selection:
    print(a.get("href"))

'''
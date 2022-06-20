from requests_html import HTMLSession
import pandas as pd

word = input("Enter the search keyword")
url = f'https://news.google.com/search?q={word}&hl=en-IN&gl=IN&ceid=IN%3Aen'

s = HTMLSession()
r= s.get(url)

r.html.render(sleep=10,scrolldown=8)

products = r.html.find('article')

newslist = []

startdate = input("Enter starting date in YYYYMMDD format")
enddate = input("Enter ending date in YYYYMMDD format")
y1 = int(startdate[0:4])
m1 = int(startdate[4:6])
d1 = int(startdate[6:])
y2 = int(enddate[0:4])
m2 = int(enddate[4:6])
d2 = int(enddate[6:])

for item in products:
    try:
        newsitem =  item.find('h3',first=True)
        newsitem2 = (item.find('div', first=True)).find('a', first=True)
        newsarticle = {
            'publisher' : newsitem2.text,
            'title' : newsitem.text,
            'link' : newsitem.absolute_links,
            'date' : item.find('time',first=True).attrs["datetime"][0:10]
        }
        y3 = int(newsarticle["date"][0:4])
        m3 = int(newsarticle["date"][5:7])
        d3 = int(newsarticle["date"][8:10])
        if(y1==y2):
            if (m1==m2):
                if (d3>=d1 and d3<=d2):
                    newslist.append(newsarticle)
            else:
                if (m3==m1):
                    if(d3>=d1):
                        newslist.append(newsarticle)
                elif (m3==m2):
                     if(d3<=d2):
                        newslist.append(newsarticle)
                else:
                    newslist.append(newsarticle)
        elif(y3>=y1 and y3<=y2):
            if (y3==y1):
                if(m3>=m1):
                    newslist.append(newsarticle)
            elif(y3==y2):
                if(m3<=m2):
                    newslist.append(newsarticle)
            else:
                newslist.append(newsarticle)
    except:
        pass

df = pd.DataFrame(newslist)
df.to_csv('News.csv')
print('Saved to CSV File.')
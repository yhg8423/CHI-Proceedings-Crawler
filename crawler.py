from bs4 import BeautifulSoup
import requests
import sys
import io

# encoding
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

chi_addr = ["https://chi2018.acm.org/attending/proceedings/", "https://chi2019.acm.org/for-attendees/proceedings/"]
paper_list = []

for addr in chi_addr:
    req = requests.get(addr)
    html = req.text

    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", attrs={'class': 'DLcontent'})
    title_a = soup.findAll("a", attrs={'class': 'DLtitleLink'})
    author_ul = soup.findAll("ul", attrs={'class': 'DLauthors'})
    abstract_div = soup.findAll("div", attrs={'class': 'DLabstract'})

    for i in range(len(title_a)):
        try:
            paper = {'title': '', 'authors': [], 'abstract': ''}
            
            # paper title
            paper['title'] = title_a[i].text

            # paper authors
            authors = author_ul[i].findAll("li")    
            for j in range(len(authors)):
                author = authors[j].contents[0]
                paper['authors'].append(author)

            # paper abstract
            paper['abstract'] = abstract_div[i].find("p").contents[0]
            paper_list.append(paper)
        except:
            break

f = open('./paper_info.txt', 'w', encoding='utf8')
for paper in paper_list:
    print(paper)
    f.write(paper['title'] + "\n")
    for author in paper['authors']:
        f.write(author+", ")
    f.write("\n")
    f.write(paper['abstract'])
    f.write("\n\n")
f.close
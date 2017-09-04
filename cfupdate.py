import urllib.request
import bs4 as bs
import html5lib
import json
import os
def updateCf():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    source1 = opener.open("http://www.codeforces.com/problemset")
    soup1 = bs.BeautifulSoup(source1, 'html5lib')
    endpage = int(soup1.findAll('span', {"class": "page-index"})[-1].getText())
    latest = soup1.find('td', {"class": "id"}).text
    with open('codeforces.json', 'r') as codeforces:
        data = json.load(codeforces)
        latest1=data['latest']
        if latest1 == latest:
            return
        else:
            data['latest']=latest
            signal=True
            for i in range(1, endpage + 1):
                if signal==False:
                    break
                source = opener.open("http://www.codeforces.com/problemset/page/" + str(i))
                soup = bs.BeautifulSoup(source, 'html5lib')
                for s1 in soup.findAll('td', {"class": "id"}):
                    idcur = s1.text
                    s2 = s1.find('a')
                    if idcur==latest1:
                        signal=False
                        break
                    else:
                        save = "http://www.codeforces.com" + s2.get('href')
                        if 'A' in save:
                            data['A'].append(save)
                        elif 'B' in save:
                            data['B'].append(save)
                        elif 'C' in save:
                            data['C'].append(save)
                        elif 'D' in save:
                            data['D'].append(save)
                        elif 'E' in save:
                            data['E'].append(save)
                        elif 'F' in save:
                            data['F'].append(save)
                        else:
                            data['OTHERS'].append(save)
    os.remove('codeforces.json')
    with open('codeforces.json','w') as codeforces:
        json.dump(data,codeforces)
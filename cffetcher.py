import urllib.request
import bs4 as bs
import html5lib
import json
import os

def updateCf():
    print("Checking if codeforces.json is up to date......")
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
            print("up to date")
            return
        else:
            print("not up to date")
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
                        print("Extracted "+s2.text)
    os.remove('codeforces.json')
    with open('codeforces.json','w') as codeforces:
        json.dump(data,codeforces)


def getcf():
    print("Extracting question urls.Please wait......")
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    source1 = opener.open("http://www.codeforces.com/problemset")
    soup1 = bs.BeautifulSoup(source1, 'html5lib')
    endpage = int(soup1.findAll('span', {"class": "page-index"})[-1].getText())
    latest = soup1.find('td', {"class": "id"}).text
    cflistA = []
    cflistB = []
    cflistC = []
    cflistD = []
    cflistE = []
    cflistF = []
    cflistOTHERS = []
    for i in range(1, endpage + 1):
        source = opener.open("http://www.codeforces.com/problemset/page/" + str(i))
        soup = bs.BeautifulSoup(source, 'html5lib')
        for s1 in soup.findAll('td', {"class": "id"}):
            s2 = s1.find('a')
            save = "http://www.codeforces.com" + s2.get('href')
            if 'A' in save:
                cflistA.append(save)
            elif 'B' in save:
                cflistB.append(save)
            elif 'C' in save:
                cflistC.append(save)
            elif 'D' in save:
                cflistD.append(save)
            elif 'E' in save:
                cflistE.append(save)
            elif 'F' in save:
                cflistF.append(save)
            else:
                cflistOTHERS.append(save)
            print("extracted"+s2.text)
    with open('codeforces.json', 'w') as codeforces:
        json.dump({"latest": latest, "A": cflistA, "B": cflistB, "C": cflistC, "D": cflistD, "E": cflistE, "F": cflistF,
                   "OTHERS": cflistOTHERS}, codeforces)

def download():
    try:
        print("preparing to download")
        with open('codeforces.json', 'r') as codeforces:
            qcf = json.load(codeforces)
            to_be_downloaded = ['A','B'] # YOU CAN PUT 'C','D','E','F','OTHERS'
            left_limit=0 #CHANGE IT TO SET THE LEFT LIMIT
            total_no
            for i in to_be_downloaded:
                for j in range(left_limit,len(qcf[i])):
                    print("index= "+str(j))
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    source1 = opener.open(qcf[i][j])
                    soup = bs.BeautifulSoup(source1, 'html5lib')
                    soup1 = soup.find('div', {"class": "problemindexholder"})
                    soup2 = soup1.find_all('img')
                    try:
                        title = soup1.find('div', {"class": "title"}).text
                    except:
                        continue
                    title = "".join(filter(str.isalpha, title))
                    path = os.getcwd() + "/" + i + "/" + title
                    path1 = os.getcwd() + "/" + i + "/" + title + "/" + "question.html"
                    try:
                        os.makedirs(os.path.dirname(path1))
                    except OSError as exc:  # Guard against race condition
                        if exc.strerror == "Cannot create a file when that file already exists":
                            print("file exists "+str(j))
                            continue
                        else:
                            print(exc.strerror)
                    for s in soup2:
                        link = s.get('src')
                        s['src'] = path + "/" + os.path.basename(link)
                        urllib.request.urlretrieve("http://codeforces.com" + link, path + "/" + os.path.basename(link))
                        print("downloaded image " + os.path.basename(link))
                    with open(path1, 'w', encoding='utf-8') as abc:
                        abc.write(str(soup1))
                    print("downloaded question " + title)
    except:
        print("Some error occured")

try:
    if os.path.exists('codeforces.json'):
        updateCf()
    else:
        getcf()
except:
    print("some network error please try again")


if __name__ == '__main__':
    download()

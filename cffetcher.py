import urllib.request
import bs4 as bs
import html5lib
import json
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
source1=opener.open("http://www.codeforces.com/problemset")
soup1=bs.BeautifulSoup(source1,'html5lib')
endpage=int(soup1.findAll('span',{"class":"page-index"})[-1].getText())
latest=soup1.find('td',{"class":"id"}).text
cflistA=[]
cflistB=[]
cflistC=[]
cflistD=[]
cflistE=[]
cflistF=[]
cflistOTHERS=[]
for i in range(1,endpage+1):
    source = opener.open("http://www.codeforces.com/problemset/page/"+str(i))
    soup = bs.BeautifulSoup(source, 'html5lib')
    for s1 in soup.findAll('td', {"class": "id"}):
        s2 = s1.find('a')
        save="http://www.codeforces.com"+s2.get('href')
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
with open('codeforces.json','w') as codeforces:
    json.dump({"latest":latest,"A":cflistA,"B": cflistB,"C": cflistC,"D": cflistD,"E": cflistE,"F": cflistF,"OTHERS": cflistOTHERS},codeforces)
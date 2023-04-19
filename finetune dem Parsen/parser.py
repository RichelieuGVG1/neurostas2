import requests
from bs4 import BeautifulSoup
import os
import time

try:
    author='чехов'
    os.mkdir('тексты')
    start_time=time.time()
    
    def decode(st):
        if '(' in st: st=st[:st.index('(')-1]
        st1=str(st.encode('cp1251'))
        st2=st1.replace(r'\x','%')
        st1=st2.replace(' ', '+')
        return st1[2:len(st1)-1]

    with open('base1.txt', 'r', encoding='utf-8') as file:
        base=file.read()
        base=base.split('\n')
        

    for st in base:
        print('Counting', st, '...')

        url = f'https://ilibrary.ru'
        response = requests.get(url+'/search.phtml?q='+decode(st)).text
        soup = BeautifulSoup(response, "lxml")
        
        print(url+'/search.phtml?q='+decode(st))
        for li in soup.find_all('li'):
            if author in str(li).lower():
                link=li.find('a').get('href')
                #print(li)
                break

            
        response=requests.get(url+link)
        soup = BeautifulSoup(response.text, "html.parser")
        text=soup.find_all("span", class_="p")
        tex=''
        for a in text:
            tex+=a.text

        st=st.replace('?','')
        tex=tex.replace('Антон Чехов','')
        with open(f'тексты/{st}.txt', 'w', encoding='utf-8') as file:
            file.write(tex)
            file.close()
    
        print(st, 'counted successfully!\n\n')
    print(f'programm finished normally. Time elapsed: {str(time.time()-start_time)[:5]} s')

    
except Exception as e:
    print(e)
finally:
    os.system('pause')

# -*- encoding: utf-8 -*-
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def buildtransp(type):
    cidade =paginas[type]['cidade'].upper()
    estado = paginas[type]['UF'].upper()
    url = str(f'{urlbase}{cidade.lower()}-{estado.lower()}')
    driver.get(url)
    time.sleep(3)
    last_height = driver.execute_script("return document.body.scrollHeight")
    countScroll = 0
    print(f'\r{cidade}-{estado}', end="")
    print('                                ')
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
        time.sleep(1)
        countScroll += 1
        print (f'\r{countScroll}- Scroll Down',end="")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + Keys.HOME)
            countScroll = 0
            # print(f'{cidade}-{estado}')
            print('\rValidando Página',end="")
            break
        last_height = new_height

    element = driver.find_element(By.XPATH,"//section[@class='l-sectionMap__results__companies']")
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    name1 = 'a'
    for div in soup.findAll('div', attrs={'class':'ng-scope'}):
        name=div.find('h2', attrs={'class':'m-boxCompany__A__info__name__txt ng-binding'})
        mailto=div.find('a', href=True, attrs={'class':'s-textBreakAll ng-binding'})
        if mailto :
            if name != name1 :
               transportadora.append(name.text)
               email.append(mailto.text)
               name1 = name

    df = pd.DataFrame({'Transportadora':transportadora,'Email':email,'Cidade':cidade, 'UF':estado})
    return df

def removeDuplicates(df):
    df = df.sort_values(['UF','Cidade','Transportadora', 'Email'])
    df = df.drop_duplicates(subset=['UF','Cidade','Email'], keep='first')
    return df

#print('##########################################################################################################')
### INIT ###
# clear terminal
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()
# Grab content from URL (Pegar conteúdo HTML a partir da URL)
bulktransp=[] #List to store name of all carriers + emails + estados

# File name to create
trecho = 'transportadoras.csv'

# Cities and Estates
paginas = {
    'sp': {'cidade': 'piracicaba','UF': 'SP'},
    'sp': {'cidade': 'rio-claro','UF': 'SP'},
    'sp': {'cidade': 'araraquara','UF': 'SP'},
    'sp': {'cidade': 'presidente-prudente','UF': 'SP'},
    'sp': {'cidade': 'campinas','UF': 'SP'},
    'sp': {'cidade': 'sorocaba','UF': 'SP'},
    'sp': {'cidade': 'ribeirao-preto', 'UF': 'SP'},
    'sp': {'cidade': 'marilia', 'UF': 'SP'},
    'sp': {'cidade': 'santos', 'UF': 'SP'},
    'sp': {'cidade': 'ourinhos', 'UF': 'SP'},
    'sp': {'cidade': 'ubatuba', 'UF': 'SP'},
    'ac': {'cidade': 'rio-branco', 'UF': 'AC'},
    'al': {'cidade': 'maceio', 'UF': 'AL'},
    'ap': {'cidade': 'macapa', 'UF': 'AP'},
    'am': {'cidade': 'manaus', 'UF': 'AM'},
    'ba': {'cidade': 'salvador', 'UF': 'BA'},
    'ce': {'cidade': 'fortaleza', 'UF': 'CE'},
    'df': {'cidade': 'brasilia', 'UF': 'DF'},
    'es': {'cidade': 'vitoria', 'UF': 'ES'},
    'go': {'cidade': 'goiania', 'UF': 'GO'},
    'ma': {'cidade': 'sao-luis', 'UF': 'MA'},
    'mt': {'cidade': 'cuiaba', 'UF': 'MT'},
    'ms': {'cidade': 'campo-grande', 'UF': 'MS'},
    'mg': {'cidade': 'belo-horizonte', 'UF': 'MG'},
    'pa': {'cidade': 'belem', 'UF': 'PA'},
    'pb': {'cidade': 'joao-pessoa', 'UF': 'PB'},
    'pr': {'cidade': 'curitiba', 'UF': 'PR'},
    'pe': {'cidade': 'recife', 'UF': 'PE'},
    'pi': {'cidade': 'teresina', 'UF': 'PI'},
    'rj': {'cidade': 'rio-de-janeiro', 'UF': 'RJ'},
    'rn': {'cidade': 'natal', 'UF': 'RN'},
    'rs': {'cidade': 'porto-alegre', 'UF': 'RS'},
    'ro': {'cidade': 'porto-velho', 'UF': 'RO'},
    'rr': {'cidade': 'boa-vista', 'UF': 'RR'},
    'sc': {'cidade': 'florianopolis', 'UF': 'SC'},
    'se': {'cidade': 'aracaju', 'UF': 'SE'},
    'to': {'cidade': 'palmas', 'UF': 'TO'},
}

# website to scraping
urlbase= 'https://www.transvias.com.br/rotas/sao-paulo-sp/'

transportadora=[] #List to store name of transportadora
email=[] # List to store email of transportadora
bdTransportadoras = pd.DataFrame() # DataFrame to store carriers information

for k in paginas:
    option = Options()
    option.headless = True
    driver = webdriver.Firefox()  # to not see firefox working use the line below
    #driver = webdriver.Firefox(options=option)
    bd = buildtransp(k)
    if bdTransportadoras.empty:
        bdTransportadoras = bd
    else:
        bdTransportadoras = pd.merge(bdTransportadoras, bd, how = 'outer')
    driver.quit()

df = removeDuplicates(bdTransportadoras) # sort and remove duplicates
df.columns = ['Transportadora', 'Email','Cidade','UF'] # insert title in columns
df.to_csv(trecho, index=False, encoding='utf-8') # save CSV file
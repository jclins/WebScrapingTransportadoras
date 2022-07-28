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
    estado = paginas[type]['estado'].upper()
    url = str(f'{urlbase}{cidade.lower()}-{estado.lower()}')
    driver.get(url)
    time.sleep(3)
    last_height = driver.execute_script("return document.body.scrollHeight")
    countScroll = 0
    print(f'{cidade}-{estado}')
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
        time.sleep(1)
        countScroll += 1
        print (f'{countScroll}- Scroll Down')
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + Keys.HOME)
            countScroll = 0
            clear()
            print(f'{cidade}-{estado}')
            print('Validando Página')
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

    df = pd.DataFrame({'Transportadora':transportadora,'Email':email,'Cidade':cidade, 'Estado':estado})
    return df

def removeDupli(df):
    df = df.sort_values(['Estado','Cidade','Transportadora', 'Email'])
    df = df.drop_duplicates(subset=['Estado','Cidade','Email'], keep='first')
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
    'sp': {'cidade': 'piracicaba','estado': 'SP'},
    'sp': {'cidade': 'rio-claro','estado': 'SP'},
    'sp': {'cidade': 'araraquara','estado': 'SP'},
    'sp': {'cidade': 'presidente-prudente','estado': 'SP'},
    'sp': {'cidade': 'campinas','estado': 'SP'},
    'sp': {'cidade': 'sorocaba','estado': 'SP'},
    'sp': {'cidade': 'ribeirao-preto', 'estado': 'SP'},
    'sp': {'cidade': 'marilia', 'estado': 'SP'},
    'sp': {'cidade': 'santos', 'estado': 'SP'},
    'sp': {'cidade': 'ourinhos', 'estado': 'SP'},
    'sp': {'cidade': 'ubatuba', 'estado': 'SP'},
    'ac': {'cidade': 'rio-branco', 'estado': 'AC'},
    'al': {'cidade': 'maceio', 'estado': 'AL'},
    'ap': {'cidade': 'macapa', 'estado': 'AP'},
    'am': {'cidade': 'manaus', 'estado': 'AM'},
    'ba': {'cidade': 'salvador', 'estado': 'BA'},
    'ce': {'cidade': 'fortaleza', 'estado': 'CE'},
    'df': {'cidade': 'brasilia', 'estado': 'DF'},
    'es': {'cidade': 'vitoria', 'estado': 'ES'},
    'go': {'cidade': 'goiania', 'estado': 'GO'},
    'ma': {'cidade': 'sao-luis', 'estado': 'MA'},
    'mt': {'cidade': 'cuiaba', 'estado': 'MT'},
    'ms': {'cidade': 'campo-grande', 'estado': 'MS'},
    'mg': {'cidade': 'belo-horizonte', 'estado': 'MG'},
    'pa': {'cidade': 'belem', 'estado': 'PA'},
    'pb': {'cidade': 'joao-pessoa', 'estado': 'PB'},
    'pr': {'cidade': 'curitiba', 'estado': 'PR'},
    'pe': {'cidade': 'recife', 'estado': 'PE'},
    'pi': {'cidade': 'teresina', 'estado': 'PI'},
    'rj': {'cidade': 'rio-de-janeiro', 'estado': 'RJ'},
    'rn': {'cidade': 'natal', 'estado': 'RN'},
    'rs': {'cidade': 'porto-alegre', 'estado': 'RS'},
    'ro': {'cidade': 'porto-velho', 'estado': 'RO'},
    'rr': {'cidade': 'boa-vista', 'estado': 'RR'},
    'sc': {'cidade': 'florianopolis', 'estado': 'SC'},
    'se': {'cidade': 'aracaju', 'estado': 'SE'},
    'to': {'cidade': 'palmas', 'estado': 'TO'},
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

df = removeDupli(bdTransportadoras) # sort and remove duplicates
df.columns = ['Transportadora', 'Email','Cidade','Estado'] # insert title in columns
df.to_csv(trecho, index=False, encoding='utf-8') # save CSV file
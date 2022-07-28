# WebScraping de Transportadoras

App para WebScraping de Transportadoras por Estado

* 1- Criar ambiente virtual (Windows)
0. cmd
1. python -m venv ./venv
2. excecutar:  .\venv\Scripts\activate.bat
3. python.exe -m pip install --upgrade pip

* 2- Instalar dependencias
==> pip install -r requirements.txt
or:
    2.1- pip install pandas
    2.2- pip install lxml
    2.3- pip install beautifulsoup4
    2.4- pip install selenium


* 3. Criar Procfile
    web: gunicorn NOME_ARQUIVO:app
4. pip install gunicorn
5. pip freeze > requirements.txt

######################


### copy geckodriver.exe and chromedriver.exe to %HOMEPATH%\AppData\Roaming\Python\Python310\Scripts
C:\Users\USER\AppData\Local\Programs\Python\Python310


https://github.com/mozilla/geckodriver/releases
https://chromedriver.storage.googleapis.com/index.html

#########################################

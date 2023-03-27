from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import re
import wget

# path à modifier en fonction d'où se trouver le chromedriver
path = '/home/lucien/Documents/final_project_Essec/scrapping/chromedriver'

#Création dossier pour les saumons : il faudra généraliser pour d'autres familles de poissons
try:
   os.mkdir('Salmonidae')
except:
    print('dossier déjà existant')


options = Options()
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=path)

# Atteindre la page des 71 espèces de saumons
driver.get('https://www.inaturalist.org/observations?place_id=any&taxon_id=47520&view=species')

time.sleep(3)

os.chdir("Salmonidae")

### SCROLLER EN BAS DE PAGE POUR ATTEINDRE TOUS LES LIENS
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(3)

# Créer une liste de listes avec tous les liens des espèces et leurs noms
links = []
for species in driver.find_elements(By.CSS_SELECTOR, "div[ng-repeat='t in taxa']"):

    link = species.find_element(By.CSS_SELECTOR, "div[class='photometa']").find_element(By.CSS_SELECTOR,'a').get_attribute('href') #on récupère les liens des espèces
    name = species.find_element(By.CSS_SELECTOR, "a[class^='display-name']").get_attribute('innerHTML').strip().split('>')[-1] #permet de récupérer le nom de l'espèce
    links.append([link,name])

# On boule sur les 71 espèces de saumons, pour chaque espèce on boucle sur les toutes les pages disponibles et on stock les photos dans un dossier du nom de l'espèce
for specie in links:

    j = 0

    os.mkdir(specie[1])
    os.chdir(specie[1])

    print(specie[1])

    i = 0
    res = True 
    while res :

        time.sleep(3)
        
        i += 1
        
        url = specie[0] + str(i) + '&subview=table' #on fait comme si on avait cliqué sur l'image (qui est une imagette) pour atteindre la page de la photo, qui est en fait le même ilen avec un numéro derrière
        
        driver.get(url)

        time.sleep(3)

        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(3)

        links = []
        try :
            for el in driver.find_elements(By.CSS_SELECTOR,"tr[class='ng-scope']"):
                num = re.search('\".*\"',el.find_element(By.CSS_SELECTOR, "a[class^='img']").get_attribute('style')).group()[1:-1] #on récupère les liens des photos en étudiant le style css
                links.append(num)
        
        except :
            print('page finished')
        
        print(len(links))

        if len(links) == 0 or len(os.listdir('.')) >= 300:
            res = False
            os.chdir('..')
            break
        
        
        for y,u in enumerate(links,j+1):
            
            time.sleep(0.5)
            try : 
                wget.download(u,str(y)+'.jpeg')
            except :
                print('something went wrong for image at url n°' + str(y) + 'that is : ' + u)
                break
            w = y
        
        j = w


driver.quit()
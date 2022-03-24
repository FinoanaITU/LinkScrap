import time
import re
from selenium.webdriver.common import keys
from Scrap.Source.utilFunction import utilFunctions
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from ..connection import connect

class linkeDin():
    def __init__(self):
        self.connexion = connect()
        self.driver = self.connexion.driver
        self.util = utilFunctions(self.driver)
        self.tabOpen = []
        self.compteActif = ""

    def loginCheck(self,username, password):
        print('ato---------')
        result = False
        try:
            self.connexion.salesNavigator()
            self.util.wait_located('XPATH','//*[@id="app__container"]/main/div[2]')
            self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
            self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
            self.util.click_element(self.driver,'//*[@id="organic-div"]/form/div[3]/button')
            result = True
        except Exception as e:
            print(e)
        
        return result

    def  listSocieteProspect(self, url, category, pageDebut,pageFin, comptes):
        # self.util.wait_located('XPATH','//*[@id="username"]')
        if comptes == "Koloina":
            conect = self.loginCheck('koloinasariaka@gmail.com','Fortunes76!')
        elif comptes == "Finoana":
            conect = self.loginCheck('finoanaandriatsilavoo@gmail.com','FaithLinke1234')
        elif comptes == "Géraud":
            conect = self.loginCheck('lamazere@breathe.paris','Fortunes67!')
        self.compteActif = comptes
        result = []
        if conect:
            time.sleep(2)
            self.driver.get(url)
            print('apres get-----------------------')
            result = self.listeParPage(result, category, pageDebut,pageFin)
        # self.driver.quit()
        return result
            


    def listeParPage (self, result, category, pageDebut,pageFin):
        self.util.wait_located_All_xpath('//*[@id="results"]')
        self.util.scroll_with_limit(self.driver,50,150)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        listSociete = soup.find_all('li',attrs={'class':'search-results__result-item'})
        for i,societe in enumerate(listSociete):
            print(i,'----------------')
            if category == 'societe':
                societeRow = societe.find('dt')
                data = {}
                if societeRow != None:
                        lien = societeRow.find('a')
                        data['nom_societe'] = str(lien.getText()).replace('\n','').strip()
                        data['lien'] = 'https://www.linkedin.com/'+str(lien['href'])
                        data = self.switchBetweenTab(data, lien, self.driver,category)
                        # print(data)
            elif category == 'prospect':
                data = {}
                nomPrenom = societe.find('dt')
                if nomPrenom != None:
                    lien = nomPrenom.find('a')
                    npData = str(lien.getText()).replace('\n','').strip().split(' ')
                    data['prenom'] = npData[0]
                    i = 1
                    nom = ''
                    while i < len(npData):
                         nom = nom + npData[i] + ' '
                         i = i + 1
                    data['nom'] = nom
                    data['lienLinkeDin'] = 'https://www.linkedin.com/'+self.formatLinkSalesToLinkedin(lien['href'])
                    data['lienSales'] = 'https://www.linkedin.com/'+lien['href']

                    ##Poste
                    detailAll = societe.find_all('dd')
                    spanAll = detailAll[1].find_all('span')
                    if len(spanAll) > 0:
                        data['poste'] = str(spanAll[0].getText()).replace('\n','').replace(' ','_').strip()
                        ##societe
                        socLien  = spanAll[2].find('a')
                        socTabName = spanAll[2].find_all('span')
                        data['Societe'] = str(socTabName[0].getText()).replace('\n','').strip()
                        data = self.switchBetweenTab(data, socLien, self.driver,category)
                        # print(data)
            print(data)
            result.append(data)
        ##pagination
        self.util.wait_located_All_xpath('//*[@id="content-main"]/div[1]/div')
        messNoresult = soup.find('p',attrs={'class':'search-results__no-results-message'})
        btnNext = soup.find('button',attrs={'class':'search-results__pagination-next-button'})
        if  messNoresult == None and btnNext != None: 
            pathBtn = self.util.xpath_soup(btnNext)
            try:
                self.util.click_element(self.driver,pathBtn)
                pageDebut = pageDebut + 1
                print('<-----------page actuel-----------> = '+ str(pageDebut))
                if pageDebut == pageFin and pageFin != 0:
                    return result
                self.listeParPage(result, category,pageDebut, pageFin)
            except ElementClickInterceptedException as e:
                print(e)
                pass
        return result

    def enrichirList (self, listSociete):
        conect = self.loginCheck('lamazere@breathe.paris','Fortunes67!')
        result = []
        if conect:
            time.sleep(2)
            for societe in listSociete: 
                self.driver.get(societe['lien'])
                socEnrichi = self.getContentSociete(societe)
                result.append(socEnrichi)
        return result

    def getContentSociete (self,societe):
        self.util.wait_located_All_xpath('//*[@id="account"]')
        time.sleep(1)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if self.compteActif == "Koloina":
            descriptionElement = soup.find('div',id='ember53-account-description-line-clamper')
            siteElement = soup.find('a',id='ember66')
        elif self.compteActif == "Finoana":
            descriptionElement =  soup.find('div',id='ember61')
            siteElement = soup.find('a',id='ember66') if soup.find('a',id='ember66') != None else soup.find('a',id='ember69') 

        societe['description'] = descriptionElement.getText() if descriptionElement else ""
        site = siteElement
        if site != None:
            societe['site'] = self.formatHref(site['href'])
        societe['Societe'] = str(soup.find('div',id='ember58').getText()).replace('\n','').strip()
        return societe

    def societeEmployés (self,societe):
        try:
            self.util.wait_visible_element('//*[@id="account"]')
        except Exception as e:
            print(e,'ERROR----- WAIT')
            pass
        time.sleep(2)
        societe = self.getContentSociete(societe)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        divContent = soup.find_all('div', attrs={'class':'t-14 mt4'})
        alllink = divContent[0].findAll('a') if len(divContent) > 0 else []
        # societe['description'] =  soup.find('div',id='ember54').getText()
        if len(alllink) > 0:
            for link in alllink:
                checkEmp = re.search('(?<=Tous les employés \()(.*)(?=\))', link.getText())
                checkDec = re.search('(?<=Décideurs \()(.*)(?=\))', link.getText())
                if checkEmp != None:
                    societe['nbr_employer'] = checkEmp.group(0)
                    societe['lien_employers'] = 'https://www.linkedin.com'+str(link['href'])
                if checkDec != None:
                    societe['nbr_decideur'] = checkDec.group(0)
                    societe['lien_decideur'] = 'https://www.linkedin.com'+str(link['href'])
        else:
            societe['remarque'] = 'à verifier'
        return societe


    def switchBetweenTab(self, data, socLien, driver,category):
        lienSocUtil = driver.find_element_by_xpath(self.util.xpath_soup(socLien))
        main_win = driver.current_window_handle
        lienSocUtil.send_keys(Keys.CONTROL + Keys.ENTER)
        self.tabOpen = self.util.switch_one_tab(driver,self.tabOpen)
        time.sleep(1)
        multiValue  = self.util.find_exist(driver,'//*[@id="results"]')
        pageIntrouvable = self.util.find_exist(driver,'//*[@id="content-main"]/div/div/figure')
        if multiValue == False and pageIntrouvable == False:
            if category == 'prospect':
                data = self.getContentSociete(data)
            elif category == 'societe':
                data = self.societeEmployés(data)

        else:
            data['remarque'] = 'à verifier'
        driver.close()
        time.sleep(1)
        driver.switch_to_window(main_win)
        return data

    def formatLinkSalesToLinkedin(self, link):
        tab = link.split(',')
        li = tab[0].replace('/sales/people','in')
        return li

    def formatHref(self, href):
        rmhttp = str(href).replace('http://','')
        rmhttps = rmhttp.replace('https://','')
        rmwww = rmhttps.replace('www.','')
        result = rmwww.split('/',1)[0]
        return result


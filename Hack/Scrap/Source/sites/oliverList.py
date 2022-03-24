from os import name
from Scrap.Source.utilFunction import utilFunctions
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
from ..connection import connect
import time
import re
class oliverList():
    def __init__(self):
        self.connexion = connect()
        self.driver = self.connexion.driver
        self.util = utilFunctions(self.driver)
        self.listAlreadyCheck = []
        self.user = []

    def selectUser(self,userName):
        if userName == "Karine":
            self.user = ['karine@mmc.paris','Fortunes76!']
        elif userName == "Dilypse":
            self.user = ['valerie.dilypse@gmail.com','Fortunes76!']
        
    def dashboard (self):
        res = True
        try:
            self.connexion.oliverList()
            self.util.wait_located_All_xpath('//*[@id="app"]/div[1]/div/div/div[2]/div')
            self.util.get_el_by_xpath(self.driver,'//*[@id="app"]/div[1]/div/div/div[2]/div/form/div[1]/input').send_keys(self.user[0])
            self.util.get_el_by_xpath(self.driver,'//*[@id="app"]/div[1]/div/div/div[2]/div/form/div[2]/input').send_keys(self.user[1])
            self.util.click_element(self.driver,'//*[@id="app"]/div[1]/div/div/div[2]/div/form/div[3]/div[1]/button')
        except Exception as e :
            print(e)
            res = False
        return res

    def actionToDo (self, action,date, userName):
        result = []
        self.selectUser(userName)
        if self.dashboard():
            if action == 'campagne':
                self.util.wait_located('XPATH','//*[@id="navbarSupportedContent"]/ul/div/div[4]')
                self.selectedCampagne()
                result = self.listCampage(date)
            elif action == 'oportunite':
                print('ato------')
                result = self.entrepriseListe()
                print(result)
        return result


    def listCampage (self,date):
        result = []
        self.util.scroll_to_element(self.driver,'//*[@id="app"]/div[1]/div/section[2]/main/section/main/div/div/div/section[2]/div/div/div[2]')
        time.sleep(2)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table',attrs={'class':'table table-hover card-style min-width-table'})
        allTr = table.find_all('tr')
        for i,tr in enumerate(allTr):
            print(i,'----------------------------------------')
            pointer = tr.find_all('a')
            data = {}
            for p in pointer:
                content = p.contents
                toCheck = str(content[0]).replace('\n','').replace("-",'').replace(' ','').replace('(','').replace(')','').replace('.','').replace('/','')
                if toCheck.isalnum():
                    pathSociete = self.util.xpath_soup(content[0])
                    campagneName = str(content[0]).replace('\n','').strip()
                    if campagneName not in self.listAlreadyCheck:
                        self.util.wait_click_xpath(pathSociete)
                        try:
                            time.sleep(2)
                            print(campagneName)
                            self.util.click_element(self.driver,pathSociete)
                        except ElementClickInterceptedException as e:
                            time.sleep(2)
                            self.util.click_element(self.driver,pathSociete)

                        data['campagne'] = campagneName
                        data['statistique'] = self.societeSatistique(date)
                        self.listAlreadyCheck.append(campagneName)
                        self.selectedCampagne()
                        print(self.listAlreadyCheck)
            if len(data) > 0 and self.checkStatData(data['statistique']) == False:
                result.append(data)
                self.util.saveToFile('C:\oliverCache\cache.txt',str(result))
        return result
                    

    
    def societeSatistique (self,date):
        try:
            self.util.wait_located_All_xpath('//*[@id="app"]')
            self.util.wait_click_xpath('//*[@id="app"]/div/div/div/div/div[7]/span')
            self.util.click_element(self.driver,'//*[@id="app"]/div/div/div/div/div[7]/span')
            self.util.wait_click_xpath('//*[@id="app"]/section/div/div/div[3]/div[1]')
            ##remplire filtre
            time.sleep(1)
            self.util.get_el_by_ID(self.driver,'startDatePicker').clear()
            self.util.get_el_by_ID(self.driver,'startDatePicker').send_keys(date)
            self.util.get_el_by_ID(self.driver,'endDatePicker').clear()
            self.util.get_el_by_ID(self.driver,'endDatePicker').send_keys(date)
            time.sleep(1)
            self.util.click_element(self.driver,'//*[@id="app"]/section/div/div/div[2]/div/div/div[3]/button')
            time.sleep(5)
            self.util.wait_located_All_xpath('//*[@id="app"]/section/div/div/div[3]/div[1]/div[1]/div/div/div/div[1]/span')
        
            data = {}
            envoi = str(self.util.get_el_by_xpath(self.driver,'//*[@id="app"]/section/div/div/div[3]/div[1]/div[1]/div/div/div/div[1]/span').text).replace("(",'').replace(")","")
            livre = str(self.util.get_el_by_xpath(self.driver,'//*[@id="app"]/section/div/div/div[3]/div[1]/div[2]/div/div/div/div[1]/span[2]').text).replace("(",'').replace(")","")
            data ['envoi'] = envoi
            data ['livrer'] = livre
            data ['ouvert'] = str(self.util.get_el_by_xpath(self.driver,'//*[@id="app"]/section/div/div/div[3]/div[1]/div[3]/div/div/div/div[1]/span[2]').text).replace("(",'').replace(")","")
            data ['cliquer'] = str(self.util.get_el_by_xpath(self.driver,'//*[@id="app"]/section/div/div/div[3]/div[1]/div[4]/div/div/div/div[1]/div[2]/div/span[2]').text).replace("(",'').replace(")","")
            data ['repondue'] = str(self.util.get_el_by_xpath(self.driver,'//*[@id="app"]/section/div/div/div[3]/div[1]/div[5]/div/div/div/div[1]/span[2]').text).replace("(",'').replace(")","")
            data ['bounce'] = int(envoi) - int(livre)

            return data
        except Exception as e:
            print(e)
            self.societeSatistique(date)

    def selectedCampagne (self):
        self.util.click_element(self.driver,'//*[@id="navbarSupportedContent"]/ul/div/div[4]')
        self.util.wait_located_All_xpath('//*[@id="app"]/div[1]/div/section[2]/main/section/main/div/div/div/section[2]/div/div/div[2]')
        self.util.scroll_to_element(self.driver,'//*[@id="app"]/div[1]/div/section[2]/main/section/main/div/div/div/section[2]/div/div/div[2]')
        time.sleep(1)
        self.util.click_element(self.driver,'//*[@id="dropdownCantPerPage"]')
        time.sleep(0.2)
        self.util.click_element(self.driver,'//*[@id="app"]/div[1]/div/section[2]/main/section/main/div/div/div/section[2]/div/div/div[2]/div[3]/div/a[5]')
        self.util.wait_located_All_xpath('//*[@id="app"]/div[1]/div/section[2]/main/section/main/div/div/div/section[2]/div/div/div[1]/div')
        
    def checkStatData(self,data):
        res = False
        if data['envoi'] == '0' and data['livrer'] == '0' and data['ouvert'] == '0' and data['cliquer'] == '0' and data['repondue'] == '0' and  data['bounce'] == 0:
            res = True
        return res

    def checkPagination (self):
        txtOportunite = self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/main/div/section/div/div/div/div[3]/div[1]/span').text
        total = re.search('(?<=sur )(.*)(?= Opportunités)', txtOportunite)
        actuelPage = re.search('(?<=à )(.*)(?= sur)', txtOportunite)
        page = int(str(total.group(0))) / int(str(actuelPage.group(0)))
        
        return round(page)

    def entrepriseListe(self):
        self.util.wait_located_All_xpath('//*[@id="navbarSupportedContent"]/ul/div/div[5]')
        self.util.click_element(self.driver,'//*[@id="navbarSupportedContent"]/ul/div/div[5]')
        self.util.wait_located_All_xpath('//*[@id="app"]/div[1]/div/main/div/section/div/div/div/div[2]/div[2]/table')
        script = 'window.scrollTo(0,document.body.scrollHeight);'
        self.driver.execute_script(script)
        time.sleep(1)
        nbrPage = self.checkPagination()
        page = range(nbrPage)
        print('nbr page = '+ str(page))
        data = []
        for i in page:
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table =  soup.find('table',attrs={'class':'table table-hover card-style min-width-table card-style'}) if i == 0 else soup.find('table',attrs={'class':'table table-hover'})
            trAll = table.find_all('tr')
            for tr in trAll:
                # print(tr.find_all('td'))
                allTd = tr.find_all('td')
                for j,td in enumerate(allTd):
                    if i == 0 and j == 1 and len(td) != 0:
                        data.append(self.findAllContactOportunity(td))
                    elif i > 0 and j == 0 and len(td) !=0:
                        data.append(self.findAllContactOportunity(td))
            print(data)
            if nbrPage > 0:
                print('click next----------------------')
                self.util.click_element(self.driver,'//*[@id="true"]/div/section/div/div/div[1]/div[3]/div[2]/button[2]')
                self.util.wait_located_All_xpath('//*[@id="true"]/div/section/div/div/div[1]')
                time.sleep(2)
        return data

    def findAllContactOportunity (self, entreprise):
        result = {}
        entrepriseName = str(entreprise.getText()).replace('\n','').strip()
        pathToClick = self.util.xpath_soup(entreprise)
        self.util.click_element(self.driver,pathToClick)
        self.util.wait_located_All_xpath('//*[@id="true"]/div/section/div/div/div[2]/div/section/main/div/div/div/div[1]/div[2]/div/div[2]')
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        allContactsCard = soup.find_all('div',attrs={'class':'opp card bg-light p-2 mt-2'})
        print('debut---------------')
        data = []
        for contact in allContactsCard:
            name = contact.find('div',attrs={'class':'d-flex mt-2'})
            linke = contact.find('a')
            poste = re.search('(?<=<div><small>)(.*)(?=<\/small><\/div><div>)', str(contact)).group(0)
            email = re.search('(?<=text-primary">)(.*)(?=<\/small><\/div>)', str(contact)).group(0)
            data.append({
                'name' : name.getText(),
                'linkedin' : linke['href'] if linke else "",
                'poste' : poste,
                'email' : email
            }) 
        result= {entrepriseName : data}
        return result
            

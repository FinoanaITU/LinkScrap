from Scrap.Source.utilFunction import utilFunctions
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
import time
from ..connection import connect
class verifCom():
    def __init__(self):
        self.connexion = connect()
        self.driver = self.connexion.driver
        self.util = utilFunctions(self.driver)
        self._countNext = 0

    def recherche (self, motCle,type):
        result = True
        self.connexion.toVerifCom()
        try:
            self.util.wait_located('XPATH','//*[@id="verif_main"]/div[3]/section[1]/div[2]/form')
            print('w---------------')
            self.util.wait_visible_element('//*[@id="didomi-popup"]/div/div')
            print('a---------------')
            self.driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]').click()
            print('dep---------------')
            if type == 'rs':
                input = self.util.get_el_by_ID(self.driver,'verif_rech_input1')
                input.send_keys(motCle)
                btn  = self.util.get_el_by_ID(self.driver, 'verif_btn_rech')
                btn.click()
            elif type == 'NAF':
                self.driver.find_element_by_xpath('//*[@id="verif_main"]/div[3]/section[1]/div[2]/form/p/a').click()
                # self.driver.find_element_by_xpath('//*[@id="navbar"]/div[4]/nav/ul/li[1]/a').click()
                # self.util.wait_located_All_xpath('//*[@id="verif_idMultiAdvanceSearch"]')
                # self.util.wait_located('ID','verif_ape')
                # self.driver.find_element_by_xpath('//*[@id="pepsia_player_close_0"]').click()
                time.sleep(5)
                print('ato---------------')
                self.util.scroll_to_element(self.driver, '//*[@id="verif_i_id_code_ape"]')
                self.driver.find_element_by_xpath('//*[@id="verif_i_id_code_ape"]').send_keys(motCle)
                # self.util.scroll_to_element(self.driver, '//*[@id="verif_defaillance2"]')
                # self.driver.find_element_by_xpath('//*[@id="verif_defaillance2"]').click()
                # self.util.scroll_to_element(self.driver, '//*[@id="verif_liste_entreprises_formulaire_btnvalider"]')
                # self.driver.find_element_by_xpath('//*[@id="verif_liste_entreprises_formulaire_btnvalider"]').click()
                self.util.scroll_to_element(self.driver, '//*[@id="verif_idMultiAdvanceSearch"]/div[2]/button')
                self.driver.find_element_by_xpath('//*[@id="verif_idMultiAdvanceSearch"]/div[2]/button').click()


        except Exception as e :
            result = False
            print (e)

        return result

    def findRS (self,dataFinal,type, nbrPageLimit):
        idTab = "tableliste" if type != 'NAF' else 'verif_conteneur'
        self.util.wait_located('ID',idTab)
        self.util.wait_located_All_xpath('//*[@id="'+idTab+'"]')
        self.util.scroll_to_element(self.driver,'//*[@id="verif_tableResult"]')
        # if type == 'NAF':
        #     self.util.wait_located('XPATH','//*[@id="pepsia_player_close_0"]')
        #     self.util.get_el_by_ID(self.driver, "pepsia_player_close_0").click()
        #     # self.driver.find_element_by_xpath('//*[@id="pepsia_player_close_0"]').click()
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(id='verif_tableResult')
        alltr = table.find_all('tr')
        for tr in alltr:
            tdInTr = tr.find_all('td')
            data = {}
            for td in tdInTr:
                classValue = td['class']
                value = td.find('a').contents
                if classValue[0] == 'verif_col1':
                    data['Raison_sociale'] = value[0]
                    data['lien'] = 'https://www.verif.com'+str(td.find('a')['href'])
                elif classValue[0] == 'verif_col2':
                    data['cp'] = value[0] if len(value) > 0 else ''
                elif classValue[0] == 'verif_col3' :
                    data['ville'] = value[0] if len(value) > 0 else ''
                elif classValue[0] == 'verif_col4':
                    data['activite'] = value[0] if len(value) > 0 else ''
                elif classValue[0] == 'verif_col5':
                    data['chiffre_afaire'] = str(value[0]).replace('\xa0', '') if len(value) > 0 else ''
            dataFinal.append(data)
            print(dataFinal)
        self.util.scroll_to_element(self.driver,'//*[@id="verif_decoup_page"]')
        time.sleep(2)
        print('decoupage---------------')
        # bntNext = self.util.get_el_by_slector(self.driver,'#verif_decoup_page > ul > li.li-next > a')
        # bntNext = self.driver.find_elements_by_css_selector(".btn-page btn-next")
        findNext = soup.find('a', attrs={'class':'btn-page btn-next'})
        if findNext != None and self._countNext < nbrPageLimit:
            xpathNext = self.util.xpath_soup(findNext) 
            # print(xpathNext)
            bntNext = self.driver.find_element_by_xpath(xpathNext)
        else:
            bntNext = False
        print('next----------------------')
        print(bntNext)
        if bntNext:
            try:
                bntNext.click()
            except ElementClickInterceptedException as e:
                bntNext = self.driver.find_element_by_xpath('//*[@id="verif_decoup_page"]/ul/li[7]/a')
                bntNext.click()
            time.sleep(1)
            self._countNext = self._countNext + 1
            dataFinal = self.findRS(dataFinal,type,nbrPageLimit)
        return dataFinal

    def getDirigeant(self,dataTab):
        result = []
        for i,row in enumerate(dataTab):
            if 'lien' in row:
                try:
                    self.driver.get(row['lien'])
                    self.driver.refresh()
                    time.sleep(1)
                    # if self.util.find_exist(self.driver,'//*[@id="didomi-popup"]/div/div'):
                    #     self.util.click_element(self.driver,'//*[@id="didomi-notice-agree-button"]')
                    # self.util.wait_located_All_xpath('//*[@id="fiche_entreprise"]/div[4]')
                    self.util.wait_located_All_xpath('//*[@id="fiche_entreprise"]/div[4]/div[2]/table[2]')
                    print('eto---------------')
                    print(i)
                    # if i == 0:
                    #     self.util.wait_visible_element('//*[@id="didomi-popup"]/div/div')
                    #     self.driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]').click()
                    self.util.scroll_to_element(self.driver,'//*[@id="fiche_entreprise"]/div[4]/div[2]/table[2]')
                    print('vita scroll---------------')
                    html = self.driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find('table', attrs={'class':'table table-default dirigeants'})
                    alltr = table.find_all('tr')
                    dataEnsemble = []
                    print('debut---------------') 
                    for tr in alltr:
                        tdInTr = tr.find_all('td')
                        data = {}
                        for td in tdInTr:
                            isLien = td.find('a')
                            val = td.contents
                            if isLien == None and  td.has_attr('class') == True:
                                data['poste'] = val[0]
                            elif isLien == None and  td.has_attr('class') == False :
                                data['nomPrenom'] = str(val[0]).replace('\t','').replace('\n','').strip()
                            elif isLien:
                                data['nomPrenom'] = str(isLien.getText()).replace('\t','').replace('\n','').strip()
                        dataEnsemble.append(data)
                    row['dirigeants'] = dataEnsemble 
                    print('fin---------------')
                except Exception as e:
                    print(e,"error")
                    next
            result.append(row)
            print(result)
        return result
            




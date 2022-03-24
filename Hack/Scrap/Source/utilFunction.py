import io
import time
import os
import pdfkit
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui

class utilFunctions():
    def __init__(self,driver):
        self.wait = ui.WebDriverWait(driver, timeout=10000)

    def wait_located(self, model, element):
        self.wait.until(EC.presence_of_element_located((getattr(By,model), element)))

    def wait_located_All_xpath(self, xpath):
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def wait_click_xpath(self, xpath):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def wait_visible_element(self, xpath):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        
    def get_el_by_xpath(self,driver,xpath):
        return driver.find_element_by_xpath(xpath)

    def get_el_by_tag_name(driver,tag):
        return driver.find_element_by_tag_name(tag)

    def get_el_by_slector(self,driver,selector):
        return driver.find_elements_by_css_selector(selector)

    def get_el_by_ID(self,driver,id):
        return driver.find_element(By.ID, id)


    def click_element(self,driver, xpath):
        self.get_el_by_xpath(driver,xpath).click()

    def get_element_table(driver,BeautifulSoup,idTable,classHTML):
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        element_table = soup.find(
            'table', attrs={classHTML: idTable})
        return element_table

    def script_link(tag,textContent):
        script = "var listLienPage = document.querySelectorAll('"+tag+"'); listLienPage.forEach(function(element) {if (element.textContent ==='" + \
            textContent+"') {element.click()}})"

        return script

    def script_include(tag,textContent):
        script = "var listLienPage = document.querySelectorAll('"+tag+"'); listLienPage.forEach(function(element) {if (element.textContent.includes('" + \
            textContent+"')) {element.click()}})"
        return script
        
    def script_find_lien(titreMenu,regex):
        script = "var listLienPage = document.querySelectorAll('a'); listLienPage.forEach(function(element) {if (element.textContent.includes('"+ \
            titreMenu+"')) {const regex = "+regex+";var lien = element.href;var found = lien.match(regex);if(found !== null){element.click()}}})"
        return script
        
        
    def find_exist(self,driver,xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def switch_one_tab(self,driver, dejaOpen):
        tabOpen = driver.current_window_handle
        dejaOpen.append(tabOpen)
        All_tab = driver.window_handles
        for tab in All_tab:
            if tab not in dejaOpen:
                driver.switch_to.window(tab)
                break
        return dejaOpen

    def remplire_input_by_id(self,driver,code):
        for input in code:
            print(input,'value')
            self.scroll_to_element(driver,'//*[@id="'+input['id']+'"]')
            inputElement = self.get_el_by_xpath(driver,'//*[@id="'+input['id']+'"]')
            inputElement.send_keys(input['value'])
            time.sleep(0.5)

    def scroll_to_element(self,driver,xpath):
        element = self.get_el_by_xpath(driver,xpath)
        action = ActionChains(driver)
        action.move_to_element(element).perform()
    
    def scroll_to_element_by_selector(driver,selector):
        element = utilFunctions.get_el_by_slector(driver,selector)
        action = ActionChains(driver)
        action.move_to_element(element[0]).perform()

    def imprimerEcran(lienPDFsortie, soup, idToImprimer,cssFileName, autreElement='', autreOption=''):
        options = {'page-size': 'Letter','encoding': "UTF-8"} if autreOption == '' else autreOption
        basedir = os.path.abspath(os.path.dirname(__file__))
        try:
            divImpirmer = soup.find("div", attrs={"id":idToImprimer}) if autreElement == '' else autreElement
            print(lienPDFsortie,'pathSaveFile-----------------------')
            #linux
            pdfkit.from_string(str(divImpirmer),output_path=lienPDFsortie,css=basedir+'/../static/css/'+cssFileName,options=options)
            #windows
            # pdfkit.from_string(str(divImpirmer),output_path=lienPDFsortie,css=basedir+'\\..\\static\\css\\'+cssFileName,options=options)
        except Exception as e:
            print(e)
            pass
        return {'pdfLien': lienPDFsortie}

    def setSelectInput(driver,inpName,value):
        driver.find_element_by_xpath("//select[@name='"+inpName+"']/option[text()='"+value+"']").click()
        
    def scrip_simulation(name):
        script = 'var targetNode = document.querySelector ("'+str(name)+'");'+\
                'if (targetNode) {'+\
                    'triggerMouseEvent (targetNode, "mouseover");'+\
                    'triggerMouseEvent (targetNode, "mousedown");'+\
                    'triggerMouseEvent (targetNode, "mouseup");'+\
                    'triggerMouseEvent (targetNode, "click");'+\
                '}'+\
                'function triggerMouseEvent (node, eventType) {'+\
                    "var clickEvent = document.createEvent ('MouseEvents');"+\
                    'clickEvent.initEvent (eventType, true, true);'+\
                    'node.dispatchEvent (clickEvent);'+\
                '}'

        return script
    
    def xpath_soup(self,element):
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name
                if siblings == [child] else
                '%s[%d]' % (child.name, 1 + siblings.index(child))
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    def saveToFile(self,lienFile,text):
        textDecode = text.encode('ascii',errors='ignore').decode('ascii')
        file = io.open(lienFile,'w', encoding='utf8')
        file.write(textDecode)
        file.close()

    def getStringFile(file):
        file = open(file,'r')
        result = file.read()
        return str(result)

    def scroll_with_limit(self,driver,nbr_boucle,length_page_scroll):
        step = 0
        for i in range(0,nbr_boucle):
            script = 'window.scrollTo(0,'+str(step)+')'
            driver.execute_script(script)
            step += length_page_scroll
            time.sleep(0.2)

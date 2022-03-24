import os,csv
import pandas as pd
class Export():
    def __init__(self):
        self.directory = os.path.dirname(os.path.dirname(__file__))

    #CSV
    def ocsv(self,filename, data):
        res = ''
        # try:
        with open(os.path.abspath(filename), 'a') as csvfile:
            fieldnames = ["Nom", "Prenom", "Poste","Email","Contacte","Société","LinkeDin","Domaine","Status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for d in data:
                element = {
                    "Nom": d['nom'], 
                    "Prenom": d['prenom'],
                    "Poste": d['poste'],
                    "Email": d['email'] if 'email' in data else '',
                    "Status": d['status'] if 'status' in data else '',
                    "Contacte": d['email'] if 'contacte' in data else '',
                    "LinkeDin": d['lienLinkeDin'],
                    "Société": d['Societe'],
                    "Domaine":d['site'] if 'site' in  data else '', 
                    }
                print(element)
                writer.writerows(element)
            res= os.path.abspath(filename)
        # except Exception as e:
        #         print(e)

        return res


    def generateExcel(self,filename,data,typeAction):
        newData = []
        for d in data:
            # print(d['site'] if 'site' in  data else '')
            domaine  = d['site'] if typeAction == "Valider" else ''
            # poste = d['poste'] if typeAction != "Valider" and "poste" in data else ''
            value = {
                "Nom": d['nom'], 
                "Prenom": d['prenom'],
                "Poste": d['poste'],
                "Email": d['email'] if 'email' in data else '',
                "Status": d['status'] if 'status' in data else '',
                "Contacte": d['email'] if 'contacte' in data else '',
                "LinkeDin": d['lienLinkeDin'],
                "Société": d['Societe'],
                "Domaine":domaine, 
            }
            newData.append(value)
        
        frame = pd.DataFrame(newData)
        #local
        lienExcel = os.path.join(self.directory,'TestExport\\'+filename+'.xlsx')
        #prod
        # lienExcel = '/home/SDABOU/SILAE/django_vue/apep/excelGenerate/'+filename+'.xlsx'
        # write =pd.ExcelWriter('excelGenerate/exported_json_data.xlsx', engine='openpyxl')
        write =pd.ExcelWriter(lienExcel, engine='openpyxl')
        frame.to_excel(write, sheet_name='Resultat')
        workbook = write.book
        worksheet = write.sheets['Resultat']
        
        worksheet.column_dimensions['B'].width = 12
        worksheet.column_dimensions['C'].width = 12
        worksheet.column_dimensions['D'].width = 20
        worksheet.column_dimensions['E'].width = 12
        worksheet.column_dimensions['F'].width = 12
        worksheet.column_dimensions['G'].width = 12
        worksheet.column_dimensions['H'].width = 12
        worksheet.column_dimensions['I'].width = 12
        worksheet.column_dimensions['J'].width = 12

        print(type(worksheet))
        write.save()

        return filename
            
        
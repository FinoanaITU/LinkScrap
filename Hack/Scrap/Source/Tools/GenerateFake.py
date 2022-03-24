import re
import secrets
from faker import Faker

class FakeInfo():
    def __init__(self):
        self.nom = ['MARTIN','BERNARD','THOMAS','PETIT','ROBERT','RICHARD','DURAND','DUBOIS','MOREAU','LAURENT','SIMON','MICHEL','LEFEVRE','LEROY','ROUX','DAVID','BERTRAND','MOREL','FOURNIER','GIRARD','FONTAINE','DUPONT','VINCENT','MULLER','BOUTTIER','COLLARD']
        self.prenom = ['Léo','Gabriel','Jade','Louise','Arthur','Louis','Jules','Emma','Adam','Lucas','Hugo','Alice','Rose','Paul','Tom','Marius','Victor','Zoé','Axel','Iris','Julien','Nicolas','Emilie','Julie','Guillaume','Jonathan','Marie']
        self.faker = Faker('fr_FR')
    
    def persoInfo (self,nbrPersonne):
        result = []
        for _ in range(nbrPersonne):
            data = {
                'nom': secrets.choice(self.nom),
                'prenom': secrets.choice(self.prenom),
                'email': '',
                'date_naisssance': self.faker.date_of_birth(minimum_age=20, maximum_age=55),
                'ville': self.faker.city(),
                'code_postal': self.faker.postcode(),
                'address':self.faker.address().replace('\n',' '),
                'poste': self.faker.job()
            }
            result.append(data)
        return result

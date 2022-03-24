import os
from .initialise.chrome import chrome

class connect():
    def __init__(self):
        self.driver = chrome(os.path.abspath(os.path.dirname(__file__))).driver()

    def toVerifCom (self):
        self.driver.get('https://www.verif.com/')

    def salesNavigator(self):
        self.driver.get('https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

    def oliverList(self):
        self.driver.get('https://app.oliverlist.com/login')

    def osv(self):
        self.driver.get('https://secure-auth.team.moovapps.com/osv/auth/login?viewstate=vLCxaFzLJKhQicq-TeFYKthFDrUfdev1JuO3yCeKj8g=.1634893098812.0hgPZoxf_aiBGdiChwHgk7MoOWeU2UgSGXNS2lldzvU=')

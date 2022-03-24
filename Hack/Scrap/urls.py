from django.urls import path
from .Views.verifVue import verifVue
from .Views.linkSalesVue import linkSalesVue
from .Views.oliverListVue import oliverListVue
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    ##verif.com
    path('verifCom/listSociete', verifVue.listSociete, name='liste_societe'),
    path('verifCom/Societe_dirigeant', verifVue.getAllDirigeant, name='liste_societe_with_dirigeant'),

    ##sales navigator
    path('sales/listScoiete', linkSalesVue.listSocieteSales, name='liste_societe'),
    path('sales/enrichir_list', linkSalesVue.enrichirListSociete, name='liste_societe_enrichir'),

    ##oliver list
    path('oliverList/execut_sequence', oliverListVue.executSequence, name='execut_sequence'),

    ##Generate info perso
    path('faker/generate_Info', linkSalesVue.generateInfoPerso, name='generate_acoumpt_info'),

    ###Export to csv
    path('export/excel', linkSalesVue.exportToExcel, name='export_to_excel'),

    ##enrichissement
    path('enrichissement/drop', linkSalesVue.enrichissementDrop, name='enrichissement_dropcontact'),


]
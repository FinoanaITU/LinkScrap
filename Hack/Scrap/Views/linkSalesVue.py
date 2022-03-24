from django.http import JsonResponse
from django.http.response import HttpResponse
from Scrap.Source.sites.linkeDin import linkeDin
from Scrap.Source.Tools.GenerateFake import FakeInfo
from Scrap.Source.Tools.Export import Export
from Scrap.Source.Tools.Dropcontact import Dropcontact
from django.views.decorators.csrf import csrf_exempt
import json

class linkSalesVue():

    @csrf_exempt
    def listSocieteSales(request):
        result = {'wawa': True}
        data = json.loads(request.body)
        ob = linkeDin()
        check = ob.listSocieteProspect(data['url'],data['cathegory'],int(data['pageDebut']),int(data['pageFin']), data['compte'])
        return JsonResponse(check,safe=False)

    @csrf_exempt
    def enrichirListSociete(request):
        data = json.loads(request.body)
        ob = linkeDin()
        list = ob.enrichirList(data)
        return JsonResponse(list,safe=False)

    @csrf_exempt
    def generateInfoPerso(request):
        data = json.loads(request.body)
        ob = FakeInfo()
        list = ob.persoInfo(int(data['nombreCompte']))
        return JsonResponse(list,safe=False)

    @csrf_exempt
    def exportToExcel(request):
        data = json.loads(request.body)
        ob = Export()
        fileName = ob.generateExcel(data['filename'],data['data'],data['typeAction'])
        return HttpResponse(fileName)

    @csrf_exempt
    def enrichissementDrop(request):
        data = json.loads(request.body)
        ob = Dropcontact()
        result = ob.executeRequest(data['data'])
        return JsonResponse(result,safe=False)
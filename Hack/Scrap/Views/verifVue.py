from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Scrap.Source.sites.verifCom import verifCom
import json
class verifVue ():
    
    @csrf_exempt
    def listSociete(request):
        result = {}
        data = json.loads(request.body)
        obVerif = verifCom()
        check = obVerif.recherche(data['motCle'],data['type'])
        if check:
            dataFinal = []
            result = obVerif.findRS(dataFinal,data['type'],int(data['limitPage']))
        return JsonResponse(result,safe=False)
        
    @csrf_exempt
    def getAllDirigeant(request):
        data  = json.loads(request.body)
        obVerif = verifCom()
        res = obVerif.getDirigeant(data)
        print(res)
        return JsonResponse(res,safe=False)
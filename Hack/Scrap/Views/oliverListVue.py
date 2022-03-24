from django.http import JsonResponse
from Scrap.Source.sites.oliverList import oliverList
from django.views.decorators.csrf import csrf_exempt
import json

class oliverListVue():

    @csrf_exempt
    def executSequence(request):
        print(request.body)
        data = json.loads(request.body)
        ob = oliverList()
        check = ob.actionToDo(data['type'],data['date'],data['userName'])
        # check = [{"campagne": "Mmc Jardin","statistique": {"envoi": "8","ouverture": "2","session": "0","reponse": "0","bounce": "0"}}]
        val = json.dumps(check)
        return JsonResponse(val,safe=False)
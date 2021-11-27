from django.shortcuts import render
import pronotepy
from pronotepy.ent import ile_de_france
from django.http.response import HttpResponse

# Create your views here.

class Average():
    def __init__(self, matiere) -> None:
        self.matiere = matiere
        self.coef_de_matiere = 1
        self.nb_de_note = 0
        self.somme_de_note=0
    
    def get(self):
        return self.somme_de_note/self.nb_de_note
    
    def add_note(self, note, coef):
        self.nb_de_note+=coef
        self.somme_de_note+=note*coef
        return self

def index(request):
    print(request.method)
    if request.method == 'GET':
        return render(request, "home/index.html")
    else:
        if True:
            password = request.POST.get("password")
            username = request.POST.get("username")
            client = pronotepy.Client('https://0922397f.index-education.net/pronote/eleve.html',
                                    username=username,
                                    password=password,
                                    ent=ile_de_france)

            a=""

            if client.logged_in:
                a+=(client.periods[0].name+":<br><br>")
                moyennes={}
                
                plus_long=0

                for grade in client.current_period.grades:
                    if grade.period.name == "Trimestre 1":
                        try:
                            note = float(grade.grade.replace(",","."))/float(grade.out_of)*20
                            coef = float(grade.coefficient.replace(",", "."))        
                            if grade.subject.id in moyennes.keys():
                                moyennes.get(grade.subject.id).add_note(note, coef)
                            else:
                                if len(grade.subject.name) > plus_long:
                                    plus_long=len(grade.subject.name)
                                moyennes.update({grade.subject.id:Average(grade.subject.name).add_note(note, coef)})
                        except:
                            pass
                global_average = Average("global")
                for moyenne in moyennes.values():
                    a+=(moyenne.matiere+" : "+" "*(plus_long-len(moyenne.matiere))+" "+str(round(moyenne.get(), 2))+"<br>")
                    global_average.add_note(moyenne.get(), moyenne.coef_de_matiere)
                a+=("<br><br>global : "+" "*(plus_long-6)+" "+str(round(global_average.get(),2))+"<br>")
                
            return HttpResponse(a)
        #except:
        #    return HttpResponse("Mot de passe faux")

def connected():
    pass
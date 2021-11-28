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
            period = int(request.POST.get("period"))
            client = pronotepy.Client('https://0922397f.index-education.net/pronote/eleve.html',
                                    username=username,
                                    password=password,
                                    ent=ile_de_france)

            a=""

            if client.logged_in:
                a+='<table><tr><td><b>Trimestre '+str(period)+'</b></td><td><b>Votre Moyenne</b></td><td><b>Moyenne de la classe</b></td><td><b>Coefficient</b></td></tr>'
                moyennes={}
                moyennes_classe={}
                plus_long=0

                for grade in client.periods[period-1].grades:
                    if grade.period.name == "Trimestre "+str(period):
                        try:
                            note = float(grade.grade.replace(",","."))/float(grade.out_of)*20
                            note_classe = float(grade.average.replace(",","."))/float(grade.out_of)*20
                            coef = float(grade.coefficient.replace(",", "."))
                            if grade.subject.id in moyennes.keys():
                                moyennes.get(grade.subject.id).add_note(note, coef)
                                moyennes_classe.get(grade.subject.id).add_note(note_classe, coef)
                            else:
                                if len(grade.subject.name) > plus_long:
                                    plus_long=len(grade.subject.name)
                                moyennes.update({grade.subject.id:Average(grade.subject.name).add_note(note, coef)})
                                moyennes_classe.update({grade.subject.id:Average(grade.subject.name).add_note(note_classe, coef)})
                        except:
                            pass
                for i in range(len(moyennes.values())):
                    matiere=moyennes.get(list(moyennes.keys())[i]).matiere
                    moyenne=round(moyennes.get(list(moyennes.keys())[i]).get(), 2)
                    moyenne_classe=round(moyennes_classe.get(list(moyennes.keys())[i]).get(), 2)
                    a+=("<tr class='rows-"+str(i)+"'><td>"+matiere+"</td><td class='average'>"+str(moyenne)+"</td><td class='classe-average'>"+str(moyenne_classe)+"</td><td><input class='coef' type='number' min='0' value='1'></td></tr>")
                a+=("<br><tr class='row-global'><td>Générale</td><td class='global-average'></td><td class='global-classe_average'></td></tr></table>") 
                a+='<style>th, td {padding: 15px;text-align: left;} body{background: #67BE4B;} table{width:100%;padding: 40px;border: 1px solid #f1f1f1;background: #fff;box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);}</style>'
                a+='<script> var averages = document.getElementsByClassName("average");var classe_averages = document.getElementsByClassName("classe-average");var coefs = document.getElementsByClassName("coef");var global_average = 0.0;var global_classe_average = 0.0;var number_of_grade= 0;for (let i = 0; i < averages.length; i++) {coef = parseInt(coefs[i].value);global_average += parseFloat(averages[i].textContent)*coef;global_classe_average += parseFloat(classe_averages[i].textContent)*coef;number_of_grade += coef;}console.log(global_average, number_of_grade, typeof(parseFloat(global_average)));document.getElementsByClassName("global-average")[0].textContent = global_average/number_of_grade;document.getElementsByClassName("global-classe_average")[0].textContent = global_classe_average/number_of_grade;</script>'
            return HttpResponse(a)
        #except:
        #    return HttpResponse("Mot de passe faux")

def connected():
    pass
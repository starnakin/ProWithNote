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
        password = request.POST.get("password")
        username = request.POST.get("username")
        client = pronotepy.Client('https://0922397f.index-education.net/pronote/eleve.html',
                        username=username,
                        password=password,
                        ent=ile_de_france)
        if client.logged_in:
            period_type = request.POST.get("period-type")
            period = int(request.POST.get("period"))
            a = """
                <table>
                    <tr>
                        <td>
                            <b>Trimestre """+str(period)+"""</b>
                        </td>
                        <td>
                            <b>Moyenne min</b></td>
                        <td>
                            <b>Votre Moyenne</b>
                        </td>
                        <td>
                            <b>Moyenne de la classe</b>
                        </td>
                        <td>
                            <b>Moyenne max</b>
                        </td>
                        <td>
                            <b>Coefficient</b>
                        </td>
                    </tr>
            """
            moyennes={}
            moyennes_classe={}
            plus_long=0
            for i in client.periods[period-1].averages:
                name = i.subject.name.split("> ")
                if len(name) > 1:
                    name=name[1]
                else:
                    name = name[0]
                a+="""
                    <tr class='rows-"""+name+"""'>
                        <td>"""+name+"""</td>
                        <td class='min-average'>"""+str(i.min)+"""</td>
                        <td class='average'>"""+str(i.student)+"""</td>
                        <td class='classe-average'>"""+str(i.class_average)+"""</td>
                        <td class='max-average'>"""+str(i.max)+"""</td>
                        <td><input id='update' class='coef' type='number' min='0' value='1' onchange='test()'></td>
                    </tr>
                    """
            a+="""
                    <br>
                    <tr class='row-global'><td>Générale</td><td class='global-min-average'></td>
                        <td class='global-average'></td>
                        <td class='global-classe_average'></td>
                        <td class='global-max-average'></td>
                    </tr>
                </table>
                """ 
            a+="""
                <style>
                    th, td {
                        padding: 15px;text-align: left;
                    } 
                    body{
                        background: #67BE4B;
                    } 
                    table{
                        width:100%;
                        padding: 40px;
                        border: 1px solid #f1f1f1;
                        background: #fff;
                        box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
                    }
                </style>
                """
            a+="""
                <script>
                    function test(){
                        var averages = document.getElementsByClassName("average");
                        var classe_averages = document.getElementsByClassName("classe-average");
                        var min_averages = document.getElementsByClassName("min-average");
                        var max_averages = document.getElementsByClassName("max-average");
                        var coefs = document.getElementsByClassName("coef");

                        var min_average = 0.0;
                        var global_average = 0.0;
                        var max_average = 0.0;
                        var classe_average = 0.0;
                        var number_of_grade= 0;

                        for (let i = 0; i < averages.length; i++) {

                            coef = parseInt(coefs[i].value);

                            global_average += parseFloat(averages[i].textContent)*coef;
                            classe_average += parseFloat(classe_averages[i].textContent)*coef;
                            min_average += parseFloat(min_averages[i].textContent)*coef;
                            max_average += parseFloat(max_averages[i].textContent)*coef;
                            number_of_grade += coef;

                        }

                        document.getElementsByClassName("global-average")[0].textContent = (global_average/number_of_grade).toPrecision(3);
                        document.getElementsByClassName("global-min-average")[0].textContent = (min_average/number_of_grade).toPrecision(3);
                        document.getElementsByClassName("global-max-average")[0].textContent = (max_average/number_of_grade).toPrecision(3);
                        document.getElementsByClassName("global-classe_average")[0].textContent = (classe_average/number_of_grade).toPrecision(3);
                    }
                    test();
                    $('#update').keyup(function(e){
                        test();
                    });
                </script>
            """
            return HttpResponse(a)
        else:
            return HttpResponse("Mot de passe faux")

def connected():
    pass
from gestione.models import Car

def erase_db():
    print("Cancello il DB...")
    Car.objects.all().delete()

def init_db():
    
    if len(Car.objects.all()) != 0:
        return

    cardict = {
        "model" : ["Ford", "Model2", "Model3", "Model4", "Model5"],
        "license_plate" : ["AB123CD", "EF456GH", "IJ789KL", "MN012OP", "QR345ST"],
        "km" : [200000 , 150000, 43414, 1012, 4000000],
    }

    for i in range(5):
        c = Car()
        for k in cardict:
            if k == "model":
                    c.autore = cardict[k][i]
            if k == "license_plate":
                    c.titolo = cardict[k][i]
            if k == "km":
                    c.pagine = cardict[k][i] 
        c.save()
    
    print("DUMP DB")
    print(Car.objects.all()) 
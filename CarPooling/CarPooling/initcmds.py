from gestione.models import Car
from django.utils import timezone
from datetime import datetime,timedelta

def erase_db():
    print("\nDeleting DB 🗑️ \n")
    Car.objects.all().delete()

def func_time(off_year=None, off_month=None, off_day=None):
        if off_year == 0 and off_month==0 and off_day==0:
            return None
        tz = timezone.now()
        out = datetime(tz.year-off_year,tz.month-off_month,
                    tz.day-off_day,tz.hour,tz.minute, tz.second)
        return out 


def init_db():

    if len(Car.objects.all()) != 0:
        return

    cardict = {
        "model" : ["Ford", "Model2", "Model3", "Model4", "Model5"],
        "license_plate" : ["AB123CD", "EF456GH", "IJ789KL", "MN012OP", "QR345ST"],
        "km" : [200000 , 150000, 43414, 1012, 4000000],
        "last_inspection_date" : [[ func_time(y,m,d) for y in range(2) for m in range(2) for d in range(2) ]]
    }

    for i in range(5):
        c = Car()
        for k in cardict:
            if k == "model":
                    c.model = cardict[k][i]
            if k == "license_plate":
                    c.license_plate = cardict[k][i]
            if k == "km":
                    c.km = cardict[k][i]
            if k == "last_inspection_date":
                    c.last_inspection_date = datetime.now()
        c.save()

        
    
    print("DUMP DB")
    print(Car.objects.all()) 
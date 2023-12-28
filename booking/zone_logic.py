from user_master.models import *



def zone_get(zone_data):
    if (ZoneA.objects.filter(location=zone_data).first()):
        return "ZoneA"
    elif(ZoneB.objects.filter(location=zone_data).first()):
        return "ZoneB"
    elif(ZoneC.objects.filter(location=zone_data).first()):
        return "ZoneC"
        

def return_charges(pickup_zone, drop_zone):
    if (pickup_zone == drop_zone):
        return 0
    elif (pickup_zone=="ZoneA" and drop_zone=="ZoneB"):
        return 100
    elif (pickup_zone=="ZoneA" and drop_zone=="ZoneC"):
        return 0
    elif (pickup_zone=="ZoneB" and drop_zone=="ZoneA"):
        return 100
    elif (pickup_zone=="ZoneB" and drop_zone=="ZoneC"):
        return 0
    elif (pickup_zone=="ZoneC" and drop_zone=="ZoneA"):
        return 0
    elif (pickup_zone=="ZoneC" and drop_zone=="ZoneB"):
        return 0
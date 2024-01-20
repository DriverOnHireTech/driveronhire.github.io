from user_master.models import *



def zone_get(zone_data):
    if (ZoneA.objects.filter(location=zone_data).first()):
        return "ZoneA"
    elif(ZoneB.objects.filter(location=zone_data).first()):
        return "ZoneB"
    elif(ZoneC.objects.filter(location=zone_data).first()):
        return "ZoneC"
    elif(ZoneD.objects.filter(location=zone_data).first()):
        return "ZoneD"
    elif(ZoneE.objects.filter(location=zone_data).first()):
        return "ZoneE"
    elif(ZoneF.objects.filter(location=zone_data).first()):
        return "ZoneF"
    elif(ZoneG.objects.filter(location=zone_data).first()):
        return "ZoneG"
    
    #Pune location zone get
    elif pune_A_location.objects.filter(location=zone_data).first():
        return "pune_A_location"
    elif pune_B_location.objects.filter(location=zone_data).first():
        return "pune_B_location"
    

def return_charges(pickup_zone, drop_zone):
    if (pickup_zone == drop_zone):
        return None
    elif (pickup_zone=="ZoneA" and (drop_zone=="ZoneB" or drop_zone=="ZoneD" or drop_zone=="ZoneF")):
        return None
    elif (pickup_zone=="ZoneA" and (drop_zone=="ZoneC" or drop_zone=="ZoneE" or drop_zone=="ZoneG")):
        return 200
    elif (pickup_zone=="ZoneB" and (drop_zone=="ZoneA" or drop_zone=="ZoneC" or drop_zone=="ZoneD" or drop_zone=="ZoneF")):
        return None
    elif (pickup_zone=="ZoneB" and (drop_zone=="ZoneE" or drop_zone=="ZoneG")):
        return 200
    elif (pickup_zone=="ZoneC" and drop_zone=="ZoneB"):
        return None
    elif (pickup_zone=="ZoneC" and drop_zone=="ZoneA" or drop_zone=="ZoneD" or drop_zone=="ZoneE" or drop_zone=="ZoneF" or drop_zone=="ZoneG"):
        return 200
    elif (pickup_zone=="ZoneD" and (drop_zone=="ZoneA" or drop_zone=="ZoneB" or drop_zone=="ZoneE" or drop_zone=="ZoneF")):
        return None
    elif (pickup_zone=="ZoneD" and (drop_zone=="ZoneC" or drop_zone=="ZoneG")):
        return 200
    elif (pickup_zone=="ZoneE" and drop_zone=="ZoneD"):
        return None
    elif (pickup_zone=="ZoneE" and drop_zone=="ZoneA" or drop_zone=="ZoneB" or drop_zone=="ZoneC" or drop_zone=="ZoneF" or drop_zone=="ZoneG"):
        return 200
    elif (pickup_zone=="ZoneF" and (drop_zone=="ZoneA" or drop_zone=="ZoneB" or drop_zone=="ZoneD" or drop_zone=="ZoneG")):
        return None
    elif (pickup_zone=="ZoneF" and (drop_zone=="ZoneC" or drop_zone=="ZoneE")):
        return 200
    elif (pickup_zone=="ZoneG" and drop_zone=="ZoneF"):
        return None
    elif (pickup_zone=="ZoneG" and drop_zone=="ZoneA" or drop_zone=="ZoneB" or drop_zone=="ZoneC" or drop_zone=="ZoneD" or drop_zone=="ZoneE"):
        return 200
    #Pune location rate check
    elif (pickup_zone=="pune_A_location" and drop_zone=="pune_B_location") or (pickup_zone== "pune_B_location" and drop_zone=="pune_A_location"):
        return 200
    elif (pickup_zone=="pune_A_location" and drop_zone=="pune_A_location") or (pickup_zone== "pune_B_location" and drop_zone=="pune_B_location"):
        return None
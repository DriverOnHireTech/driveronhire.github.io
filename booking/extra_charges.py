from .models import ZoneA, ZoneB, ZoneC

class ExtraRate:
    def __init__(self,pickuplocation, droplocation):
        self.pickuplocation=pickuplocation
        self.drop_location_change=droplocation

    def extrarate(pickuplocation, droplocation):
        zonea=ZoneA.objects.get(pickuplocation=pickuplocation)
        zoneb=ZoneB.objects.get(droplocation=droplocation)

        if zonea in pickuplocation:
           pass 
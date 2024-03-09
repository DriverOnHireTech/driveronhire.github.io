def get_base_charge(cartype, packege):
    if "Luxury" in cartype:
        if "2" in packege:
            return "500"
        elif "4" in packege:
            return "600"
        elif "8" in packege:
            return "900"
    else:
        if "2" in packege:
            return "400"
        elif "4" in packege:
            return "500"
        elif "8" in packege:
            return "800"
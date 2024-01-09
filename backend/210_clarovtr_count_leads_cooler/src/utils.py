def element_to_json(data):
    return [
        {
            "total_leads": element[0],
            "en_nomolestar": element[1],
            "leads_en_cooler": element[2],
            "leads_liberados": element[3],
            "total_gestiones": element[4],
        }
        for element in data
    ]
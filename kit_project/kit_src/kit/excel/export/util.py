def get_district(location):
    try:
        return location.name if location.type.name == 'district' else location.get_ancestors().get(type__name='district').name
    except:
        return None

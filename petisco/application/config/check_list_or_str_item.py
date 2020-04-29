def check_list_or_str_item(kdict, key, required=False, suffix="", typename="Element"):
    kvalue = kdict.get(key)
    if not kvalue and required:
        raise TypeError(f"{typename} must contains {key}{suffix} variable")

    if isinstance(kvalue, str):
        value = [kvalue]
    elif isinstance(kvalue, list):
        value = kvalue
    else:
        if required:
            raise TypeError(
                f"{typename} must contains {key}{suffix} variable (Only list and str is supported)"
            )
        else:
            value = None
    return value

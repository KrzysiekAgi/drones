def where_to_move(requested, actual):
    regular = requested - actual

    if regular > 180:
        regular = regular - 360

    if regular < -180:
        regular =  regular + 360

    return regular

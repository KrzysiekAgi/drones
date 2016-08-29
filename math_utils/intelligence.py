def where_to_move_relative(requested, actual):
    regular = requested - actual

    if regular > 180:
        regular = regular - 360

    if regular < -180:
        regular =  regular + 360

    return regular


def where_to_move_absolute(requested, actual):
    no_minus = actual % 360
    regular = requested - no_minus
    print requested
    print actual
    print regular
    if regular > 180:
        regular = regular - 360

    if regular < -180:
        regular =  regular + 360

    return actual + regular
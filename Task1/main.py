compass = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
constant = 45


def direction(facing, turn):
    if turn > 1080 or turn < -1080:
        return None
    else:
        multipliers = turn // constant
        start_position = compass.index(facing)
        end_position = (start_position + multipliers) % len(compass)
        return compass[end_position]

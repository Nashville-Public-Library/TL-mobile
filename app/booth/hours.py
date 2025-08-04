from datetime import datetime

def hour1() -> str:
    current_hour = datetime.now().strftime('%H')

    if int(current_hour) <= 11:
        # booth schedule begins at 9am, but we want to start showing the schedule at 8am
        if int(current_hour) == 8:
            lead_hour = '9:00am - '
        else:
            lead_hour = f'{current_hour}:00am - '.lstrip('0')
    elif int(current_hour) == 12:
        lead_hour = '12:00pm - '
    else:
        lead_hour = int(current_hour) - 12
        lead_hour = f'{lead_hour}:00pm - '.lstrip('0')

    if int(current_hour) == 12:
        trail_hour = int(current_hour) - 11
        trail_hour = f'{trail_hour}:00pm'
    elif int(current_hour) < 11:
        if int(current_hour) == 8:
            trail_hour = '10:00am'
        else:
            trail_hour = int(current_hour) + 1
            trail_hour = f'{trail_hour}:00am'.lstrip('0')
    elif int(current_hour) == 11:
        trail_hour = '12:00pm'
    else:
        trail_hour = int(current_hour) - 11
        trail_hour = f'{trail_hour}:00pm'.lstrip('0')

    #3-4:30pm is a special case. deal with this separately.
    if int(current_hour) == 15 or int(current_hour) == 16:
        lead_hour = '3:00pm - '
        trail_hour = '4:30pm'

    final_hour = f'{lead_hour}{trail_hour}'
    return final_hour

def hour2() -> str:
    current_hour = datetime.now().strftime('%H')
    current_hour = int(current_hour) + 1

    if current_hour <= 11:
        # booth schedule begins at 9am, but we want to start showing the schedule at 8am
        if current_hour == 9:
            lead_hour = '10:00am - '
        else:
            lead_hour = f'{current_hour}:00am - '.lstrip('0')
    elif current_hour == 12:
        lead_hour = '12:00pm - '
    else:
        lead_hour = (current_hour) - 12
        lead_hour = f'{lead_hour}:00pm - '.lstrip('0')

    if current_hour == 13:
        trail_hour = (current_hour) - 11
        trail_hour = f'{trail_hour}:00pm'.lstrip('0')
    elif current_hour < 11:
        if current_hour == 9:
            trail_hour = '11:00am'
        else:
            trail_hour = (current_hour) + 1
            trail_hour = f'{trail_hour}:00am'.lstrip('0')
    elif (current_hour) == 11:
        trail_hour = '12:00pm'
    else:
        trail_hour = (current_hour) - 11
        trail_hour = f'{trail_hour}:00pm'.lstrip('0')

    #3-4:30pm is a special case. deal with this separately.
    if current_hour == 15:
        lead_hour = '3:00pm - '
        trail_hour = '4:30pm'
    
    if current_hour >= 16:
        lead_hour = 'Rest of Day'
        trail_hour = ''

    final_hour = f'{lead_hour}{trail_hour}'
    return final_hour
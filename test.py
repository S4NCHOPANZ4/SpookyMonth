from datetime import datetime


def is_it_spookymonth():
    spookyMonth = datetime(datetime.now().year, 10, 1)
    now = datetime.now()
    if now.month == spookyMonth.month:
        return(True, 0)
    if now > spookyMonth:
        spookyMonth = datetime(datetime.now().year + 1, 9, 1)    
    time_left = spookyMonth - now
    days_left = time_left.days
    return (False, days_left)


print(is_it_spookymonth()[0])






from __future__ import division
import datetime


def today():
    return datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d")


def now():
    return datetime.datetime.now()


def format_time_h(tm_str):
    return datetime.datetime.strftime(datetime.datetime.strptime(tm_str, "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d-%H")


def get_date_from_hour(hour):
    return datetime.datetime.strftime(datetime.datetime.strptime(hour, "%Y-%m-%d-%H"), "%Y-%m-%d")


def now_hour():
    return datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H")


def now_h():
    return datetime.datetime.strftime(datetime.datetime.now(), "%H")


def now_str():
    return datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")


def timeobj2str(obj):
    return datetime.datetime.strftime(obj, "%Y-%m-%d %H:%M:%S")


def day2time(day):
    dayobj = datetime.datetime.strptime(day, "%Y-%m-%d")
    return dayobj.strftime("%Y-%m-%d %H:%M:%S")


def time2day(day):
    dayobj = datetime.datetime.strptime(day, "%Y-%m-%d %H:%M:%S")
    return dayobj.strftime("%Y-%m-%d")


def today_break():
    return datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")


def add_day(day, n):
    return datetime.datetime.strftime(datetime.datetime.strptime(day, "%Y-%m-%d") + datetime.timedelta(n), "%Y-%m-%d")


def get_days(start, end):
    d1 = datetime.datetime.strptime(start, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(end, " %Y-%m-%d")
    return (d2 - d1).days


def get_day(day):
    tmptime = datetime.datetime.strptime(day, "%Y-%m-%d")
    return int(datetime.datetime.strftime(tmptime, "%j"))


def adddaybreak(day, n):
    return datetime.datetime.strftime(datetime.datetime.strptime(day, "%Y-%m-%d") + datetime.timedelta(n),
                                      "%Y-%m-%d %H:%M:%S")


def addhour(time, n):
    return datetime.datetime.strftime(
        datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=n), "%Y-%m-%d %H:%M:%S")

def addhour2(time, n):
    return datetime.datetime.strftime(
        datetime.datetime.strptime(time, "%Y-%m-%d-%H") + datetime.timedelta(hours=n), "%Y-%m-%d-%H")


def gethours(time1, time2):
    time1 = datetime.datetime.strptime(time1, "%Y-%m-%d-%H")
    time2 = datetime.datetime.strptime(time2, "%Y-%m-%d-%H")
    delta = time2 - time1
    return int(delta.days*24 + int(delta.seconds)/3600)


def comparedate(date1, date2):
    t2 = date2
    t1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
    return t1 > t2


def comparetime(time1, time2):
    t1 = time1
    t2 = datetime.datetime.strptime(time2, "%Y-%m-%d")
    return t1 > t2


def curmonth():
    return datetime.datetime.strftime(datetime.datetime.strptime(today(), '%Y-%m-%d'), "%Y-%m")


def addmonth(month_str, n):
    dayobj = datetime.datetime.strptime(month_str, "%Y-%m")
    year = dayobj.year
    month = dayobj.month + n
    if month < 1:
        year_inc = int(month / 12) - 1
    elif month > 12:
        year_inc = int((month - 1) / 12)
    year += year_inc
    month -= year_inc * 12
    return '%04d-%02d' % (year, month)


def month2time(month):
    return datetime.datetime.strftime(datetime.datetime.strptime(month, "%Y-%m"), '%Y-%m-%d %H:%M:%S')


def month2timeobj(month):
    return datetime.datetime.strptime(month, "%Y-%m")


def monthcompare(month1, month2):
    m1 = month2timeobj(month1)
    m2 = month2timeobj(month2)
    return m1 <= m2


def getmonths(start, end):
    m1 = datetime.datetime.strptime(start, "%Y-%m")
    m2 = datetime.datetime.strptime(end, "%Y-%m")
    return (m2.year - m1.year) * 12 + (m2.month - m1.month)


def str2timeobj(timestring):
    return datetime.datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")


def weekofyear(date=None):
    if not date:
        date = today()
    tmptime = datetime.datetime.strptime(date, "%Y-%m-%d")
    return int(datetime.datetime.strftime(tmptime, "%W"))


def getyear(date=None):
    if not date:
        date = today()
    tmptime = datetime.datetime.strptime(date, "%Y-%m-%d")
    return int(datetime.datetime.strftime(tmptime, "%Y"))


def monthofyear(date=None):
    if not date:
        date = today()
    tmptime = datetime.datetime.strptime(date, "%Y-%m-%d")
    return int(datetime.datetime.strftime(tmptime, "%m"))


def yearweekinfo(year, weeknum):
    firstdayofyear = datetime.date(year, 1, 1)
    tmpday = firstdayofyear + datetime.timedelta(weeknum * 7)
    dayofweek = tmpday.strftime("%w")
    firstdayofweek = tmpday - datetime.timedelta(int(dayofweek) - 1)
    nextweekday = firstdayofweek + datetime.timedelta(7)
    return firstdayofweek.strftime("%Y-%m-%d"), nextweekday.strftime("%Y-%m-%d")


def yearmonthinfo(year, month):
    startdate = "%4d-%02d-01" % (year, month)
    # enddate = "%4d-%02d-01"%(year, month + 1)
    enddate = addmonth("%4d-%02d" % (year, month), 1) + "-01"
    return startdate, enddate


def getyearofmaxweek(year=None):
    if not year:
        year = getyear()
    lastday = "%4d-12-31" % year
    tmptime = datetime.datetime.strptime(lastday, "%Y-%m-%d")
    return int(datetime.datetime.strftime(tmptime, "%W"))

# coding=utf-8
'''
Created on 10.01.2014

@author: Poschi
'''

import os, pytz, uuid
import datetime
from icalendar import Calendar, Event, vText

filesToDo = []
for dirname, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith(".year"):
            filesToDo.append(filename)


print filesToDo

#Werte aus Datei laden:
dates = [[] for x in xrange(10)]
for file in filesToDo:
    year = int(file[:-5])
    print year
    lines = open(file, "rU")

    route = 0
    month = 0

    # Für jede Zeile in der Datei
    for days in lines:
        for day in days.split("/"): # Eine Zeile enthält 1 bis 4 Termine
            realDay = int(day.strip()[:-1])
            realMonth = int(month + 1)
            #print str(year) + "-" + str(realMonth) + "-" + str(realDay) + " Route " + str(route)
            datum = datetime.date(int(year), realMonth, realDay)
            datum = datetime.datetime(year=int(year), month=realMonth, day=realDay, tzinfo=pytz.timezone("Europe/Berlin"))
            dates[route].append(datum)

        month += 1
        if month >= 12:
            route += 1
            month = 0

# Pro Route ausgeben:
routeNum = 1
for route in dates:
    cal = Calendar()
    cal.add("prodid", "python")
    cal.add("version", "2.0")
    cal["X-WR-CALNAME"] = "Gelber Sack Nürnberg Route " + str(routeNum)
    cal["X-WR-CALDESC"] = "Abfuhrplan für den gelben Sack in Nürnberg von 2017 bis 2019 für die Route " + str(routeNum)
    
    for date in route:
        #nextDay = date + datetime.timedelta(days=1)
        start = datetime.datetime.combine(date, datetime.time(4, 0))
        end = datetime.datetime.combine(date, datetime.time(10, 0))

        event = Event()
        event.add("summary", "Gelber Sack")
        event.add("dtstart", start)
        event.add("dtend", end)
        event.add("dtstamp", date)
        
        event['uid'] = uuid.uuid4()
        event['location'] = vText("Route " + str(routeNum))
        event['description'] = vText("Route " + str(routeNum))
        
        cal.add_component(event)
        
    f = open("route" + str(routeNum) + ".ics", "wb")
    f.write(cal.to_ical())
    f.close()
    routeNum += 1

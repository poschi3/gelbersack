# coding=utf-8
'''
Created on 10.01.2014

@author: Poschi
'''

import os, pytz, uuid
import datetime
from icalendar import Calendar, Event, vText

# Parameter parsen:

filesToDo = []

for dirname, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith(".year"):
            filesToDo.append(filename)


print filesToDo

#Werte aus Datei laden:


dates = [[] for x in xrange(10)] 


# Datei Auslesen
for file in filesToDo:
    year = int(file[:-5])
    print year
    lines = open(file, "rU")
    players = []
    
    route = 0
    month = 0

    # F�r jede Zeile in der Datei
    for days in lines:
        for day in days.split("/"): # Eine Zeile enth�lt 1 bis 4 Termine
            realDay = int(day.strip()[:-1])
            realMonth = int(month + 1)
            datum = datetime.date(int(year), realMonth, realDay)
            datum = datetime.datetime(year=int(year), month=realMonth, day=realDay, tzinfo=pytz.timezone("Europe/Berlin"))
            dates[route].append(datum)

        route += 1
        if route >= 10:
            month += 1
            route = 0

# Pro Route ausgeben:

routeNum = 1
for route in dates:
    
    cal = Calendar()
    cal.add("prodid", "python")
    cal.add("version", "2.0")
    cal["X-WR-CALNAME"] = "Gelber Sack Nuernberg Route " + str(routeNum)
    cal["X-WR-CALDESC"] = "Abfuhrplan fuer den gelben Sack in Nuernberg von 2014 bis 2016 fuer die Route " + str(routeNum)
    
    for date in route:
        nextDay = date + datetime.timedelta(days=1)
        event = Event()
        event.add("summary", "Gelber Sack")
        event.add("dtstart", date)
        event.add("dtend", nextDay)
        event.add("dtstamp", date)
        
        #event['uid'] = uuid.uuid4()
        event['location'] = vText("Route " + str(routeNum))
        event['description'] = vText("Route " + str(routeNum))
        
        cal.add_component(event)
        
    #directory = tempfile.mkdtemp()
    #print directory
    
    f = open("route" + str(routeNum) + ".ics", "wb")
    f.write(cal.to_ical())
    f.close()
#     
    routeNum += 1
    
    
        






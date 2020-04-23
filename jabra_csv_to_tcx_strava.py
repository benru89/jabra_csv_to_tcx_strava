from jabra_parser import Parser
from datetime import datetime
from dateutil import tz
import datetime

# List of available timezones here:
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# ex. for US Pacific Time:
# from_timezone = tz.gettz('America/Los_Angeles')
from_timezone = tz.gettz('UTC')
to_timezone = tz.gettz('UTC')

"""Define the structure of a valid TCX file. Another parsers aside 
from the Jabra parser along with a new method for converting
the trackpoints could be used to extend the functionality to other types of input files"""
def define_tcx(sport, id, start_time, total_time, distance_meters, avg_speed, calories, av_hr, max_hr, trackpoints):
    
    tcx = """<?xml version="1.0" encoding="UTF-8"?> \
<TrainingCenterDatabase xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 \
http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd" xmlns:ns5="http://www.garmin.com/xmlschemas/ActivityGoals/v1" \
xmlns:ns3="http://www.garmin.com/xmlschemas/ActivityExtension/v2" xmlns:ns2="http://www.garmin.com/xmlschemas/UserProfile/v2" \
xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">"""

    tcx += "<Activities>"
    tcx += '<Activity Sport="' + sport + '">'
    tcx += '<Id>' + start_time + '</Id>'
    tcx += '<Lap StartTime="' + start_time + '">'
    tcx += '<TotalTimeSeconds>'+total_time+'</TotalTimeSeconds>'
    tcx += '<DistanceMeters>'+str(distance_meters)+'</DistanceMeters>'
    tcx += '<AverageSpeed>'+str(avg_speed)+'</AverageSpeed>'
    tcx += '<Calories>'+calories+'</Calories>'
    tcx += '<AverageHeartRateBpm>'
    tcx += '<Value>'+av_hr+'</Value>'
    tcx += '</AverageHeartRateBpm>'
    tcx += '<MaximumHeartRateBpm>'
    tcx += '<Value>'+max_hr+'</Value>'
    tcx += '</MaximumHeartRateBpm>'
    tcx += '<Intensity>Active</Intensity>'
    tcx += '<TriggerMethod>Location</TriggerMethod>'
    tcx += '<Track>'
    
    for trackpoint in trackpoints:
        tcx += jabra_trackpoint(trackpoint)

    tcx += "</Track></Lap></Activity></Activities></TrainingCenterDatabase>"
    return tcx


def km_to_m(value):
    return float(value)*1000


def mph_to_kmh(value):
    return float(value)*1.60934


def mi_to_m(value):
    return float(value) * 1609.34


def feet_to_meter(value):
    return float(value) * 0.3048


def jabra_tag(key, dict, tag_name, conversion=None):

    if key not in dict:
        return ''

    value = dict[key]

    if value == '':
        value = 0

    if callable(conversion):
        value = conversion(value)

    return '<' + tag_name + '>' + str(value) + '</' + tag_name + '>'


def jabra_trackpoint(trackpoint):

    tp = "<Trackpoint>"
    tp_time = datetime.datetime.strptime(trackpoint["Date"]+trackpoint["Time"], '%d.%m.%Y%H:%M:%S.%f')
    tp_time = tp_time.replace(tzinfo=from_timezone)
    tp_time = tp_time.astimezone(to_timezone)

    tp_time = tp_time.strftime('%Y-%m-%dT%TZ')
    tp += "<Time>"+tp_time+"</Time>"
    tp += "<Position>"
    tp +=  '<LatitudeDegrees>'+trackpoint["Latitude"]+'</LatitudeDegrees>'
    tp +=  '<LongitudeDegrees>'+trackpoint["Longitude"]+'</LongitudeDegrees>'
    tp += '</Position>'

    tp += jabra_tag('Altitude (m)', trackpoint, 'AltitudeMeters')
    tp += jabra_tag('Altitude (feet)', trackpoint, 'AltitudeMeters', feet_to_meter)

    tp += jabra_tag('Total distance (km)', trackpoint, 'DistanceMeters', km_to_m)
    tp += jabra_tag('Total distance (miles)', trackpoint, 'DistanceMeters', mi_to_m)

    tp += '<HeartRateBpm>'
    tp += '<Value>'+trackpoint["Heart rate (bpm)"]+'</Value>'
    tp += '</HeartRateBpm>'
    tp += '<Extensions>'
    tp += '<TPX xmlns="http://www.garmin.com/xmlschemas/ActivityExtension/v2">'

    tp += jabra_tag('Speed (km/h)', trackpoint, 'Speed', None)
    tp += jabra_tag('Speed (mph)', trackpoint, 'Speed', mph_to_kmh)

    tp += '</TPX>'
    tp += '</Extensions>'
    tp += '</Trackpoint>'
    return tp

def jabra_converter(summary, trackpoint_data):
    sport = summary["Activity type"]
    date = datetime.datetime.strptime(summary["Date"]+summary["Time"], '%d.%m.%Y%H:%M:%S.%f')
    date = date.strftime('%Y-%m-%dT%TZ')
    id = summary["Date"]+'T'+summary["Time"]+'Z'
    start_time =  date
    total_time = summary["Duration (seconds)"]

    distance_kilometers = summary.get("Distance (km)", None)
    if distance_kilometers is not None:
        distance_meters = float(km_to_m(distance_kilometers))

    distance_miles = summary.get("Distance (miles)", None)
    if distance_miles is not None:
        distance_meters = float(mi_to_m(distance_miles))

    avg_speed_kilometers = summary.get("Average speed (km/h)", None)
    if avg_speed_kilometers is not None:
        avg_speed = float(km_to_m(distance_kilometers))

    avg_speed_mph = summary.get("Average speed (mph)", None)
    if avg_speed_mph is not None:
        avg_speed = float(mph_to_kmh(avg_speed_mph))

    calories = summary["Calories (kcal)"]
    av_hr = summary["Average heart rate (bpm)"]
    max_hr = summary["Maximum heart rate (bpm)"]
    return define_tcx(sport,id,start_time,total_time,distance_meters,avg_speed,calories,av_hr,max_hr,trackpoint_data)


def main():
    
    summary_filename = "workout_summaries.csv"
    filename = "workout_updates.csv"

    p = Parser(summary_filename,filename)
    summary, trackpoint_data = p.get_data()

    tcx_file = jabra_converter(summary, trackpoint_data)
    text_file = open("out_workout.tcx", "w")
    text_file.write(tcx_file)
    text_file.close()
    

if __name__== "__main__":
    main()
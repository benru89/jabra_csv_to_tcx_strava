from jabra_parser import Parser
import datetime

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
    tcx += '<AverageSpeed>'+avg_speed+'</AverageSpeed>'
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


def jabra_trackpoint(trackpoint):
    tp = "<Trackpoint>"
    tp_time = datetime.datetime.strptime(trackpoint["Date"]+trackpoint["Time"], '%d.%m.%Y%H:%M:%S.%f')
    tp_time = tp_time.strftime('%Y-%m-%dT%TZ')
    tp += "<Time>"+tp_time+"</Time>"
    tp += "<Position>"
    tp +=  '<LatitudeDegrees>'+trackpoint["Latitude"]+'</LatitudeDegrees>'
    tp +=  '<LongitudeDegrees>'+trackpoint["Longitude"]+'</LongitudeDegrees>'
    tp += '</Position>'
    tp += '<AltitudeMeters>'+trackpoint["Altitude (m)"]+'</AltitudeMeters>'
    total_distance = trackpoint["Total distance (km)"] if trackpoint["Total distance (km)"] != '' else 0
    tp += '<DistanceMeters>'+str(float(total_distance)*1000)+'</DistanceMeters>'
    tp += '<HeartRateBpm>'
    tp += '<Value>'+trackpoint["Heart rate (bpm)"]+'</Value>'
    tp += '</HeartRateBpm>'
    tp += '<Extensions>'
    tp += '<TPX xmlns="http://www.garmin.com/xmlschemas/ActivityExtension/v2">'
    speed = trackpoint["Speed (km/h)"] if trackpoint["Speed (km/h)"] != '' else 0
    tp += '<Speed>'+speed+'</Speed>'
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
    distance_meters = float(summary["Distance (km)"])*1000
    avg_speed = summary["Average speed (km/h)"]
    calories = summary["Calories (kcal)"]
    av_hr = summary["Average heart rate (bpm)"]
    max_hr = summary["Maximum heart rate (bpm)"]
    return define_tcx(sport,id,start_time,total_time,distance_meters,avg_speed,calories,av_hr,max_hr,trackpoint_data)


def main():
    
    summary_filename = "C:/Users/r.fernandez/Downloads/workout_summaries.csv"
    filename = "C:/Users/r.fernandez/Downloads/workout_updates.csv"

    p = Parser(summary_filename,filename)
    summary, trackpoint_data = p.get_data()

    tcx_file = jabra_converter(summary, trackpoint_data)
    text_file = open("out_workout.tcx", "w")
    text_file.write(tcx_file)
    text_file.close()
    

if __name__== "__main__":
    main()
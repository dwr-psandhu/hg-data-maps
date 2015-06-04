# Build a station map to use in a browser from WDL station metadata
import csv
import sys
def csv2geojson(filename):
    stations={}
    result_field_name='Result'
    time_field_name='Collected'
    print 'Processing file %s'%filename
    with open(filename, 'rb') as csvfile:
        csvr = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in csvr:
            try:
                stationNumber = row['Station Number']
                lat = float(row['QST_LATITUDE_DEGREE'])+float(row['QST_LATITUDE_MINUTE'])/60.+float(row['QST_LATITUDE_SECOND'])/3600.
                lon = float(row['QST_LONGITUDE_DEGREE'])+float(row['QST_LONGITUDE_MINUTE'])/60.+float(row['QST_LONGITUDE_SECOND'])/3600.
                lon = -lon # Note the longitude in California is -ve but the data doesn't store it that way !
                #some files call Result as Field Result
                if not row.has_key('Result'):
                    result_field_name='Field Result'
                    time_field_name='Field Result Time'
                if stations.has_key(stationNumber):
                    stations[stationNumber]['Data'].append((row[time_field_name],row[result_field_name]))
                    continue
                else:
                    stations[stationNumber] = {'Full Station Name': row['Full Station Name'],
                                               'Run Name': row['Run Name'], 
                                               'RUN_SUBMITTED_BY': row['RUN_SUBMITTED_BY'],
                                               'Analyte_Fraction_Units': row['Analyte_Fraction_Units'],
                                               'Data': [(row[time_field_name],row[result_field_name])],
                                               'Lon': lon,
                                               'Lat': lat
                    }
            except:
                #print row
                #print sys.exc_info()[0]
                pass
    csvfile.close()
    #
    geojsonfile = open(filename+"_station_map.geojson",'wb')
    geojsonfile.write("""{
  "type": "FeatureCollection",
  "features": [\n""")
    first=True
    for stationNumber in stations.keys():
        stationEntry = stations[stationNumber]
        if not first: 
            geojsonfile.write(",\n")
        else:
            first=False
        geojsonfile.write("""{"type": "Feature",
      "properties": {
      "station name": "%s",
      "full station name": "%s",
      "run name": "%s",
      "run submitted by": "%s",
      "data": "%s",
      "analyte_fraction_units": "%s"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          %f,
          %f
        ]
      }
    }"""%(stationNumber, stationEntry['Full Station Name'],stationEntry['Run Name'], stationEntry['RUN_SUBMITTED_BY'],stationEntry['Data'],stationEntry['Analyte_Fraction_Units'],stationEntry['Lon'], stationEntry['Lat'])) 
    #
    geojsonfile.write("""]
}""")
    geojsonfile.close()
    
if __name__=='__main__':
    import os
    path='D:\MercuryModeling\Data'
    for file in os.listdir(path):
        if file.endswith('.csv'):
            print os.path.join(path,file)
            csv2geojson(os.path.join(path,file))
#
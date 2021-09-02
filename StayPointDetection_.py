import datetime
import qgis 
from qgis.PyQt import QtGui
from math import sin, cos, sqrt, atan2, radians
import random

def rand_color():
    return "#" + "".join(random.sample("0123456789abcdef", 6))
    

def categorized(stay_point, stay_point_time, stay_point_distance):
    new_fn = 'C:\\Users\\matti\\Desktop\\Progetto GIG\\StayPoint.shp'
    layerFields = QgsFields()
    layerFields.append(QgsField('id', QVariant.Int))
    layerFields.append(QgsField('id_SP', QVariant.Int))

    writer = QgsVectorFileWriter(new_fn, 'UTF-8', layerFields, QgsWkbTypes.Point, QgsCoordinateReferenceSystem('EPSG:4326'), 'ESRI Shapefile')

    feat = QgsFeature()
    i = 0
    j = 0
    for s in stay_point:
            print(f'SP {j}: from {stay_point_time[j][0]} to {stay_point_time[j][1]}, range: {stay_point_distance[j] * 1000} m')
            for p in s:
                feat.setGeometry(QgsGeometry.fromPointXY(p))
                feat.setAttributes([i, j])
                writer.addFeature(feat)
                i+=1
            j+=1
    lyr = iface.addVectorLayer(new_fn, 'StayPoint', 'ogr')
    del(writer)

    d = dict()
    for n in range(0,j):
        d[n] = list()
    feats = lyr.getFeatures()
    for f in feats:
        geom = f.geometry()
        x = geom.asPoint()
        d[f['id_SP']].append(x)

    targetField = 'id_SP'
    rangeList = []
    opacity = 1
    min = 0
    max = len(d)
    i = 0
    minVal = min
    while i < max:
        lab = f'Stay Point {i}'
        maxVal = minVal+1
        rangeColor = QtGui.QColor(rand_color())
        # create symbol and set properties
        symbol2 = QgsSymbol.defaultSymbol(lyr.geometryType())
        symbol2.setColor(rangeColor)
        symbol2.setOpacity(opacity)
         
        #create range and append to rangeList
        range2 = QgsRendererRange(minVal, maxVal-1, symbol2, lab)
        rangeList.append(range2)
        minVal+=1
        i+=1

    groupRenderer = QgsGraduatedSymbolRenderer('', rangeList)
    groupRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
    groupRenderer.setClassAttribute(targetField)
     
    # apply renderer to layer
    lyr.setRenderer(groupRenderer)
     
    # add to QGIS interface
    QgsProject.instance().addMapLayer(lyr)

# Haversine Formule
# mi restituisce in chilometri la distanza
def calculate_distance(lat1,lon1,lat2,lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

def calculate_stay_points(fn, p_dist, minuti):
    p_dist = p_dist/1000 # conversion from meters to kilometers
    layer = iface.addVectorLayer(fn, '', 'ogr')
    feats = layer.getFeatures()
    p_time = minuti * 60 # seconds
    stay_point = list()   
    stay_point_time = list()
    stay_point_distance = list()
    points = [] 
    points_time = []
    S = list()
    for feat in feats:
        geom = feat.geometry()
        x = geom.asPoint()
        points.append(x)
        points_time.append(feat['time']) # times per traiettoria lunga

    flag = True
    i = 0
    while i < len(points):
        flag = True
        j = i+1
        while j < len(points):
            if calculate_distance(points[i].y(), points[i].x(), points[j].y(), points[j].x()) > p_dist:
                flag = False
                d2 = datetime.datetime.strptime(points_time[j-1], '%Y/%m/%d %H:%M:%S.%f')
                d1 = datetime.datetime.strptime(points_time[i], '%Y/%m/%d %H:%M:%S.%f')
                if (d2 - d1).seconds > p_time:
                    for index in range(i, j):
                        S.append(points[index])
                    stay_point_time.append([points_time[i], points_time[j-1]])
                    stay_point_distance.append(calculate_distance(points[i].y(), points[i].x(), points[j-1].y(), points[j-1].x()))
                    stay_point.append(S)
                    S = list()
                i = j
                break
            j+=1
        if flag:
            i+=1
        
    categorized(stay_point, stay_point_time, stay_point_distance)



        

calculate_stay_points('C:\\Users\\matti\\Desktop\\Progetto GIG\\traj.shp', 50, 40)  # distance in meters, time in minutes
#calculate_stay_points('C:\\Users\\matti\\Desktop\\Traiettoria test\\traj.shp', 40, 120) # Traiettoria lunga














#calculate_stay_points('C:\\Users\\matti\\Desktop\\Progetto GIG\\traj.shp', 35, 10)  # distance in meters, time in minutes
#calculate_stay_points('C:\\Users\\matti\\Desktop\\oneWayATraj\\traj_A.shp', 40, 120) # Traiettoria testo 3 esame


            
            
            


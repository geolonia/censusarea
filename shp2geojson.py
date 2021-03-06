"""
Convert for ESRI Shapefile to GeoJSON.
"""
import yaml
import fiona
import datetime as dt
from shapely.geometry import shape,Polygon
from shapely.ops import polylabel
import json
from GJWriter import GJWriter

# Open setting file.
with open('./shp2geojson.yaml' ,'r') as yml:
    config = yaml.load(yml, Loader=yaml.SafeLoader)

# Create instance of GJWriter
gjWriter = GJWriter(config['outputfile'])
# Get basic information from yaml
basedir = config['basedir']
layers = config['layers']

# Get layer information
for layer in layers:
    # Get file information
    for filename in layer['file']:
        # Print start message
        print('Start:['+str(dt.datetime.now())+']'+filename['name'])
        # Open the shapefile
        if 'encoding' in filename:
            elements = fiona.open(basedir+filename['name'] ,encoding='CP932')
        else:
            elements = fiona.open(basedir+filename['name'])
        # Get elements
        for element in elements:
            # Ignore Null Shapes
            if element['geometry']==None:
                continue
            # Set "Property" notation
            if 'class' in filename:
                gjWriter.setProperty('class' ,filename['class'])
            if 'subclass' in filename:
                gjWriter.setProperty('subclass' ,filename['subclass'])
            if 'admin_level' in filename:
                gjWriter.setProperty('admin_level' ,filename['admin_level'])
            if 'prop' in filename:
                gjWriter.setProperty('name' ,element['properties'][filename['prop']])
            # Set "Tippecanoe" notation
            gjWriter.setTippecanoe('layer' ,layer['layer'])
            if 'minzoom' in filename:
                gjWriter.setTippecanoe('minzoom' ,filename['minzoom'])
            if 'maxzoom' in filename:
                gjWriter.setTippecanoe('maxzoom' ,filename['maxzoom'])
            # Set "Geometry" notation
            if 'attr' in filename:
                # Attribute label (only polygon and multipolygon are supported)
                if element['geometry']['type']=='MultiPolygon' or element['geometry']['type']=='Polygon' :
                    # Get attribute name and set "Property" notation
                    gjWriter.setProperty('name' ,element['properties'][filename['attr']])
                    area=0.0
                    # Get polygon
                    for parts in element['geometry']['coordinates']:
                        if element['geometry']['type']=='MultiPolygon':
                            pgn = Polygon(parts[0])
                        else:
                            pgn = Polygon(parts)
                        if area < pgn.area:
                            # Save the polygon with the largest area
                            area = pgn.area
                            maxpgn=pgn
                    try:
                        # The label position is determined by the polylabel
                        geometry = "{\"type\":\"Point\",\"coordinates\":"
                        geometry += str(polylabel(maxpgn ,tolerance=10)).replace("(","[").replace(")","]").replace("\'","\"").replace("POINT " ,"").replace(" " ,",")
                        geometry += "}"
                    except:
                        # In case of InvalidPolygon, use centroid
                        geometry = "{\"type\":\"Point\",\"coordinates\":"
                        geometry += str(maxpgn.centroid).replace("(","[").replace(")","]").replace("\'","\"").replace("POINT " ,"").replace(" " ,",")
                        geometry += "}"
                    # Set "Geometry" notation
                    gjWriter.setGeometry(geometry)
                elif element['geometry']['type']=='Point':
                    gjWriter.setProperty('name' ,element['properties']['no'])
                    gjWriter.setGeometry(element['geometry'])
            else:
                # Write "Geometry" notation(Other than attribute label)
                gjWriter.setGeometry(element['geometry'])
            # Write "Geometry" notation
            gjWriter.Write()
            
        # Close Shapefile
        elements.close()
        # Print end message
        print('End  :['+str(dt.datetime.now())+']'+filename['name'])

# Dispose GJWriter instance
del gjWriter

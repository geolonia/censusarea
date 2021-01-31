#!/bin/bash
# Define
DOWNLOAD_DIR="./download"
SHAPE_DIR="./shape"
SPATIALITE_FILE="./censusarea.sqlite"
MBTILES="./censusarea.mbtiles"
GEOJSONFILE="./censusarea.json"
# Create or remove file ,directory
if [ ! -e ${DOWNLOAD_DIR} ]; then
	mkdir ${DOWNLOAD_DIR}
fi
if [ ! -e ${SHAPE_DIR} ]; then
	mkdir ${SHAPE_DIR}
fi
if [ -e ${SPATIALITE_FILE} ]; then
	rm ${SPATIALITE_FILE}
fi
if [ -e ${MBTILES} ]; then
	rm ${MBTILES}
fi
# Download census area and load database
for i in {1..47} ; do
	id=`printf %02d $i`
	echo ${id}
	if [ ! -e ${DOWNLOAD_DIR}/${id}.zip ]; then
		curl "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212015&code="${id}"&coordSys=1&format=shape&downloadType=5" -o ${DOWNLOAD_DIR}/${id}.zip
	fi
	unzip -o ${DOWNLOAD_DIR}/${id}.zip -d ${DOWNLOAD_DIR}
	spatialite_tool -i -shp ${DOWNLOAD_DIR}/h27ka${id} -d ${SPATIALITE_FILE} -t area${id} -c CP932 -s 4326 -2
done
# Create view and tables
spatialite ${SPATIALITE_FILE} < ./c_vallarea.sql
spatialite ${SPATIALITE_FILE} < ./city_area.sql
# Create Shapefile
spatialite_tool -e -shp ${SHAPE_DIR}/pref -d ${SPATIALITE_FILE} -t pref -g geometry -c CP932 --type POLYGON
spatialite_tool -e -shp ${SHAPE_DIR}/city -d ${SPATIALITE_FILE} -t city -g geometry -c CP932 --type POLYGON
spatialite_tool -e -shp ${SHAPE_DIR}/city_s -d ${SPATIALITE_FILE} -t city_s -g geometry -c CP932 --type POLYGON
spatialite_tool -e -shp ${SHAPE_DIR}/city_sb -d ${SPATIALITE_FILE} -t city_sb -g geometry -c CP932 --type POLYGON
spatialite_tool -e -shp ${SHAPE_DIR}/c_area -d ${SPATIALITE_FILE} -t c_area -g geometry -c CP932 --type POLYGON

# Create GeoJSON
python3 shp2geojson.py
# Create mbtiles
tippecanoe -z16 -o ${MBTILES} -n censusarea ${GEOJSONFILE}
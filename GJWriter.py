"""
Writing a GeoJSON File.
Note : Depended Fiona(Python Extend Module) data model.
"""
class GJWriter:
    """
    A class for writing GeoJSON file. 
    """
    def __init__( self ,inOutFile ):
        """
        Constructor method.
        :param inOutFile: Name of the file to output
        :type inOutFile: String
        """
        self._jsonfd = open(inOutFile ,'w')
        # Clear properties.
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

    def __del__(self):
        """
        Destructor method.
        """
        # Output Footer and close file.
        self._jsonfd.write( "\n" + "]}")
        self._jsonfd.close()

    def setGeometry(self ,inGeom):
        """
        Set "Geometry" notation.
        :param inGeom: Geometry data to output
        :type inOutFile: Objects in Fiona Geometry
        """
        self.Geometry = str(inGeom).replace("(","[").replace(")","]").replace("\'","\"")

    def setProperty(self ,inName ,inValue):
        """
        Set "Property" notation.
        "Tippecanoe" is special notation for the tippecanoe utility.
        :param inName: Name of the property
        :type inName: String
        :param inValue: Value of the property
        :type inValue: String or Integer
        """
        # Tabs for the first item, commas for the second and subsequent items
        if self.Properties==None:
            self.Properties = "\t"
        else:
            self.Properties+= ","
        # Set value
        if type(inValue) is int:
            self.Properties+= "\"" + inName + "\"" + ":" + str(inValue)
        elif inValue==None:
            self.Properties+= "\"" + inName + "\"" + ":" + "\""  + "\""
        else:
            self.Properties+= "\"" + inName + "\"" + ":" + "\"" + inValue + "\""

    def setTippecanoe(self ,inName ,inValue):
        """
        Set "Tippecanoe" notation.
        "Tippecanoe" is an attribute of Feature object.
        :param inName: Name of the tippecanoe
        :type inName: String
        :param inValue: Value of the tippecanoe
        :type inValue: String or Integer
        """
        # Tabs for the first item, commas for the second and subsequent items
        if self.Tippecanoe==None:
            self.Tippecanoe = "\t"
        else:
            self.Tippecanoe += ","        
        # Set value
        if type(inValue) is int:
            self.Tippecanoe += "\"" + inName + "\"" + ":" + str(inValue)
        else:
            self.Tippecanoe += "\"" + inName + "\"" + ":" + "\"" + str(inValue) + "\""

    def Write(self):
        """
        Writing GeoJSON file.
        """
        # Header for the first Feature, commas and LF for the second and subsequent items
        if self._jsonfd.tell()==0 :
            self._jsonfd.write("{" + "\"" + "type" + "\"" + ":" + "\"" + "FeatureCollection" + "\"" + "," + "\"" + "features" + "\""  + ": [" + "\n")
        else:
            self._jsonfd.write(",\n")

        # Set "type" notation(Header for the Feature)
        self._jsonfd.write("\t{\"type\":\"Feature\",\n")
        # Set "Geometry" notation
        self._jsonfd.write("\"geometry\":" + self.Geometry + ",\n")
        # Set "Tippecanoe" notation
        self._jsonfd.write("\"tippecanoe\":{" + self.Tippecanoe + "}")
        # Set "Property" notation
        if self.Properties != None:
            self._jsonfd.write(",\n")
            self._jsonfd.write("\"properties\":{" + self.Properties + "}")

        # End of Feature
        self._jsonfd.write("}")

        # Clear all properties
        self.Geometry = None
        self.Properties = None
        self.Tippecanoe = None

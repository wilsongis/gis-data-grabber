import arcpy
from urllib.request import urlopen  
import json

# baseURL = "http://services.gis.ca.gov/arcgis/rest/services/Environment/Wildfires/MapServer/0"
# outdata = "C:/Users/cordellm/Documents/ArcGIS/Projects/MyProject18/MyProject18.gdb/testdata"


def fetchRESTjson(url: str, verbose: bool = False) -> json:
  """Fetches the JSON outline with only id info for a REST service

  Args:
      url (str): Full URL to an ArcGIS Server REST service
      verbose (bool, optional): If True, outputs print statements. Defaults to False.

  Returns:
      json: JSON for REST service
  """  

  where = "1=1"
  urlstring = url + "/query?where={}&returnIdsOnly=true&f=json".format(where)
  if verbose:
    print(f"Querying: {urlstring}")
  j = urlopen(urlstring)
  return json.load(j)

def fetchRESTMaxRecs(url:str, verbose: bool = False) -> int:
  """Gets the maximum amount of records that can be queried at once for a service

  Args:
      url (str): Full URL for an ArcGIS Server REST service
      verbose (bool, optional): If True, outputs print statements. Defaults to False.

  Returns:
      int: Max amount of records that can be quereied at once for the service
  """  
  urlstring = url + "?f=json"
  j = urlopen(urlstring)
  js = json.load(j)
  maxrc = int(js["maxRecordCount"])
  if verbose:
    print (f"Record extract limit: %s" % maxrc)
  return maxrc

def numrecsFromURL(url: str, verbose: bool = False) -> int:
  """By popular demand, returns number of records based on just a URL. 

  Args:
      url (str): Full URL to an ArcGIS Server REST service.
      verbose (bool, optional): If True, outputs print statements. Defaults to False.

  Returns:
      int: Number of records
  """  

  return numrecs(fetchRESTjson(url,verbose),verbose)

def numrecs(serviceJSON: json, verbose: bool = False) -> int:
  """Extracts the total number of records in an ArcGIS Server REST service from service json.

  Args:
      serviceJSON (json): JSON info about REST service
      verbose (bool, optional): If True, outputs print statements

  Returns:
      int: The number of records present in the service at the given URL
  """  

  idlist = serviceJSON["objectIds"]
  if verbose:
    print (f"Number of target records: %s" % len(idlist))
  return len(idlist)
  
def getIdInfo(serviceJSON: json, verbose: bool = False)-> tuple[str,list]:
  """Extracts both the name of the id field and the list of ids from service json.

  Args:
      serviceJSON (json): JSON info about REST service
      verbose (bool, optional): If True, outputs print statements. Defaults to False.

  Returns:
      tuple[str,list]: (idfield, idlist)
  """  

  idfield = serviceJSON["objectIdFieldName"]
  idlist = serviceJSON["objectIds"]
  idlist.sort()
  return (idfield,idlist)

def RESTDownloader(baseURL: str,filename: str,
                   overwrite: bool=True, verbose: bool=False) -> bool:
  """Connects to an ArcGIS Server REST service and downloads all data from it 
  into the feature class stated in `filename`.
  Args:
      baseURL (str): Full URL to an ArcGIS Server REST service
      filename (str): The full filepath to a file geodatabase including the 
        feature class name (Example: C:/test.gdb/parcels)
      overwrite (bool): Determines if downloaded data overwrites pre-existing data
        in the output destination
      verbose (bool, optional): If True, outputs print statements. Defaults to False.

  Returns:
      bool: True if successful, False if not.
  """
  arcpy.env.overwriteOutput = True
  # TODO: Make fields a parameter.
  fields = "*"
  

  # Get record extract limit
  maxrc = fetchRESTMaxRecs(baseURL, verbose)

  # Get object ids of features
  js = fetchRESTjson(baseURL,verbose)
  numrec = numrecs(js,verbose)
  idfield,idlist = getIdInfo(js,verbose)
  # Gather features
  if verbose:
    print ("Gathering records...")
  fs = dict()
  for i in range(0, numrec, maxrc):
    torec = i + (maxrc - 1)
    if torec > numrec:
      torec = numrec - 1
    fromid = idlist[i]
    toid = idlist[torec]
    where = "{} >= {} and {} <= {}".format(idfield, fromid, idfield, toid)
    if verbose:
      print ("  {}".format(where))
    urlstring = baseURL + "/query?where={}&returnGeometry=true&outFields={}&f=json".format(where,fields)
    fs[i] = arcpy.FeatureSet()
    fs[i].load(urlstring)

  # Save features
  if verbose:
    print ("Saving features...")
  fslist = []
  for key,value in fs.items():
    fslist.append(value)
  arcpy.management.Merge(fslist, filename)
  if verbose:
    print ("Done!")
  return True
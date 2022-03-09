import json
import urllib.request
import zipfile
import os
import sys
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt

def download_and_extract_zip_file(url : str, file : str):
    """Download the data file from the url, and unzip it

    Args:
        url (str): URL to download the file
        file (str): Name of the file
    """
    zipped_name = file + ".zip"
    # Download file
    urllib.request.urlretrieve(url, zipped_name)
    # Extract file
    with zipfile.ZipFile(zipped_name, 'r') as zipped:
        zipped.extractall()
    # Remove zip
    os.remove(zipped_name)

def load_xml(file : str, searched_fuel : str):
    """Load and parse the XML file, filter results by the searched fuel

    Args:
        file (str): XML file
        searched_fuel (str): Searched fuel

    Returns:
        dict: all the fuel stations which provides the searched fuel
    """
    data = []
    root = ET.parse(file).getroot()
    # Get all fuel station
    for pdv in root.findall("pdv"):
        # Filter by fuel
        if(pdv.find("prix[@nom='" + searched_fuel + "']") != None) :
            element = {
                "latitude" : float(pdv.attrib["latitude"]) / 100000,
                "longitude" : float(pdv.attrib["longitude"]) / 100000,
                "cp" : pdv.attrib["cp"],
                "adresse" : pdv.find("adresse").text,
                "prix" : pdv.find("prix[@nom='" + searched_fuel + "']").attrib["valeur"]
            }
            data.append(element)
    return data

def distance(lat1, lat2, lon1, lon2):
    """ Calculate the distance between two LatLon
    Copied from https://www.geeksforgeeks.org/program-distance-two-points-earth/

    Args:
        lat1 (float): Latitude of the point 1
        lat2 (float): Latitude of the point 2
        lon1 (float): Longitude of the point 1
        lon2 (float): Longitude of the point 2
    """
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def filter_in_range(data : dict, latitude : float, longitude : float, range_km : int) :
    """Filter the data by range in km between source and gaz station

    Args:
        data (dict): Dict that contains gaz station informations
        latitude (float): Starting latitude
        longitude (float): Starting longitude
        range_km (int): Range max in km between starting point and gaz station

    Returns:
        dict: Filtered data by distance
    """
    filtered_data = []
    for element in data:
        if distance(latitude, element["latitude"], longitude, element["longitude"]) < range_km:
            filtered_data.append(element)
    return filtered_data


if __name__ == "__main__":
    # Verification of the number of arguments
    if len(sys.argv) != 6:
        print("Failed to launch the program, usage : python main.py <configuration_file> <latitude> <longitude> <fuel> <range_km>")
        exit(1)
    # Parsing of the configuration file
    with open(sys.argv[1]) as file :
        configuration = json.load(file)
    # Type verification of latitude and longitude
    try :
        latitude = float(sys.argv[2])
        longitude = float(sys.argv[3])
    except :
        print("Failed to launch the program, usage : python main.py <configuration_file> <latitude> <longitude> <fuel> <range_km>")
        print("Latitude and longitude must be float.")
        exit(1)
    # Fuel verification
    fuel = sys.argv[4]
    if fuel not in configuration["fuels"]:
        print("Failed to launch the program, usage : python main.py <configuration_file> <latitude> <longitude> <fuel> <range_km>")
        print("Fuel must be in the list : " + str(configuration["fuels"]))
        exit(1)
    # Type verification of the range
    try :
        range_km = int(sys.argv[5])
    except :
        print("Failed to launch the program, usage : python main.py <configuration_file> <latitude> <longitude> <fuel> <range_km>")
        print("Range must be an integer")
        exit(1)
    ########## Main program ##########
    print("Downloading and extracting file")
    download_and_extract_zip_file(configuration["url"], configuration["file"])
    print("Loading data")
    data = load_xml(configuration["file"], fuel)
    print("Filter by the distance")
    data = filter_in_range(data, latitude, longitude, range_km)
    print("Sorting by price")
    data = sorted(data, key=lambda x: x["prix"])
    for i in range(len(data)):
        print("Top " + str(i+1) + " : prix = " + data[i]["prix"] + ", position : " + data[i]["adresse"] + " (" + data[i]["cp"] + ")")

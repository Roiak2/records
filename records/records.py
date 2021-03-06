#!/usr/bin/env python

"""
A program that queries GBIF for records of a given genus in a given year range
"""
#Importing packages
import requests #to get records
import pandas as pd #to manipulate data

#Record class to query GBIF to return plant records from US and spatial data for user-inputted genus and years 
class Records:
    def __init__(self, genuskey=None, genusname=None, year=None):
        """
        Function to initialize the search parameters from GBIF
        and the dataframes where record requests will be stored
        
        ----
        PARAMETERS
        genusKey - the GBIF integer matching a specific genus. None is default
        genusName - the string of genus name to match to genusKey in GBIF.
        year - year(s) of records requested from GBIF
        """
        # store input params
        self.genuskey = genuskey
        self.genusname = genusname
        self.year = year
        
        # will be used to store output results
        self.df = None
        self.json = None
        
    def get_single_batch(self, offset=0, limit=20):
        "returns JSON result for a small batch query"

        #setting up unchanging parameters to then go into request.get command
        param = {
                "year": self.year,
                "offset": offset,
                "limit": limit,
                "hasCoordinate": "true",
                "country": "US",
                }
        #if user inputs genus key (i.e. integer), take that as argument in parameters
        if self.genuskey:
            param["genuskey"] = self.genuskey
        
        #else, if input is string of genus name, get that key from the rank argument in GBIF API query (i.e. 'q')
        elif self.genusname:
            param["q"] = self.genusname
            param["rank"] = "GENUS"
        
        #now make query from GBIF for the inputted genus and year from the parameter arguments above
        res = requests.get(
            url = "https://api.gbif.org/v1/occurrence/search/",
            params = param
        )
        
        #return the JSON data from the record request
        return res.json()
        
    def get_all_records(self):
        """
        Stores queried results for given genus and year range
        in JSON and dataframe (i.e. list of dictionaries)
        """
        # for storing results
        alldata = []

        # continue until we call 'break'
        offset = 0
        while 1:

            # get JSON data for a batch 
            jdata = self.get_single_batch(offset, limit=300)

            # increment counter by 300 (the max limit)
            offset += 300

            # add this batch of data to the growing list
            alldata.extend(jdata["results"])

            # stop when end of record is reached
            if jdata["endOfRecords"]:
                print(f'Done. Found {len(alldata)} records')
                break

            # print a dot on each rep to show progress
            print('.', end='')
        
        #return data
        return alldata
        #convert to dataframe of list of dictionaries
        self.json = alldata
        self.df = pd.json_normalize(alldata)
# REST Service Downloader

## Description
  Library for downloading features from an ArcGIS Server REST service. 

## Purpose
  Our clients are beginning to automate their workflows and want to provide data to us 
  in the form of REST services. To accomodate this, we need to be able to download data
  from their services.

## Other History 
  Mick Cseri with Montgomery County announced their intention to shift to providing
  data through REST services on January 21, 2025.
  Basis for this code came from https://socalgis.org/2018/03/28/extracting-more-features-from-map-services/ 
  and was modernized to Python 3.

  

-------------------------------------------------------------------------------------------------

## Requirements

+ Python 3.7

## Package Requirements

+ arcpy

## Optional Build Requirements


-------------------------------------------------------------------------------------------------
## Installation Instructions
  IDK

## Run as Standalone Tool
  From the root directory of this project, run `python -m rest-service-downloader`.

-----------------------------------------------------------------------------------------------------------
## Running Tests
  

### Build Pipeline
  
-----------------------------------------------------------------------------------------------------------
## Version History
  - v0.1.0: Wrote code that can be used to download a REST service and put it into a feature class.
  - v0.2.0: Split initial script into multiple functions.
  - v0.3.0: Add support for a method to run this script as a standalone.

## Planned Versions
  - v0.5.0: Basic tests written and implemented for ~80% of this code.
  - v1.0.0: Converted to proper Python library we can use internally.
  - v1.1.0: Supports export of service to shapefile (just in case?)
  

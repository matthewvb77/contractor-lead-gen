# mv-effect

#### Note: THIS PROJECT IS LIKELY AGAINST GOOGLE MAPS API TOS [Section 10.5 b. "No derivative works"](https://developers.google.com/maps/terms-20180207) AND HAS BEEN DELAYED INDEFINITELY

## Developer Notes

To test: `pytest`

## Script Docs

**streetview-sampler.py** - It hits the metadata endpoint once for each city with >20k population in North America, then saves the results to cities\*streetview.xlsx.

**data_analysis.py** - Uses the other scripts to generate data.

**scrape_region.py** - Takes a region defined by lat and lng ranges and requests all images in that region in a grid pattern using the meter_step parameter with 0% miss-rate by using the metadata endpoint first. Each run's results are saved to a new folder 'data/{city}/region_scrape\*{id}'. The folder's contents include a log file and all the image png files with naming format {lat},{lng}\_{direction}.png.

**identify_leads.py** TODO - Takes a run*id from scrape_region, and asks GPT-4 to identify leads from all the images in the folder. Saves results to a new file in the 'data/{city}/scrape_region*{id}' folder called 'leads.xlsx' where each row is in the following format: location: str, direction: str, date: str, roof_repair: bool, power_washing: bool, painting: bool, etc.

**get_address.py** TODO - Takes location and (direction?) and returns the address.

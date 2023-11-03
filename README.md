# mv-effect

Includes all code related to mv effect and it's operation.

### Developer Notes

To test: `pytest`

PRODUCTION SCRIPTS:

**streetview-sampler.py** - hits metadata endpoint once for each city in NA above 20k population. Saves results to cities*streetview.xlsx.
**data_analysis.py** - Uses the other scripts to generate data.
**scrape_region.py** - Takes a region defined by lat and lng ranges, scrapes all images in that region in a grid pattern using the meter_step parameter with 100% accuracy by using the metadata endpoint first. Each run's results are saved to a new folder 'data/{city}/region_scrape*{id}'. The folder's contents include a log file and all the image png files with naming format {lat},{lng}\_{direction}.png.
**identify_leads.py** TODO - Takes a run*id from scrape_region, and asks GPT-4 to identify leads from all the images in the folder. Saves results to a new file in the 'data/{city}/scrape_region*{id}' folder called 'leads.xlsx' where each row is in the following format: location, direction, date,
**get_address.py** TODO - Takes location and (direction?) and returns the address.

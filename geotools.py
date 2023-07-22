"""
Functions list:

1) img_dates
    This functions generate image acquisition graph of S1, S2, L8, and L9.

"""



# code as function
def img_dates(startDate, endDate, aoi, export, s1, s2, l8, l9):
    """
    Generates a chart of the availability of images in a collection.	
    
    ...
    
    Args:
    ----------
        startDate: The start date of the image collection. Format: YYYY-MM-DD
        endDate: The end date of the image collection. Format: YYYY-MM-DD
        aoi: The area of interest.
        export: If True, exports the plotly figure as html and png.
        s1: If True, includes Sentinel-1 in the plot.
        s2: If True, includes Sentinel-2 in the plot.
        l8: If True, includes Landsat-8 in the plot.
        l9: If True, includes Landsat-9 in the plot.
    
    Package Requirements:
    ---------------------
        ee, matplotlib, seaborn, pandas, numpy, plotly
    Returns:
    ----------
        A chart of the availability of images in a collection.
        Exported as an interactive HTML file, png, and data csv.

    Note:
    1)  To export plotly plot as png, kaleido package is required.
        currently (22-07-2021) kaleido version 0.1.0.post1 is the only version that works with plotly. The newer version has bug, so we need to install the older version.
        The code to downgrade and install working version is already included in the code.
        
    
    2)  User need to authenticate their google account to access Google Earth Engine.
        To authenticate, uncomment the ee.Authenticate() line and run the code.

    """
    
    # Function to get dates for image collections
    
    import ee
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    import plotly.express as px
    
    try:
        # Try to initialize Earth Engine
        ee.Initialize()
    except Exception as e:
        # If Earth Engine is not authenticated, authenticate it
        ee.Authenticate()
        ee.Initialize()
    if export == True:
        import pkg_resources; pkg_resources.require("kaleido==0.1.0.post1") or subprocess.call(["pip", "install", "--upgrade", "kaleido==0.1.0.post1"])

        
    def get_dates(collection, name):
        """Generates a chart of the availability of images in a collection.

        Args:
            collection: The Earth Engine image collection.

        Returns:
            A dictionary of the availability of images in the collection.
        """

        # Get the list of all available dates.
        date_range = collection.reduceColumns(ee.Reducer.toList(), ["system:time_start"])
        date_range = date_range.values().get(0)

        # Convert the list of dates to a list of strings.
        date_range = ee.List(date_range).map(lambda n: ee.Date(n).format("YYYY-MM-dd"))

        # Create a frequency histogram of the available dates.
        availability_dict = date_range.reduce(ee.Reducer.frequencyHistogram())

        # Convert the frequency histogram to a dictionary.
        availability_dict = ee.Dictionary(availability_dict).getInfo()

        for value in availability_dict:
            availability_dict[value] = name

        return availability_dict
    all_dicts = []
    if s1 == True:
        # Function to get dates for Sentinel-2
        def get_sentinel1_dates():
            sentinel1_collection = ee.ImageCollection("COPERNICUS/S1_GRD")\
                                    .filterDate(startDate, endDate)\
                                        .filterBounds(aoi)\
                                        .select('VV')

            return get_dates(sentinel1_collection, 'Sentinel-1')
        # Get dates for Sentinel-1
        sentinel1_data = get_sentinel1_dates()
        all_dicts.append(sentinel1_data)
    if s2 == True:
        # Function to get dates for Sentinel-2 surface reflectance
        def get_sentinel2_dates():
            sentinel2_collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")\
                                    .filterDate(startDate, endDate)\
                                        .filterBounds(aoi)\
                                            .select('B1')

            return get_dates(sentinel2_collection, 'Sentinel-2')
        # Get dates for Sentinel-2
        sentinel2_data = get_sentinel2_dates()
        all_dicts.append(sentinel2_data)
    if l8 == True:
        # Function to get dates for Landsat-8
        def get_landsat8_dates():
            landsat8_collection = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")\
                                    .filterDate(startDate, endDate)\
                                        .filterBounds(aoi)\
                                            .select('SR_B1')
            return get_dates(landsat8_collection, 'Landsat-8')
            # Get dates for Landsat-8
        landsat8_data = get_landsat8_dates()
        all_dicts.append(landsat8_data)
    if l9 == True:
        # Function to get dates for Landsat-9
        def get_landsat9_dates():
            landsat9_collection = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")\
                                    .filterDate(startDate, endDate)\
                                        .filterBounds(aoi)
            return get_dates(landsat9_collection, 'Landsat-9')
        # Get dates for Landsat-9
        landsat9_data = get_landsat9_dates()
        all_dicts.append(landsat9_data)

    # Create an empty dictionary to hold the combined data
    combined_dict = {}

    # Iterate over each dictionary in the list and add its items to the combined_dict
    for curr_dict in all_dicts:
        for date, code in curr_dict.items():
            # Check if the date is already in the combined_dict
            if date not in combined_dict:
                combined_dict[date] = code

    # If you want to convert it back to a dictionary and sort by date, you can do this:
    sorted_combined_dict = dict(sorted(combined_dict.items()))

    # Convert the dictionary to a Pandas DataFrame
    df = pd.DataFrame(list(combined_dict.items()), columns=['Date', 'Satellite'])
    


    # Plot using Plotly express line chart
    fig = px.line(df, x='Date', y='Satellite', line_group='Satellite', markers=True, color='Satellite',
                  title='Satellite Image Acquisition Dates from ' + startDate + ' to ' + endDate)
    fig.update_layout(xaxis_title='Date', xaxis_tickangle=-45)
    fig.show()
    
    if export == True:
        
        # export plotly figure as html
        # Export as an interactive HTML file
        fig.write_html(f'satellite_acquisition_{startDate}_{endDate}.html')
        fig.write_image(f'satellite_acquisition_{startDate}_{endDate}.png', width=1200, height=600, scale=2)
        
        # export data as csv
        df.to_csv(f'satellite_acquisition_{startDate}_{endDate}.csv', index=False)
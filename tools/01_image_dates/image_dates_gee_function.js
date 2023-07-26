/*
    ***** Image Dates Acquisition Tool *****

    This tool is used to find the available satellite images 
    in a given time period and for a given area of interest.
    
    The tool is developed by Mirza Waleed (waleedgeo@outlook.com)

    The tools is also available as a python version at:
    https://github.com/waleedgeo/geotools/blob/main/tools/01_image_dates/image_dates.ipynb

    Below is the code for the standalon function implemented in Google Earth Engine.
*/
    function generateCollectionChart(startDate, endDate, aoi){

        // Filter images by date range and AOI

    var col1 = ee.ImageCollection("COPERNICUS/S1_GRD")
                            .filterDate(startDate, endDate).filterBounds(aoi)
    var col2 = ee.ImageCollection("COPERNICUS/S2")
        .filterDate(startDate, endDate).filterBounds(aoi)
    var col3 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
        .filterDate(startDate, endDate).filterBounds(aoi)
    var col4 = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")
        .filterDate(startDate, endDate).filterBounds(aoi)
    

    var col1_range = col1.reduceColumns(ee.Reducer.toList(), ["system:time_start"])
        .values().get(0)
    col1_range = ee.List(col1_range)
        .map(function(n){
            return ee.Date(n).format("YYYY-MM-dd")
        })
    var col2_range = col2.reduceColumns(ee.Reducer.toList(), ["system:time_start"])
        .values().get(0)
    col2_range = ee.List(col2_range)
        .map(function(n){
            return ee.Date(n).format("YYYY-MM-dd")
        })
    var col3_range = col3.reduceColumns(ee.Reducer.toList(), ["system:time_start"])
        .values().get(0)
    col3_range = ee.List(col3_range)
        .map(function(n){
            return ee.Date(n).format("YYYY-MM-dd")
        })
    var col4_range = col4.reduceColumns(ee.Reducer.toList(), ["system:time_start"])
        .values().get(0)
    col4_range = ee.List(col4_range)
        .map(function(n){
            return ee.Date(n).format("YYYY-MM-dd")
        })
    
    var all_dates = col1_range.distinct()
                    .cat(col2_range.distinct())
                    .cat(col3_range.distinct())
                    .cat(col4_range.distinct())
                    .distinct().sort()

    var col1_dict = col1_range.reduce(ee.Reducer.frequencyHistogram())
    var col1_dict = ee.Dictionary(col1_dict)
    var col2_dict = col2_range.reduce(ee.Reducer.frequencyHistogram())
    var col2_dict = ee.Dictionary(col2_dict)
    var col3_dict = col3_range.reduce(ee.Reducer.frequencyHistogram())
    var col3_dict = ee.Dictionary(col3_dict)
    var col4_dict = col4_range.reduce(ee.Reducer.frequencyHistogram())
    var col4_dict = ee.Dictionary(col4_dict)
    //print(asc_avail_dict, desc_avail_dict)
    
    var col1_feat = col1_dict.map(function(date, n){
        return ee.Feature(ee.Geometry.Point(77.58, 13), {label: date, number_images:n, s1: n, s2: 0, l8:0, l9:0, weight:1})
    }).values()
    var col2_feat = col2_dict.map(function(date, n){
        return ee.Feature(ee.Geometry.Point(77.58, 13), {label: date, number_images:n, s1: 0, s2: n, l8:0, l9:0, weight:1})
    }).values()
    var col3_feat = col3_dict.map(function(date, n){
        return ee.Feature(ee.Geometry.Point(77.58, 13), {label: date, number_images:n, s1: 0, s2: 0, l8:n, l9:0, weight:1})
    }).values()
    var col4_feat = col4_dict.map(function(date, n){
        return ee.Feature(ee.Geometry.Point(77.58, 13), {label: date, number_images:n, s1: 0, s2: 0, l8:0, l9:n, weight:1})
    }).values()
    

    
    var comb_feat = col1_feat.cat(col2_feat).cat(col3_feat).cat(col4_feat)
    var comb_col = ee.FeatureCollection(comb_feat);
    //print(comb_col)
    
    // map over dates
    var merged_collection = ee.FeatureCollection(all_dates.map(function(date){
        var new_feat_collection1 = comb_col.filter(ee.Filter.equals('label', date))
        var s1_sum = new_feat_collection1.reduceColumns({
            reducer: ee.Reducer.sum(),
            selectors: ['s1'],
            weightSelectors: ['weight']
            }).get('sum')
        var s2_sum = new_feat_collection1.reduceColumns({
            reducer: ee.Reducer.sum(),
            selectors: ['s2'],
            weightSelectors: ['weight']
            }).get('sum')
        var l8_sum = new_feat_collection1.reduceColumns({
            reducer: ee.Reducer.sum(),
            selectors: ['l8'],
            weightSelectors: ['weight']
            }).get('sum')
        var l9_sum = new_feat_collection1.reduceColumns({
            reducer: ee.Reducer.sum(),
            selectors: ['l9'],
            weightSelectors: ['weight']
            }).get('sum')

        var merged = comb_col.filter(ee.Filter.equals('label', date))
        .union().first()
        .set({label:date, s1:s1_sum, s2:s2_sum, l8:l8_sum, l9:l9_sum})


        return(merged)
    }))

    
    // Define the chart and print it to the console.
    var chart = ui.Chart.feature
        .byFeature({
        features: merged_collection.select('s1', 's2', 'l8', 'l9', 'label'),
        xProperty: 'label'
        })
        .setChartType('ColumnChart')
        .setOptions({
        width: 100,
        height: 40,
        title: 'Satellite Image Availability',
        hAxis: {title: 'Dates', titleTextStyle: {italic: false, bold: true}},
        vAxis: {title: 'Number of images',
                titleTextStyle: {italic: false, bold: true}
        },
        colors: ['blue', 'green', 'red', 'purple'],
        isStacked: 'absolute'
        })
        
    return(chart);
    }

    var startDate = '2022-01-01'
    var endDate = '2023-01-01'

    print(generateCollectionChart(startDate, endDate, aoi))
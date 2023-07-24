
# GeoTools

This repository contains various remote sensing, Google Earth Engine, ArcPy, and Python-based tools for different geospatial applications. The overall purpose of these tools is to provide a set of functions that can be used to automate common geospatial tasks. The tools are organized into different directories based on their source package.

## List of Tools

click on the tool name to see the code, documentation, and visualziation.

- **[img_dates:](/scripts/gee/img_dates.ipynb)** A tool for extracting and visualizing the dates of available images in a GEE image collection.

![Imgur](https://imgur.com/HjlzjP0.gif)

**More tools coming soon!**

## Installation

Currently, the geotools require Python 3 and associated libraries like numpy, rasterio, ee, geemap etc. Specific dependencies are listed in the requirements.txt file. The easiest way to install the dependencies is to use conda. If you don't have conda installed, you can download and install it from [here](https://docs.conda.io/en/latest/miniconda.html).

Clone the repository and install requirements:

```
git clone https://github.com/waleedgeo/geotools.git
pip install -r requirements.txt
```

Then you can either open each jupyter noteebook in the tools directory and run the code, or you can import the tools as a module in your own Python scripts.
To import the tools as a module, add the path to the geotools directory to your PYTHONPATH environment variable. For example, if you are using a bash shell, you can add the following line to your .bashrc file:

```
export PYTHONPATH=$PYTHONPATH:/path/to/geotools
```

Then you can import the tools in your Python scripts:

Alternatively, you can also copy the geotools.py file to your working directory and import the tools as a module in your Python scripts:

```
from geotools import NAME_OF_TOOL
```


## Contributing

Contributions in the form of additional tools, improvements, or bug fixes are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# Pseudo Code
# Program Design

# Extraction.py responsible for extracting data from Med Associates Files to a FileData object 
# that has both data (dictionary) and metadata (list) attriobutes

# FileData objects require a filename at the time of initialization or will be prompted for the filepath when the class is called
# This can be useful if you want to add a single data file from the commandline vs multiple data files in a later implemented GUI

# Specific subclasses are implemented to extend FileData objects to insert the data correctly into the database through
# the Extraction.store_data method

# In the future, GUI will need to have checkboxes/some other solution for select available program modules from the databse so that the GUI
# can correctly insert the selected data files

# Database specific commands (connection and initialization of cursors, creating/erasing the database tables are located in database.py)
# are available in the database module



### TO DO ###

# Short Term:
#   - Output data from dataframe to csv text file
#   - refactor database.py and get ready for integration with GUI
#   - refactor Retrieve.py and get ready for integration with GUI
#

# Long Term:
#   - Selecting Multiple Files at once
#   - GUI
#   - Directory Scan for files not included in the database along with a list of programs not found in the database
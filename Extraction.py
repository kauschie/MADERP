# Mike and Amy Data Extraction Retrieval Program
# 
#   Data Extraction from MPC Data Files


class DataParsingError(Exception):
    # Print error to the screen with the GUI or to a log 
    pass
class InvalidProgramError(Exception):
    pass
    # Print error that an incorrect file type was selected for datafile

class MetadataError(Exception):
    pass

class FileData:
    """File Object with Data and Metadata taken from MPC Files
    
    Metadata is loaded into a standard Python List object as self.metadata
    Data is loaded into a standard Python dictionary object as self.data"""
    list_of_datafiles = []

    def __init__(self, filename=None):
        """If file_data object is called with filename kwarg, methods are
        automatically called to retrieve data. 
        
        This class is designed to accept calls to FileData from a menu where the only argument is the filepath.
        Otherwise, program will prompt for filename in terminal
        
        self.metadata & self.data will be set to None if there are any errors importing the data
        """

        if not filename:
            filename = self._get_filename()
        self.filename = filename
        self.lines = self._import_file()
        try:
            self._get_metadata()
            if not self.metadata['program'] in self.valid_file_formats:
                raise InvalidProgramError
        except InvalidProgramError:
            print(f"{self.metadata['program']} is unable to be imported as a {type(self).__name__} object")
        except MetadataError:
            print(f"The metadata for {self.filename} could not be read")
        except Exception as e:
            print(f"Unexpected {type(e)} error with {e.args}")
        try:
            self._get_data()
        except DataParsingError:
            self.data = None
        except Exception as e:
            print(f"Unexpected {type(e)} error with {e.args}")
            self.data = None

        FileData.list_of_datafiles.append(self)

        # for key, value in data.items():
        #     print(key,':',value,'\n') # Debug

    def _get_filename(self):
        """Prompts the user for a relative filename or the absolute filepath
        This method is called if file_data is not initialized with a filename

        Returns the filename/path"""

        print('Enter name of file to be read')
        print('If the file is located in a different folder than this program')
        print('Enter the full path (with filename) to the file')
        fname = input('Press return for default test file (test_data.bak): ')
        if len(fname)<1: fname = 'c:\\my_docs\\Coding\\Python\\maderp\\test_data.bak'
        return fname

    def _import_file(self):
        """Attempts to open and read a provided file.
        If it is successful it returns the contents of the file"""
        # print(f"Attempting to open file {fname}...") # Debug
        while True:
            try:
                fhand = open(self.filename)
                lines = fhand.readlines()
                fhand.close()
                return lines
            except OSError:
                print(f"Could not open {self.filename}")
                print("Verify the file path and try again...")
            fhand = input("Enter the full or relative file path: ")

    def _get_metadata(self):
        """Reads through the lines of a file to find and return the metadata as a dictionary
    Requires the file to be opened and it's contents to be read into a variable and passed as an arg"""
        try:
            i = 1
            for line in self.lines:
                line = line.rstrip()
                if line:
                    words = line.split()
                    if i == 1:
                        file_name = line[6:]
                        i+=1
                        continue
                    elif i == 2: 
                        pieces = words[2].split('/')
                        start_date = '20'+pieces[2]+'-'+pieces[0]+'-'+pieces[1]
                        i += 1
                        continue
                    elif i == 3:
                        pieces = words[2].split('/')
                        end_date = '20'+pieces[2]+'-'+pieces[0]+'-'+pieces[1]
                        i += 1
                        continue
                    elif i == 4:
                        rat_id = line[9:]
                        i += 1
                        continue
                    elif i == 5:
                        experiment = int(line[12:])
                        i += 1
                        continue
                    elif i == 6:
                        group = int(line[7:])
                        i += 1
                        continue
                    elif i == 7:
                        box = int(words[1])
                        i += 1
                        continue
                    elif i == 8:
                        start_time = words[2]
                        pieces = words[2].split(':')
                        num = int(pieces[0])
                        pieces[0] = f"{num:02}"
                        start_time = ':'.join(pieces)
                        i += 1
                        continue
                    elif i == 9:
                        end_time = words[2]
                        i += 1
                        continue
                    elif i == 10:
                        program = line[5:]
                        i += 1
                        continue
                    else:
                        break
        except Exception as e:
            self.metadata = None
            raise MetadataError(f"Error occured on line {i} with args ({e.args}")

        metadata = {
            'file_name': file_name,
            'start_date': start_date,
            'end_date': end_date,
            'rat_id': rat_id,
            'experiment' : experiment,
            'groups' : group,
            'box': box,
            'start_time' : start_time,
            'end_time' : end_time,
            'program': program,
        }

        self.metadata = metadata


    def _get_data(self):
        """Reads through the lines of a file to find and return all data and vars as a dictionary
    Requires the file to be opened and it's contents to be read into self.lines"""
        i = 1
        header_size = 11
        errors = 0
        array_flag = 0
        array_char = ''
        array_list = []
        d = {}
        for line in self.lines:
            line = line.rstrip()

            if line and i < header_size:     # skip metadata information
                i += 1
                continue
            words = line.split()
    
    ## MPC data files consist of 26 variables with each variable being one of two variable types.
    # Each variable is named with a letter of the alphabet. 
    # If an array isn' listed within the mpc program as having dimensionality to it, then it will be a single variable type
    # if the array has dimensionality to it then it will be essentially be an indexed list of values called an array
    # the Single Variable types are listed first with the pattern [Letter]: [data] 
    # Variables are split at ':'. 
    #              If there are two items after the split its a variable
    #                                    and the first one is a letter its a variable
    #               If the first item is a letter
    #               If there's a numerical value you are in the array variables

    # The arrays are printed afterwards so an array_flag is set to switch the program logic


    ## If the line isnt blank, and if it starts with a letter and the arrays haven't started printing yet
            if line and words[0][0].isalpha() and array_flag == 0:
                array_char = words[0][0]
                words = line.split()
                # print(f"found the following words: {words}") # Debug
                if len(words) == 2:                     # identify variable and store data in dictionary wntry
                    # print("you found a variable") # Debug
                    d[array_char] = int(float(words[1]))
                    continue
                elif len(words) == 1:                   # identfy array header
                    # print("you found an array") # Debug
                    array_flag = 1
                    array_list = []
                    continue
                else:                                   # error catch in case a data file isn't formatted correctly
                    raise DataParsingError(f"I was expecting a one or two word list and instead there were {len(words)}")
                    ## Return an Exception Here Later <!>
            
            ## if the line begins with a digit, continue adding the data into the array's list
            if line and words[0][0].isdigit():
                for word in words[1:]:
                    array_list.append(int(float(word)))
                continue

            ## If the line starts with a letter and the array flag has already been triggered, 
            ## it's time to begin a new list and enter that in the dictionary

            if line and words[0][0].isalpha() and array_flag == 1:       # identify if line starts with the array variable or a digit
                length = len(array_list)    # if the line starts with a digit, the line being read is within a data array
                d[array_char] = array_list
                array_char = words[0][0]
                array_list = []
                continue

        d[array_char] = array_list
        if not len(d) == 26:
            raise DataParsingError(f"Error parsing the data for {self.filename}. I was expecting 26 variables and I found {len(d)}")

        self.data = d

## Notes about adaptations of FR Programs to data structure
## Amy FR Program v6 doesnt have variable A(10) - Cue Type

class FRFileData(FileData):
    valid_file_formats = ["Amy FR Program v8", "Amy FR Program v7", "Amy FR Program v6"]
    dtname = 'FRdVars' # 'data table name in DoctorG.db'
    def __init__(self, filename=None):
        super().__init__(filename)
        # control variables (cvar) required for database module to access for this class
        # each subclass needs to implement these variables differently for data insertion into database
        # _cvar_array should be the dictionary key for the array that the data is found in
        # a list of indexes that the array elements are in the corresponding array
        # a list of names in sequential order of the data being pulled out that corresponds] to the columns from the DoctorG.db database
        # if the values are spread throughout multiple arrays then the _get_multi_vars will need to be implemented which accepts lists of lists for the arrays, names and indexes
        
        self._cvar_array_ = self.data['A']
        self._cvar_indexes_ = [0,1,2,3,4,5,6,7,10]
        self._cvar_names_ = [
            'session_duration',
            'active_side',
            'inactive_side',
            'fr',
            'max_rewards',
            'light_dur',
            'pump_dur',
            'to_dur',
            'cue_type']

        # Remove cue_type cvar which wasn't present in v6 of the program
        if self.metadata['program'] == 'Amy FR Program v6':
            self._cvar_indexes_.pop()
            self._cvar_names_.pop()
        # dependant variables (dvar) required for database module to access for this class
        # each subclas needs to implement these variables differently for data insertion into the db
        self._dvar_array_ = self.data['B']
        self._dvar_indexes_ = [0,1,2,3,4,5]
        self._dvar_names_ = [
            'actrsp',
            'inactrsp',
            'rewards',
            'sessionend',
            'actrspto',
            'inactrspto',
        ]

        self.cvars = _get_vars(self._cvar_array_, self._cvar_indexes_, self._cvar_names_)
        self.dvars = _get_vars(self._dvar_array_, self._dvar_indexes_, self._dvar_names_)

class PRFileData(FileData):
    valid_file_formats = ["Amy PR Program"]
    dtname = 'PRdVars'
    # create cvars and dvars


def _get_vars(array, indexes, names):
    """Looks up data in specified mpc array at specified list of indexes and creates a 
    vars dictionary with values being array[index] = data
    
    used when looking up cvar and dvar data from FileData.data"""
    vars = {}
    values = [array[index] for index in indexes]
    i = 0
    for column in names:
        vars[column] = values[i]
        i += 1
    return vars

# commented out until it needs to be used
# useful if dvars or cvars are spread through 
#
# def _get_multi_vars_(list_of_arrays, list_of_indexes, list_of_names):
#     """Returns a dictionary with variables in the event there are variables that span multiple arrays"""
#     i = 0
#     vars = {}
#     all_vars = {}
#     for array in list_of_arrays:
#         vars = _get_vars_(array, list_of_indexes[i], list_of_names[i])
#         for key, value in vars.items():
#             all_vars[key] = value
#         i += 1
#     return all_vars

if __name__ == "__main__":
    Database = None
    n09 = FRFileData('data/test_data.bak')
    n06 = FRFileData('data/test_data2.bak')
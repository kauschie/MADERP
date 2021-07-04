# Mike and Amy Data Extraction Retrieval Program
# 
#   Data Extraction from MPC Data Files


class FileData:
    """File Object with Data and Metadata taken from MPC Files
    
    Metadata is loaded into a standard Python List object as self.metadata
    Data is loaded into a standard Python dictionary object as self.data"""

    def __init__(self, filename=None):
        """If file_data object is called with filename kwarg, methods are
        automatically called to retrieve data. 
        
        Otherwise, program will prompt for filename in terminal"""
        if filename:
            self.filename = filename
        else:
            self.filename = self._get_filename_()
        self.lines = self._load_file_()
        self.metadata = self._get_metadata_()
        # print(metadata) # Debug
        if not self.metadata['program'] in self.valid_file_formats:
            raise Exception("Invalid file format")
        self.data = self._get_data_()
        # for key, value in data.items():
        #     print(key,':',value,'\n') # Debug

    def _get_filename_(self):
        """Prompts the user for a relative filename or the absolute filepath
        This method is called if file_data is not initialized with a filename

        Returns the filename/path"""

        print('Enter name of file to be read')
        print('If the file is located in a different folder than this program')
        print('Enter the full path (with filename) to the file')
        fname = input('Press return for default test file (test_data.bak): ')
        if len(fname)<1: fname = 'c:\\my_docs\\Coding\\Python\\maderp\\test_data.bak'
        return fname

    def _load_file_(self):
        """Attempts to open and read a provided file.
        If it is successful it returns the contents of the file"""
        # print(f"Attempting to open file {fname}...") # Debug
        try:
            fhand = open(self.filename)
        except OSError:
            print(f"Could not open {self.filename}")
            print("Verify the file name and this program's location")
            print("Quitting now...")
            quit()
        # print(f"{fname} opened successfully...") # Debug
        lines = fhand.readlines()
        fhand.close()
        return lines

    def _get_metadata_(self):
        """Reads through the lines of a file to find and return the metadata as a dictionary
    Requires the file to be opened and it's contents to be read into a variable and passed as an arg"""

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

        metadata = {
            'file_name': file_name,
            'start_date': start_date,
            'end_date': end_date,
            'rat_id': rat_id,
            'experiment' : experiment,
            'group' : group,
            'box': box,
            'start_time' : start_time,
            'end_time' : end_time,
            'program': program,
        }

        # <!> Raise Error 
        if not len(metadata) == 10:
            print("Could not Gather file information")
            print("Quitting now...")
            quit()
        
        return metadata

    def _get_data_(self):
        """Reads through the lines of a file to find and return all data and vars as a dictionary
    Requires the file to be opened and it's contents to be read into a variable and passed as an arg"""
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

            if line and words[0][0].isalpha() and array_flag == 0:
                array_char = words[0][0]
                # print(f"found the {line[0]} array") # Debug
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
                    print("you encountered an error parsing the data...")
                    return None
                    ## Return an Exception Here Later <!>
            
            if line and words[0][0].isdigit():
                for word in words[1:]:
                    array_list.append(int(float(word)))
                continue

            if line and words[0][0].isalpha() and array_flag == 1:       # identify if line starts with the array variable or a digit
                length = len(array_list)    # if the line starts with a digit, the line being read is within a data array
                # print(f"There were {length} elements in the {array_char} array") # Debug
                d[array_char] = array_list
                array_char = words[0][0]
                array_list = []
                continue

        d[array_char] = array_list
        return d

## Notes about adaptations of FR Programs to data structure
## Amy FR Program v6 doesnt have variable A(10) - Cue Type

class FRFileData(FileData):
    valid_file_formats = ["Amy FR Program v8", "Amy FR Program v7", "Amy FR Program v6"]
    dtname = 'FRiVars' # 'data table name in DoctorG.db'
    def __init__(self, filename=None):
        super().__init__(filename)
        # control variables (cvar) required for database module to access for this class
        # each subclass needs to implement these variables differently for data insertion into database
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
        # independant variables (ivar) required for database module to access for this class
        # each subclas needs to implement these variables differently for data insertion into the db
        self._ivar_array_ = self.data['B']
        self._ivar_indexes_ = [0,1,2,3,4,5]
        self._ivar_names_ = [
            'actrsp',
            'inactrsp',
            'rewards',
            'sessionend',
            'actrspto',
            'inactrspto',
        ]

        self.cvars = _get_vars_(self._cvar_array_, self._cvar_indexes_, self._cvar_names_)
        self.ivars = _get_vars_(self._ivar_array_, self._ivar_indexes_, self._ivar_names_)

class PRFileData(FileData):
    valid_file_formats = ["Amy PR Program"]
    dtname = 'PRiVars'
    # create cvar and ivars


def _get_vars_(array, indexes, names):
    """Looks up data in specified mpc array at specified list of indexes and creates a 
    vars dictionary with values being array[index] = data
    
    used when looking up cvar and ivar data from FileData.data"""
    vars = {}
    values = [array[index] for index in indexes]
    i = 0
    for column in names:
        vars[column] = values[i]
        i += 1
    return vars

# commented out until it needs to be used
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
    n09 = FRFileData('test_data.bak')
    n06 = FRFileData('test_data2.bak')
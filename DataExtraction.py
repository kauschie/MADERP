# Mike and Amy Data Extraction Retrieval Program
# 
#   Data Extraction from MPC Data Files

class file_data:
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
            self.filename = self.get_filename()
        self.lines = self.open_file(self.filename)
        self.metadata = self.get_metadata(self.lines)
        # print(metadata) # Debug
        self.data = self.get_data(self.lines)
        # for key, value in data.items():
        #     print(key,':',value,'\n') # Debug

    def get_filename(self):
        """Prompts the user for a relative filename or the absolute filepath
        This method is called if file_data is not initialized with a filename

        Returns the filename/path"""

        print('Enter name of file to be read')
        print('If the file is located in a different folder than this program')
        print('Enter the full path (with filename) to the file')
        fname = input('Press return for default test file (test_data.bak): ')
        if len(fname)<1: fname = 'c:\\my_docs\\Coding\\Python\\maderp\\test_data.bak'
        return fname

    def open_file(self, fname):
        """Attempts to open and read a provided file.
        If it is successful it returns the contents of the file"""
        # print(f"Attempting to open file {fname}...") # Debug
        try:
            fhand = open(fname)
        except OSError:
            print(f"Could not open {fname}")
            print("Verify the file name and this program's location")
            print("Quitting now...")
            quit()
        # print(f"{fname} opened successfully...") # Debug
        lines = fhand.readlines()
        fhand.close()
        return lines

    def get_metadata(self, lines):
        """Reads through the lines of a file to find and return the metadata as a dictionary
    Requires the file to be opened and it's contents to be read into a variable and passed as an arg"""

        i = 1
        for line in lines:
            line = line.rstrip()
            if line:
                if i == 1:
                    file_name = line
                    i+=1
                    continue
                elif i == 2: 
                    start_date = line
                    i += 1
                    continue
                elif i == 4:
                    rat_id = line
                    i += 1
                    continue
                elif i == 7:
                    box = line
                    i += 1
                    continue
                elif i == 10:
                    program = line
                    i += 1
                    continue
                else:
                    i += 1
                    continue

        metadata = {
            'file_name': file_name,
            'start_date': start_date,
            'rat_id': rat_id,
            'box': box,
            'program': program,
        }

        # <!> Raise Error 
        if not len(metadata) == 5:
            print("Could not Gather file information")
            print("Quitting now...")
            quit()
        
        return metadata

    def get_data(self, lines):
        """Reads through the lines of a file to find and return all data and vars as a dictionary
    Requires the file to be opened and it's contents to be read into a variable and passed as an arg"""
        i = 1
        header_size = 11
        errors = 0
        array_flag = 0
        array_char = ''
        array_list = []
        d = {}
        for line in lines:
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
                    d[array_char] = float(words[1])
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
                    array_list.append(word)
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
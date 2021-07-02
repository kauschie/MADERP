# Mike and Amy Data Extraction Retrieval Program
# 
#   Data Extraction from MPC Data Files

import sqlite3

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
            self.filename = self.get_filename()
        self.lines = self.load_file()
        self.metadata = self.get_metadata()
        # print(metadata) # Debugquit
        if not self.metadata['program'] in self.valid_file_formats:
            raise Exception("Invalid file format")
        self.data = self.get_data()
        # for key, value in data.items():
        #     print(key,':',value,'\n') # Debug

    def _OrganizeData_(self):
        """ Sorts Data based on subclass """
        pass

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

    def load_file(self):
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

    def get_metadata(self):
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
                    start_date = words[2]
                    i += 1
                    continue
                elif i == 3:
                    end_date = words[2]
                    i += 1
                    continue
                elif i == 4:
                    rat_id = line[9:]
                    i += 1
                    continue
                elif i == 5:
                    experiment = line[12:]
                    i += 1
                    continue
                elif i == 6:
                    group = line[6:]
                    i += 1
                    continue
                elif i == 7:
                    box = words[1]
                    i += 1
                    continue
                elif i == 8:
                    start_time = words[2]
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

    def get_data(self):
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
    
    def store_data(self):
        pass

## Notes about adaptations of FR Programs to data structure
## Amy FR Program v6 doesnt have variable A(10) - Cue Type

class FRFileData(FileData):
    valid_file_formats = ["Amy FR Program v8", "Amy FR Program v7", "Amy FR Program v6"] 

    def store_data(self):
        curr= initialize_db()
        print("Executing statements to store FR data into the database")
        # code to enter FR data into database
        print("closing connection to database")
        cur.close()




class PRFileData(FileData):
    valid_file_formats = ["Amy PR Program"]

    def store_data(self):
        cur = initialize_db()
        print("Executing statements to store PR data into the database")
        # code to enter PR data into database
        print("closing connection to database")
        cur.close()

def initialize_db():
    global Database
    if not Database:
        try:
            conn = sqlite3.connect('DoctorG.db')
            print("Connection to DoctorG.db established")
            return conn.cursor()
        except:
            print("Could not connect to DoctorG.db")
            quit()
    else:
        print("Connection to DoctorG.db already established")
        return conn.cursor()

if __name__ == "__main__":
    Database = None
    n09 = FRFileData('test_data.bak')
    n06 = FRFileData('test_data2.bak')
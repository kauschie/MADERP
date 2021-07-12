## Updates database with 

import sqlite3
import os
from Extraction import FRFileData as FR


class Database:
    conn = None

    def __init__(self, database=None):
        """Creates a connection to the main database for use in the Extraction module
            connection is stored in Database.conn class variable to use in the event multiple cursors are
            needed so that program doesn't get bogged down creating a connection to the database over and over
        
        call set_groups to import groups from configuration file and set them in the data table
        automatically call set_groups after data import


        """

        if not Database.conn:
            try:
                if database:
                    DBQuery = database
                else:
                    print('Enter the filepath for the databse')
                    DBQuery = input('Press return to use default "DoctorG.db":')
                    if len(DBQuery)<1:
                        DBQuery = 'DoctorG.db'
                Database.conn = sqlite3.connect(DBQuery)
                print(f"Connection to {DBQuery} established")
            except:
                print(f"Could not connect to {DBQuery}")
                print("Check file name or path and try again")
                quit()
        else:
            print("Connection to DoctorG.db already established")
            print("Query for a cursor to the sqlite database...")
    
    def _erase_all_tables_(self, cursor):
        """Erases all tables. 
        This should only be used for testing purposes which is why i made it an internal
        """

        cursor.executescript('''
        DROP TABLE IF EXISTS DataFiles;
        DROP TABLE IF EXISTS Dates;
        DROP TABLE IF EXISTS Metadata;
        DROP TABLE IF EXISTS Programs;
        DROP TABLE IF EXISTS Subjects;
        DROP TABLE IF EXISTS Times;
        DROP TABLE IF EXISTS FRdVars;
        DROP TABLE IF EXISTS FRcVars
        ''')
    
    def _create_all_tables_(self, cursor):
        """Creates all tables. 
        This should only be used for testing purposes which is why i made it an internal
        """

        cursor.executescript('''
        CREATE TABLE "DataFiles" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            filepath TEXT UNIQUE, 
            dateadded_id INTEGER, 
            metadata_id INTEGER, 
            program_id INTEGER,
            datatablename INTEGER,
            dvars_id INTEGER,
            cvars_id INTEGER
        );

        CREATE TABLE "Dates" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            date TEXT UNIQUE
        );

        CREATE TABLE "Programs" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            program TEXT UNIQUE,
            datatablename TEXT
        );

        CREATE TABLE "Subjects" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            subject TEXT UNIQUE
        );

        CREATE TABLE "Times" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            time TEXT UNIQUE
        );

        CREATE TABLE "Metadata" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            OrigFilePath TEXT UNIQUE,
            startdate_id INTEGER,
            enddate_id INTEGER,
            subject_id INTEGER,
            box INTEGER,
            starttime_id INTEGER,
            endtime_id INTEGER,
            program_id INTEGER,
            groups TEXT
        );

        CREATE TABLE "FRdVars" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            datafile_id INTEGER UNIQUE,
            actrsp INTEGER,
            inactrsp INTEGER,
            rewards INTEGER,
            sessionend INTEGER,
            actrspto INTEGER,
            inactrspto INTEGER
        );

        CREATE TABLE "FRcVars" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            datafile_id INTEGER UNIQUE,
            session_duration INTEGER,
            active_side INTEGER,
            inactive_side INTEGER,
            fr INTEGER,
            max_rewards INTEGER,
            light_dur INTEGER,
            pump_dur INTEGER,
            to_dur INTEGER,
            cue_type INTEGER
            )
        ''')

    def _testing_(self):
        """Starts the database fresh. Should only be used for testing otherwise you will lose all your data"""
        cur = Database.conn.cursor()
        self._erase_all_tables_(cur)
        self._create_all_tables_(cur)
        Database.conn.commit()
        cur.close()

    def storeDataFile(self, FileData):
        """Accepts a FileData object and adds the file to the DataFiles Table"""
        print(f"Adding {FileData.filename} to the database...")
        cur = Database.conn.cursor()

        # Add FilePath to Datafiles
        filepath = os.path.abspath(FileData.filename)
        cur.execute('''INSERT OR IGNORE INTO DataFiles (filepath) VALUES ( ? )''',(filepath,))
        cur.execute('SELECT id FROM DataFiles WHERE filepath = ? ', (filepath,))
        datafiles_id =  cur.fetchone()[0]

        # Add dateadded to DataFiles and get foreign key
        cur.execute("INSERT OR IGNORE INTO Dates (date) VALUES (date())")
        cur.execute("SELECT id FROM Dates WHERE date = date()")
        dateadded_id =  cur.fetchone()[0]

        # Add unique Metadata filepath and get foreign key for FileData table
        cur.execute("INSERT OR IGNORE INTO Metadata (origfilepath) VALUES ( ? )", (FileData.metadata['file_name'],))
        cur.execute("SELECT id FROM Metadata WHERE origfilepath = ?", (FileData.metadata['file_name'],))
        metadata_id = cur.fetchone()[0]

        # get startdate foreign keys
        cur.execute("INSERT OR IGNORE INTO Dates (date) VALUES ( ? )", (FileData.metadata['start_date'],))
        cur.execute("SELECT id FROM Dates WHERE date = ?", (FileData.metadata['start_date'],))
        startdate_id = cur.fetchone()[0]

        # get enddate foreign key
        cur.execute("INSERT OR IGNORE INTO Dates (date) VALUES ( ? )", (FileData.metadata['end_date'],))
        cur.execute("SELECT id FROM Dates WHERE date = ?", (FileData.metadata['end_date'],))
        enddate_id = cur.fetchone()[0]

        # get subject_id foreign key
        cur.execute("INSERT OR IGNORE INTO Subjects (subject) VALUES ( ? )", (FileData.metadata['rat_id'],))
        cur.execute("SELECT id FROM Subjects WHERE subject = ?", (FileData.metadata['rat_id'],))
        subject_id = cur.fetchone()[0]

        # get starttime_id foreign key
        cur.execute("INSERT OR IGNORE INTO Times (time) VALUES ( ? )", (FileData.metadata['start_time'],))
        cur.execute("SELECT id FROM Times WHERE time = ?", (FileData.metadata['start_time'],))
        starttime_id = cur.fetchone()[0]

        # get endtime_id foreign key
        cur.execute("INSERT OR IGNORE INTO Times (time) VALUES ( ? )", (FileData.metadata['end_time'],))
        cur.execute("SELECT id FROM Times WHERE time = ?", (FileData.metadata['end_time'],))
        endtime_id = cur.fetchone()[0]

        # get program_id foreign key
        cur.execute("INSERT OR IGNORE INTO Programs (program, datatablename) VALUES (?, ?)", (FileData.metadata['program'], FileData.dtname))
        cur.execute("SELECT id, datatablename FROM Programs WHERE program = ?", (FileData.metadata['program'],))
        program_id, datatablename = cur.fetchone()

        cur.execute("""UPDATE DataFiles 
                        SET 
                            dateadded_id = ?, 
                            metadata_id = ?,
                            datatablename = ?,
                            program_id = ?
                        WHERE 
                            id = ?
        """,(dateadded_id, metadata_id, datatablename, program_id, datafiles_id))

        cur.execute("""UPDATE MetaData 
                        SET 
                            startdate_id = ?, 
                            enddate_id = ?,
                            subject_id = ?,
                            box = ?,
                            starttime_id = ?,
                            endtime_id = ?,
                            program_id = ?
                        WHERE 
                            id = ?
        """, (startdate_id, enddate_id, subject_id, FileData.metadata['box'], starttime_id, endtime_id, program_id, metadata_id))

        self._store_datatables_(FileData)
        Database.conn.commit()
       
        cur.close()

# i want to set the groups
# i have the date, the subject and the group
# i got the date id to scan datafiles for the correct files
# i should now find the subject in the subject table then search 
#           the metadata files found for the right subject

# handle TypeError when looking through datafile and finding a subject_id that doesn't exist in the database

    
    def set_groups(self):
        configuration_file_path = 'maderp_settings.ini'
        cur = db.conn.cursor()
        try:
            config_file = open(configuration_file_path, 'r')
        except OSError:
            print("Could not locate the configuration file")
        lines = config_file.readlines()
        config_file.close()
        if not lines:
            raise TypeError("Could not read configuration file")

        groups = {}
        i = 0
        for line in lines:
            line = line.rstrip()
            if i == 0:
                date = line
                i+=1
                continue
            words = line.split(' = ')
            if '#' in words[0]: continue        # '#' at the start of a line as a simple way to distinguish a commented out line. This will cufrrently cause a bug if it appears after '=' in the config file
            group = words[0]
            subjects = words[1].split(',')
            for subject in subjects:
                groups[subject] = group
        print(f"groups: {groups}")
        cur.execute("SELECT id FROM Dates WHERE date = ?", (date,)) # get date_id from Dates
        result = cur.fetchone()
        print(f"result: {result}")
        date_id = result[0]
        print(f"date_id: {date_id}")
        for key, value in groups.items():
            print(f"Key: {key} Value: {value}")
            cur.execute('SELECT id FROM Subjects WHERE subject = ?', ((key),))
            sub_id = cur.fetchone()[0]
            cur.execute('UPDATE Metadata SET groups = ? WHERE subject_id = ? AND startdate_id = ?', (value, sub_id, date_id))
        Database.conn.commit()
        cur.close()


    
    def _store_datatables_(self, FileData):
        """Stores data from the FileData parameter into the database"""
        """Data stored in the database will not be able to be overridden unless the entry is deleted"""
        data_table = FileData.dtname                #   get table name where data is to be stored
        logical_key = os.path.abspath(FileData.filename)  # get logical key from filename
        cur = Database.conn.cursor()
        cur.execute("SELECT id from DataFiles WHERE filepath = ?",(logical_key,))
        datafile_id = cur.fetchone()[0]
        self._store_cvars_(FileData, datafile_id)
        self._store_dvars_(FileData, datafile_id)


    def _store_cvars_(self, FileData, fk):
        """unpacks cvars from FileData and stores them into the database"""
        """Also stores the cvar foreign key"""
        cur = Database.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO FRcVars (datafile_id) VALUES (?)", (fk,))
        FileData.cvars_id = cur.lastrowid
        cur.execute("UPDATE DataFiles SET cvars_id = ? WHERE id = ?", (FileData.cvars_id, fk))
        for key, value in FileData.cvars.items():
            sql = f"UPDATE FRcVars SET {key} = {value} WHERE id = {fk}"
            cur.execute(sql)
        cur.close()


    def _store_dvars_(self, FileData, fk):
        """unpacks cvars from FileData and stores them into the database"""
        """Also stores the dvar foreign key"""
        cur = Database.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO FRdVars (datafile_id) VALUES (?)", (fk,))
        FileData.dvars_id = cur.lastrowid
        cur.execute("UPDATE DataFiles SET dvars_id = ? WHERE id = ?", (FileData.dvars_id, fk))
        for key, value in FileData.dvars.items():
            sql = f"UPDATE FRdVars SET {key} = {value} WHERE id = {fk}"
            cur.execute(sql)
        cur.close()


    def _lookup_id_(self, column, key, table_name):
        """Retrieves foreign key from specified table"""
        sql = "SELECT id FROM ? WHERE ? = ?"
        params = (table_name, column, key)
        cur = Database.conn.cursor()
        cur.execute(sql,params)
        i = cur.fetchone()[0]
        return i


class FileNotFound(Exception):
    pass


if __name__ == "__main__":
    db = Database("DoctorG.db")
    db._testing_()
    i = 0
    files = []
    listy = os.listdir('data/')
    for each in range(len(listy)):      # import all files in dir as datafiles and add their data to db
        a = FR('data/'+listy[i])
        files.append(a)
        db.storeDataFile(a)
        i+=1
    print(files)
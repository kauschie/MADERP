import sqlite3
from Extraction import FRFileData as FR

class Database:
    conn = None

    def __init__(self):
        """Creates a connection to the main DoctorG.db and 
            returns a cursor to execute commands"""
        if not Database.conn:
            try:
                print('Enter the filepath for the databse')
                DBQuery = input('Press return to use default "DoctorG.db":')
                if len(DBQuery)<1:
                    DBQuery = 'DoctorG.db'
                Database.conn = sqlite3.connect(DBQuery)
                print(f"Connection to {DBQuery} established")
            except:
                print(f"Could not connect to {DBQuery}")
                quit()
        else:
            print("Connection to DoctorG.db already established")
            print("Query for a cursor to the sqlite database...")
    
    def _erase_all_tables_(self, cursor):
        """Erases all tables. This should only be used
        for testing purposes which is why i made it an internal"""
        cursor.executescript('''
        DROP TABLE IF EXISTS DataFiles;
        DROP TABLE IF EXISTS Dates;
        DROP TABLE IF EXISTS Metadata;
        DROP TABLE IF EXISTS Programs;
        DROP TABLE IF EXISTS Subjects;
        DROP TABLE IF EXISTS Times;  
        ''')
    
    def _create_all_tables_(self, cursor):
        """Creates all tables. This should only be used during testing"""
        cursor.executescript('''
        CREATE TABLE "DataFiles" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            "FilePath" TEXT, 
            "DateAdded_id" INTEGER, 
            "Metadata_id" INTEGER, 
            "Program_id" INTEGER,
            "DataTableName_id" INTEGER,
        )

        CREATE TABLE "Dates" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            "date" TEXT,
        )

        CREATE TABLE "Programs" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            "program" TEXT UNIQUE,
            "data_table_name" TEXT,
        )

        CREATE TABLE "Subjects" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            "subject" TEXT,
        )

        CREATE TABLE "Times" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
            "time" TEXT,
        )

        CREATE TABLE "Metadata" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            "OrigFilePath" TEXT UNIQUE,
            "startdate_id" INTEGER,
            "enddate_id" INTEGER,
            "subject_id" INTEGER,
            "box" INTEGER,
            "starttime_id" INTEGER,
            "endtime_id" INTEGER,
            "program_id" INTEGER,
        )

        ''')


if __name__ == "__main__":
    db = Database()


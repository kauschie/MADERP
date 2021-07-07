from Extraction import FRFileData as FR
from database import Database
import pandas as pd
from datetime import datetime

class QuerySelector():
    pass



class DateQuery:
    """Querys Data from DoctorG.db based on the specified date when initialized
    date is first format checked 
    
    
    
    """
    db = Database("DoctorG.db")


    def __init__(self, date):
        self.date = date
        self._get_groups_()
        self._check_date_()
        # self._get_file_list_()
        self._get_data_()
        # Output headings
        # self.line1 = ["Dr. Amy Gancarz-Kausch's lab", 'Date:', date]
        # self.line2 = []
    

    ## ToDo: read config file and sort data by group
    def _get_groups_(self):
        with open('maderp_settings.ini', 'r') as config_file:
            lines = config_file.read()
            







# make a prompt beforehand that shows the subject_id's of the animals so that you can 
# Utilizing the pandas library, SQL query is performed and returned in a DataFrame structure
# columns provides the headers for the data that is selected from DoctorG.db
# 


    def _get_cvars_(self):
        columns = ["Subjects", "Box" ,"Active Side", "FR", "Rewards", "Pump Duration", "Stimulus Duration", "Time Out Duration", "Cue Type"]
        SQL_Query = pd.read_sql_query(
            f"""SELECT Subjects.subject, 
                    Metadata.box, 
                    FRcVars.active_side,
                    FRcVars.fr,
                    FRcVars.max_rewards,
                    FRcVars.pump_dur,
                    FRcVars.light_dur,
                    FRcVars.to_dur,
                    FRcVars.cue_type
                FROM 
                    Subjects JOIN Metadata JOIN DataFiles JOIN FRcVars
                ON 
                    Subjects.id = Metadata.subject_id
                    AND Metadata.id = DataFiles.metadata_id
                    AND DataFiles.id = FRcVars.datafile_id
                WHERE
                    Metadata.startdate_id = {self.date_id}
                ORDER BY
                    FRcVars.active_side ASC,
                    Subjects.subject ASC""", DateQuery.db.conn)
        df = pd.DataFrame(SQL_Query) # SQL query is returned in a DataFrame
        df.set_axis(columns, inplace=True, axis=1)  # changes column headings
        print(df)
    # store df for writing to csv for later
    def _get_data_(self):
        columns = ["Subjects", "Box" ,"Active Side", "FR", "Rewards", "Pump Duration", "Stimulus Duration", "Time Out Duration", "Cue Type"]
        SQL_Query = pd.read_sql_query(
            f"""SELECT Subjects.subject, 
                    Metadata.box, 
                    FRcVars.active_side,
                    FRcVars.fr,
                    FRcVars.max_rewards,
                    FRcVars.pump_dur,
                    FRcVars.light_dur,
                    FRcVars.to_dur,
                    FRcVars.cue_type
                FROM 
                    Subjects JOIN Metadata JOIN DataFiles JOIN FRcVars
                ON 
                    Subjects.id = Metadata.subject_id
                    AND Metadata.id = DataFiles.metadata_id
                    AND DataFiles.id = FRcVars.datafile_id
                WHERE
                    Metadata.startdate_id = {self.date_id}
                ORDER BY
                    FRcVars.active_side ASC,
                    Subjects.subject ASC""", DateQuery.db.conn)
        df = pd.DataFrame(SQL_Query) # SQL query is returned in a DataFrame
        df.set_axis(columns, inplace=True, axis=1)  # changes column headings
        print(df)


    def _check_date_(self):
        try:
            datetime.strptime(self.date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        cur = DateQuery.db.conn.cursor()
        cur.execute("SELECT id FROM Dates WHERE date = ?",(self.date,))
        results1 = cur.fetchone()
        if results1:
            cur.execute("SELECT * FROM Metadata WHERE startdate_id = ? OR enddate_id = ?",(results1[0],results1[0]))
            results2 = cur.fetchone()
            if results2:
                self.date_id = results1[0]
                return True
            else:
                raise ValueError(f"Data was added on {self.date} but there are none found for that experimental date")
        else:
            raise ValueError(f"Could not locate {self.date} in the database")


# Commented out until feature is later added.

    # def _get_file_list_(self):
    #     """Used to retrieve a list of files for that date
    #     Later, the user can use this list to disclude any animals from the printout
    #     Perhaps separate them based on program run
    #     """
    #     # Get date_id
    #     cur = DateQuery.db.conn.cursor()
    #     cur.execute("SELECT id FROM Dates WHERE date = ?",(self.date,))
    #     self.date_id = cur.fetchone()[0]
    #     print(self.date_id)
    #     cur.execute("""SELECT 
    #                         Dates.date,
    #                         Subjects.subject,
    #                         Programs.program
    #                     FROM
    #                         Dates JOIN Subjects JOIN Programs JOIN Metadata
    #                     ON
    #                         Dates.id = Metadata.startdate_id
    #                         AND Subjects.id = Metadata.subject_id
    #                         AND Programs.id = Metadata.program_id
    #                     WHERE
    #                         Metadata.startdate_id = ?
    #                     ORDER BY
    #                         Programs.program ASC""",(self.date_id,))
    #     self.file_list = cur.fetchall()
    #     # print(self.file_list)
    #     for item in self.file_list:
    #         print(item)
    #     cur.close()









if __name__ == "__main__":
    q = DateQuery("2020-10-30")

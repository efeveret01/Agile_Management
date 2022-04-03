from numpy import record
import pandas as pd
import sqlite3
from datetime import date

class backend():
    def __init__(self):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()
        self.checkifTablesCreated()

    # CHECK IF TABLE IS CREATED
    def checkifTablesCreated(self):
        #get the count of tables with the name
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute(''' SELECT count(*) FROM sqlite_master WHERE type='table' AND name='projects'; ''')

        #if the count is 1, then table exists
        if self.c.fetchone()[0]==1 : 
            print('Table exists.')
            self.conn.commit()
            self.conn.close()
        else :
            print('Table does not exist. Creating table...')
            self.createcharts()

    # CREATE CHARTS AT THE START
    def createcharts(self):
        self.conn = sqlite3.connect("database/agile_framework.db")
        #c = self.conn.cursor()
        self.c = self.conn.cursor()

        self.c.execute("""          
        CREATE TABLE projects (
            project_id text,
            pro_name text,
            pro_dis text,
            sprodate text,
            eprodate text,
            procomp text
        )
        """)

        self.c.execute("""
        CREATE TABLE ProductItems (
            projitem_id text,
            prior text,
            prItemDisc text,
            proItStat text,
            pl_ids text
        )
        """)

        self.c.execute("""
        CREATE TABLE Sprints (
            spr_id text,
            spr_num text,
            spr_sdate text,
            spr_edate text,
            proj_ids text
        )
        """)

        self.c.execute("""
        CREATE TABLE SprintItems (
            spr_item_id text,
            items text,
            sprItemStatues text,
            spr_ids text,
            projitem_ids text
        )
        """)

        self.c.execute("""
        CREATE TABLE ProdSpriMeetings (
            psmeeting_id text,
            psmType text,
            psmdiscp text,
            psmsdate text,
            sprint_ids text
        )
        """)

        self.c.execute("""
        CREATE TABLE DailyMeetings (
            dailyM_id text,
            sections text,
            dmdates text,
            dmuser text,
            sprint_idsk text
        )
        """)
        
        self.conn.commit()
        self.conn.close()

    #################################################################################################
    # (1) FIND PROJECT WITH ID or GIVE NEW ID - FROM INPUT PROJECT POPUP 1
    #################################################################################################
    def getProjectIDForProjectInputPopup(self, primaryID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        records = ""

        if primaryID == "":
            #find new id
            self.c.execute("SELECT project_id FROM projects ORDER BY  CAST(project_id AS INTEGER) DESC")
            records = self.c.fetchall()
            if len(records) == 0:
                records = ["0", "", "", " / / ", " / / ", "", ""]
            else:
                newNum = str(int(records[0][0]) + 1)
                records = [newNum, "", "", " / / ", " / / ", "", ""]
        else:
            self.c.execute("SELECT * FROM projects WHERE project_id = '" + primaryID + "'")
            records = self.c.fetchall()
            records = records[0]
        
        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    #################################################################################################
    # (2) INSERT INTO PRODUCT TABLE - FROM INPUT PROJECT POPUP 2
    #################################################################################################
    def addProjectsToDatabase(self, primaryID, name, discription, startDate, endDate):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("INSERT INTO projects VALUES (:project_id, :pro_name, :pro_dis, :sprodate, :eprodate, :procomp)",
            {
                'project_id': "" + primaryID + "",
                'pro_name': "" + name + "",
                'pro_dis': "" + discription + "",
                'sprodate': "" + startDate + "",
                'eprodate': "" + endDate + "",
                'procomp': "a"
            })
        
        self.conn.commit()
        self.conn.close()

    #################################################################################################
    #################################################################################################
    # (3) GET PROJECTS - FROM STARTING PAGE 1
    #################################################################################################
    def getAllProjects(self):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT * FROM projects")
        records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    #################################################################################################
    # (4) GET LATAST OR DESIRED SPRINT, OR CREATE NEW SPRINT - FROM SPRINT PAGE 1 (ALSO GOOD FOR NEXT SPRINT BUTTON, JUST MAKE YOU TO HAVE THE NEXT SPRINT NUMBER AS THEN SPRINTNUM)
    #################################################################################################
    def getDesiredSprint(self, projectID, sprintNum):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        today = date.today()
        today = today.strftime("%d/%m/%Y")
        maxSprintCount = ""
        spr_id = ""

        self.c.execute("SELECT * FROM Sprints WHERE proj_ids ='" + projectID + "' ORDER BY CAST(spr_num AS INTEGER) DESC")
        records = self.c.fetchall()

        if sprintNum == "": #The "" would create a newly starterd sprint PLUS THE OTHER OPTION IF YOU MOVE TO THE NEXT SPRINT HAVE 

            #NEW AND NO SPRINTS
            if len(records) == 0:
                self.c.execute("SELECT * FROM Sprints ORDER BY CAST(spr_id AS INTEGER) DESC")
                firstPart = self.c.fetchall()

                if len(firstPart) ==  0:
                    self.c.execute("INSERT INTO Sprints VALUES (:spr_id, :spr_num, :spr_sdate, :spr_edate, :proj_ids)",
                        {
                            'spr_id': "0",
                            'spr_num': "1",
                            'spr_sdate': "" + today + "",
                            'spr_edate': "" + today + "",
                            'proj_ids': "" + projectID + ""
                        })
                    maxSprintCount = "1"
                    spr_id = "0"
                else:
                    newID = str( int(firstPart[0][0]) + 1 )
                    self.c.execute("INSERT INTO Sprints VALUES (:spr_id, :spr_num, :spr_sdate, :spr_edate, :proj_ids)",
                        {
                            'spr_id': "" + newID + "",
                            'spr_num': "1",
                            'spr_sdate': "" + today + "",
                            'spr_edate': "" + today + "",
                            'proj_ids': "" + projectID + ""
                        })

                    maxSprintCount = "1"
                    spr_id = newID

            else:
                maxSprintCount = records[0][1]
                spr_id = records[0][0]

        else:
            checker = False
            for x in range(len(records)):
                    if records[x][1] == sprintNum:
                        spr_id = records[x][0]
                        checker = True
                    maxSprintCount = records[0][1]
                        

            if checker == False:
                newID = str( int(records[0][0]) + 1 )
                newmMaxNum = str( int(records[0][1]) + 1 )
                self.c.execute("INSERT INTO Sprints VALUES (:spr_id, :spr_num, :spr_sdate, :spr_edate, :proj_ids)",
                    {
                        'spr_id': "" + newID + "",
                        'spr_num': "" + newmMaxNum + "",
                        'spr_sdate': "" + today + "",
                        'spr_edate': "" + today + "",
                        'proj_ids': "" + projectID + ""
                    })
                spr_id = newID
                maxSprintCount = newmMaxNum

        self.conn.commit()
        self.conn.close()

        return maxSprintCount, spr_id

    #################################################################################################
    #################################################################################################
    # (5) UPDATE THE PROJECT TABLE WITH INPUTS - FROM INPUT PROJECT POPUP 1
    #################################################################################################
    def updateProjectTable(self, primaryID, name, discription, startDate, endDate):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("UPDATE projects SET  pro_name = '" + name + "', pro_dis = '" + discription + "', sprodate = '" + startDate + "', eprodate = '" + endDate + "'  WHERE project_id = '" + primaryID + "'")

        self.conn.commit()
        self.conn.close()

    #################################################################################################
    #################################################################################################
    # (6) UPDATE PROJECT AS COMPLETED - FROM SPRINT PAGE 1
    #################################################################################################
    def completeTheProject(self, primaryID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("UPDATE projects SET  procomp = 'c'  WHERE project_id = '" + primaryID + "'")

        self.conn.commit()
        self.conn.close()
    
    #################################################################################################
    #################################################################################################
    # (7) GET NEXT PRODUCT ITEM ID AND PRIORITIES - FROM PRODUCT BACKLOG PAGE 1
    #################################################################################################
    def getNewProjectBacklogItemsIDs(self, projectItemID, projectID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        records = ""

        if projectItemID == "":
            #find new id
            self.c.execute("SELECT projitem_id FROM ProductItems ORDER BY  CAST(projitem_id AS INTEGER) DESC")
            records = self.c.fetchall()
            if len(records) == 0:
                records = ["0", "1", "", "", projectID]
            else:
                newNum = str(int(records[0][0]) + 1)
                
                self.c.execute("SELECT * FROM ProductItems WHERE pl_ids = '" + projectID +"' ORDER BY  CAST(prior AS INTEGER) DESC")
                records01 = self.c.fetchall()
                if len(records01) == 0:
                    records = [newNum, "1", "", "", projectID]
                else:
                    newPriority = str(int(records01[0][1]) + 1)
                    records = [newNum, newPriority, "", "", projectID]
        else:
            self.c.execute("SELECT * FROM ProductItems WHERE projitem_id = '" + projectItemID + "'")
            records = self.c.fetchall()
            records = records[0]
        
        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    #################################################################################################
    # (8) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def updateProductLogItemTable(self, nextID, prioriy, disc, state, pid, option):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()
        if option == 0:
            self.c.execute("INSERT INTO ProductItems VALUES (:projitem_id, :prior, :prItemDisc, :proItStat, :pl_ids)",
                {
                    'projitem_id': "" + nextID + "",
                    'prior': "" + prioriy + "",
                    'prItemDisc': "" + disc + "",
                    'proItStat': "" + state + "",
                    'pl_ids': "" + pid + ""
                })
        else:
            self.c.execute("UPDATE ProductItems SET  prior = '" + prioriy + "', prItemDisc = '" + disc + "', proItStat = '" + state + "' WHERE projitem_id = '" + nextID + "'")
            pass

        checker = True
        IDHolder = nextID

        while checker:
            self.c.execute("SELECT * FROM ProductItems WHERE pl_ids = '" + pid + "' AND prior = '" + prioriy + "'")
            lookAtRows =  self.c.fetchall()
            
            if len(lookAtRows) <= 1:
                break
            else:
                tempHolder = ""
                for row in lookAtRows:
                    if row[0] != IDHolder:
                        tempHolder = row[0]
                        prioriy = int(prioriy) + 1
                        prioriy = str(prioriy)
                        self.c.execute("UPDATE ProductItems SET  prior = '" + prioriy + "' WHERE projitem_id = '" + row[0] + "'")
                IDHolder = tempHolder

        self.conn.commit()
        self.conn.close()

    #################################################################################################
    # (9) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def getGetMeetingLogInputPopup(self,type, meetingID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        if type == "DMLogs":
            if meetingID == "":

                self.c.execute("SELECT dailyM_id FROM DailyMeetings ORDER BY CAST(dailyM_id AS INTEGER) DESC")
                record =  self.c.fetchall()

                if len(record) == 0:
                    record = ["0", "", "", "", ""]
                else:
                    nextID = str( int(record[0][0]) + 1 )
                    record = [nextID, "", "", "", ""]
                pass
            else:
                self.c.execute("SELECT * FROM DailyMeetings WHERE dailyM_id = '" + meetingID + "'")
                record =  self.c.fetchall()
                record = record[0]
                pass
            pass
        else: # if sprint or product meeting
            if meetingID == "":
                self.c.execute("SELECT psmeeting_id FROM ProdSpriMeetings ORDER BY CAST(psmeeting_id AS INTEGER) DESC")
                record =  self.c.fetchall()

                if len(record) == 0:
                    record = ["0", "", "", "", ""]
                else:
                    nextID = str( int(record[0][0]) + 1 )
                    record = [nextID, "", "", "", ""]
                pass
            else:
                self.c.execute("SELECT * FROM ProdSpriMeetings WHERE psmeeting_id = '" + meetingID + "'")
                record =  self.c.fetchall()
                record = record[0]

        self.conn.commit()
        self.conn.close()

        return record
        
    #################################################################################################
    # (10) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def updateMeetingLogsTable(self, meeintingID, type, dates, user, discption, sprintID, addOrUpdate):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        if type == "Daily Meeting":
            if addOrUpdate == 0:
                self.c.execute("INSERT INTO DailyMeetings VALUES (:dailyM_id, :sections, :dmdates, :dmuser, :sprint_idsk)",
                {
                    'dailyM_id': "" + meeintingID + "",
                    'sections': "" + discption + "",
                    'dmdates': "" + dates + "",
                    'dmuser': "" + user + "",
                    'sprint_idsk': "" + sprintID + ""
                })
            else:
                #update
                self.c.execute("UPDATE DailyMeetings SET  sections = '" + discption + "', dmdates = '" + dates + "', dmuser = '" + user + "' WHERE dailyM_id = '" + meeintingID + "'")
                pass
        else:
            if addOrUpdate == 0:
                self.c.execute("INSERT INTO ProdSpriMeetings VALUES (:psmeeting_id, :psmType, :psmdiscp, :psmsdate,  :sprint_ids)",
                {
                    'psmeeting_id': "" + meeintingID + "",
                    'psmType': "" + type + "",
                    'psmdiscp': "" + discption + "",
                    'psmsdate': "" + dates + "",
                    'sprint_ids': "" + sprintID + ""
                })
            else:
                #update
                self.c.execute("UPDATE ProdSpriMeetings SET  psmType = '" + type + "', psmdiscp = '" + discption + "', psmsdate = '" + dates + "' WHERE psmeeting_id = '" + meeintingID + "'")


        self.conn.commit()
        self.conn.close()

    #################################################################################################
    # (11) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def sprintMeetings(self, sprintID, type):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()
            
        if type == "DMLogs":
            self.c.execute("SELECT * FROM DailyMeetings WHERE sprint_idsk = '" + sprintID + "'")
        else:
            self.c.execute("SELECT * FROM ProdSpriMeetings WHERE sprint_ids = '" + sprintID + "'")
            pass

        record =  self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        return record
        
    #################################################################################################
    # (12) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def addOrUpdateTheSprintItem(self, sprintItemID, item, statues, sprintID, prodoctItemID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        if sprintItemID == "":
            self.c.execute("SELECT spr_item_id FROM SprintItems ORDER BY CAST(spr_item_id AS INTEGER) DESC")
            record =  self.c.fetchall()

            if len(record) == 0:
                 self.c.execute("INSERT INTO SprintItems VALUES (:spr_item_id, :items, :sprItemStatues, :spr_ids, :projitem_ids)",
                    {
                        'spr_item_id': "0",
                        'items': "" + item + "",
                        'sprItemStatues': "" + statues + "",
                        'spr_ids': "" + sprintID + "",
                        'projitem_ids': "" + prodoctItemID + ""
                    })
            else:
                nextID = str( int(record[0][0]) + 1 )

                self.c.execute("INSERT INTO SprintItems VALUES (:spr_item_id, :items, :sprItemStatues, :spr_ids, :projitem_ids)",
                    {
                        'spr_item_id': "" + nextID + "",
                        'items': "" + item + "",
                        'sprItemStatues': "" + statues + "",
                        'spr_ids': "" + sprintID + "",
                        'projitem_ids': "" + prodoctItemID + ""
                    })

        else:
            self.c.execute("UPDATE SprintItems SET  items = '" + item + "', sprItemStatues = '" + statues + "' WHERE spr_item_id = '" + sprintItemID + "'")
            pass
    
        self.conn.commit()
        self.conn.close()

    #################################################################################################
    # (13) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def populateTheSprintItemInputSecondTable(self, prodoctItemID, sprintID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT *  FROM SprintItems WHERE projitem_ids = '" + prodoctItemID + "' AND spr_ids = '" + sprintID + "'")
        records =  self.c.fetchall()
        self.conn.commit()
        self.conn.close()
        
        return records

    #################################################################################################
    # (14) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def populateSprintItemTablePage(self, sprintID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT spr_item_id, prItemDisc, items, sprItemStatues  FROM ProductItems, SprintItems WHERE projitem_id = projitem_ids AND spr_ids = '" + sprintID + "'")
        records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    # (15) INSERT/UPDATE PRODUCT ITEM LIST - FROM PRODUCT BACKLOG PAGE 2
    #################################################################################################
    def getTheSprintItemRecords(self, sprintItemID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT items, sprItemStatues FROM SprintItems WHERE spr_item_id = '" + sprintItemID + "'")
        if sprintItemID == "":
            records = ["","Not Started"]
        else:
            records = self.c.fetchall()
            records = records[0]

        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    def populateProductBacklogTablePage(self, projectID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT projitem_id, prior, prItemDisc, proItStat  FROM ProductItems WHERE pl_ids = '" + projectID + "' ORDER BY  CAST(prior AS INTEGER) ASC")
        records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    def populateMeetinglogTablePage(self, sprintID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT psmeeting_id, psmsdate, psmType, psmdiscp, dailyM_id, dmdates, dmuser, sections  FROM ProductItems WHERE sprint_ids = sprint_idsk AND sprint_ids = '" + sprintID + "'")
        records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    def populateSprintItemTopPopupBox(self, projectID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT projitem_id, prItemDisc FROM ProductItems WHERE pl_ids = '" + projectID + "'")
        records = self.c.fetchall()


        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    def populateSprintItemButtomPopupBox(self, sprintID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT spr_item_id, items FROM SprintItems WHERE pl_ids = '" + sprintID + "'")
        records = self.c.fetchall()

        self.conn.commit()
        self.conn.close()

        return records

    #################################################################################################
    def viewAll(self, tablename):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT * FROM " + tablename + "")
        records = self.c.fetchall()
        print(records)

        self.conn.commit()
        self.conn.close()
        pass

    #################################################################################################
    def clearOneWholeProject(self, projectID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("SELECT spr_id  FROM projects, Sprints WHERE project_id = proj_ids AND project_id = '" + projectID + "'")
        records = self.c.fetchall()
        
        if len(records) != 0:
            for x in range(len(records)):
                self.c.execute("DELETE FROM DailyMeetings WHERE sprint_idsk = '" + records[x][0] + "'")
                self.c.execute("DELETE FROM ProdSpriMeetings WHERE sprint_ids = '" + records[x][0] + "'")

                self.c.execute("DELETE FROM SprintItems WHERE spr_ids = '" + records[x][0] + "'")
                self.c.execute("DELETE FROM Sprints WHERE spr_id = '" + records[x][0] + "'")

        self.c.execute("DELETE FROM ProductItems WHERE pl_ids = '" + projectID + "'")
        self.c.execute("DELETE FROM projects WHERE project_id = '" + projectID + "'")

        self.conn.commit()
        self.conn.close()

    #################################################################################################
    def deleteSpecificSprintItem(self, sprintItemID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("DELETE FROM SprintItems WHERE spr_item_id = '" + sprintItemID + "'")

        self.conn.commit()
        self.conn.close()

    #################################################################################################
    def deleteSpecificProjectBacklog(self, projectItemID):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        self.c.execute("DELETE FROM ProductItems WHERE projitem_id = '" + projectItemID + "'")

        self.conn.commit()
        self.conn.close()

    #################################################################################################
    def deleteSpecificMeetingLog(self, tempID, tableOption):
        self.conn = sqlite3.connect("database/agile_framework.db")
        self.c = self.conn.cursor()

        if tableOption == "Daily Meeting":
            self.c.execute("DELETE FROM DailyMeetings WHERE dailyM_id = '" + tempID + "'")
        else:
            self.c.execute("DELETE FROM ProdSpriMeetings WHERE psmeeting_id = '" + tempID + "'")

        self.conn.commit()
        self.conn.close()

   
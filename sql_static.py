DB_PATH = 'serverbot.db'
#
#
CREATE_SERVER_TABLE = """CREATE TABLE IF NOT EXISTS ServerTable 
                        (ServerId INTEGER PRIMARY KEY AUTOINCREMENT, 
                        Title TEXT, 
                        Ip INTEGER,
                        Login TEXT,
                        Password TEXT,
                        Port INTEGER,
                        Ssh TEXT)"""
DROP_SERVER_TABLE = """DROP TABLE IF EXISTS ServerTable"""
#
INSERT_SERVER_TABLE = """INSERT INTO ServerTable(Title, Ip, Login, Password, Port, Ssh) VALUES(?, ?, ?, ?, ?, ?)"""
GET_SERVER_ID = """SELECT ServerId FROM  ServerTable WHERE Title == ?"""
#
#
CREATE_PERIOD_OF_ACTION = """CREATE TABLE IF NOT EXISTS Period_Of_Action 
                            (PeriodId INTEGER PRIMARY KEY AUTOINCREMENT,
                             ServerId INTEGER,
                             ServerUrl TEXT,
                             StartDate DATE,
                             EndDate DATE,
                             Price INTEGER,
                             FOREIGN KEY (ServerId) REFERENCES ServerTable (ServerId))"""
#
INSERT_PERIOD_OF_ACTION = """INSERT INTO Period_Of_Action(ServerId, ServerUrl, StartDate, EndDate, Price) 
                            VALUES(?, ?, ?, ?, ?)"""
DROP_PERIOD_OF_ACTION = """DROP TABLE IF EXISTS Period_Of_Action"""
#
#
GET_ALL_INFO = """SELECT ServerTable.Title, ServerTable.Ip, ServerTable.Login, ServerTable.Password, 
                         ServerTable.Port, ServerTable.Ssh, 
                         Period_Of_Action.ServerUrl, Period_Of_Action.StartDate, Period_Of_Action.EndDate, 
                         Period_Of_Action.Price
                  FROM ServerTable 
                  JOIN Period_Of_Action 
                  ON ServerTable.ServerId == Period_Of_Action.ServerId"""
#
GET_BY_TITLE = """SELECT ServerTable.Title, ServerTable.Ip, ServerTable.Login, ServerTable.Password, 
                         ServerTable.Port, ServerTable.Ssh, 
                         Period_Of_Action.ServerUrl, Period_Of_Action.StartDate, Period_Of_Action.EndDate, 
                         Period_Of_Action.Price
                  FROM ServerTable 
                  JOIN Period_Of_Action 
                  ON ServerTable.ServerId == Period_Of_Action.ServerId AND ServerTable.Title == ?"""
#
GET_BY_IP = """SELECT ServerTable.Title, ServerTable.Ip, ServerTable.Login, ServerTable.Password, 
                         ServerTable.Port, ServerTable.Ssh, 
                         Period_Of_Action.ServerUrl, Period_Of_Action.StartDate, Period_Of_Action.EndDate, 
                         Period_Of_Action.Price
                  FROM ServerTable 
                  JOIN Period_Of_Action 
                  ON ServerTable.ServerId == Period_Of_Action.ServerId AND ServerTable.Ip == ?"""

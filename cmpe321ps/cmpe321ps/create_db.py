import mysql.connector
import environ

env = environ.Env()
environ.Env.read_env()

connection = mysql.connector.connect(
  host=env("MYSQL_HOST"),
  user=env("MYSQL_USER"),
  password=env("MYSQL_PASSWORD"),
  database=env("MYSQL_DATABASE"),
  auth_plugin='mysql_native_password'
)

cursor= connection.cursor()
#Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
username varchar(200) PRIMARY KEY,
password TEXT NOT NULL
);""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Post (
title TEXT NOT NULL,
body TEXT NOT NULL,
poster varchar(200),
FOREIGN KEY(poster) REFERENCES User(username) ON UPDATE CASCADE ON DELETE CASCADE
);""")

#Create the trigger for limiting 5 posts per user
cursor.execute("""
CREATE TRIGGER PostInsert
BEFORE INSERT ON Post
FOR EACH ROW
BEGIN
    IF ( SELECT COUNT(*) FROM Post  WHERE poster = new.poster GROUP BY poster) = 5 THEN 
    SIGNAL SQLSTATE '45000';
    END IF;
END;""")

#Create a stored procedure
cursor.execute("""
CREATE PROCEDURE CreatePost(IN title TEXT, IN body TEXT, IN poster VARCHAR(200))
BEGIN
INSERT INTO Post VALUES (title,body,poster);
END;

""")
connection.commit()

cursor.execute('INSERT INTO User VALUES ("berke.argin","123abc");')
cursor.execute('INSERT INTO User VALUES ("niyazi.ulke","password");')
cursor.execute('INSERT INTO Post VALUES ("Post1","Post 1 of berke.argin","berke.argin");')
cursor.execute('INSERT INTO Post VALUES ("Post2","Post 2 of berke.argin","berke.argin");')
cursor.execute('INSERT INTO Post VALUES ("Post3","Post 3 of berke.argin","berke.argin");')

connection.commit()
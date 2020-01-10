from datetime import datetime
lst = []
nowja = datetime.now()
while True:
    s = input()
    if (s == ''):
        now = datetime.now()
        thetime = (nowja-now)
        lst.append(thetime)
    else:
        break




















##import sqlite3
##username = "Toonkung"
##selectedSong = 2
##score = 100
##
##conn = sqlite3.connect('highScore.db')
##print ("Opened database successfully")
##
##cursor = conn.execute("SELECT highScore1, highScore2, highScore3, highScore4, highScore5 from highScore where key = "+str(selectedSong))
##for row in cursor:
##    if score >= row[4]:
##        if score >= row[0]:
##            sql_update_query = "Update highScore set nameScore1 = '"+username+"', highScore1 = "+str(score)+" where key = " + str(selectedSong)
##        elif score >= row[1]:
##            sql_update_query = "Update highScore set nameScore2 = '"+username+"', highScore2 = "+str(score)+" where key = " + str(selectedSong)
##        elif score >= row[2]:
##            sql_update_query = "Update highScore set nameScore3 = '"+username+"', highScore3 = "+str(score)+" where key = " + str(selectedSong)
##        elif score >= row[3]:
##            sql_update_query = "Update highScore set nameScore4 = '"+username+"', highScore4 = "+str(score)+" where key = " + str(selectedSong)
##        elif score >= row[4]:
##            sql_update_query = "Update highScore set nameScore5 = '"+username+"', highScore5 = "+str(score)+" where key = " + str(selectedSong)
##
##        cursor.execute(sql_update_query)
##        conn.commit()
##        print("Record Updated successfully ")
##conn.close()
##
##
##
##conn = sqlite3.connect('highScore.db')
##print ("Opened database successfully")
##cursor = conn.execute("SELECT song, nameScore1, highScore1, nameScore2, highScore2, nameScore3, highScore3, nameScore4, highScore4 from highScore where key = "+str(selectedSong))
##for row in cursor:
##   s1 = 
##   s2 =
##   s3 =
##   s4 =
##   s5 =
##
##print ("Operation done successfully")
##conn.close()

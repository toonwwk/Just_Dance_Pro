conn = sqlite3.connect('highScore.db')
                print("Opened database successfully")
                cursor = conn.execute(
                    "SELECT highScore1, highScore2, highScore3, highScore4, highScore5 from highScore where key = " + str(
                        selectedSong))
                for row in cursor:
                    if score >= row[4]:
                        if score >= row[0]:
                            sql_update_query = "Update highScore set nameScore1 = '" + username + "', highScore1 = " + str(
                                score) + " where key = " + str(selectedSong)
                            temp = 0
                        elif score >= row[1]:
                            sql_update_query = "Update highScore set nameScore2 = '" + username + "', highScore2 = " + str(
                                score) + " where key = " + str(selectedSong)
                            temp = 1
                        elif score >= row[2]:
                            sql_update_query = "Update highScore set nameScore3 = '" + username + "', highScore3 = " + str(
                                score) + " where key = " + str(selectedSong)
                            temp = 2
                        elif score >= row[3]:
                            sql_update_query = "Update highScore set nameScore4 = '" + username + "', highScore4 = " + str(
                                score) + " where key = " + str(selectedSong)
                            temp = 3
                        elif score >= row[4]:
                            sql_update_query = "Update highScore set nameScore5 = '" + username + "', highScore5 = " + str(
                                score) + " where key = " + str(selectedSong)
                            temp = 4

                        cursor.execute(sql_update_query)
                        conn.commit()
                        print("Record Updated successfully ")
                conn.close()

                conn = sqlite3.connect('highScore.db')
                print("Opened database successfully")
                cursor = conn.execute(
                    "SELECT nameScore1, highScore1, nameScore2, highScore2, nameScore3, highScore3, nameScore4, highScore4, nameScore5, highScore5 from highScore where key = " + str(
                        selectedSong))
                for row in cursor:
                    txt_surface1 = font.render(str(row[0]), True, [0, 0, 0])
                    txt_surface2 = font.render(str(row[2]), True, [0, 0, 0])
                    txt_surface3 = font.render(str(row[4]), True, [0, 0, 0])
                    txt_surface4 = font.render(str(row[6]), True, [0, 0, 0])
                    txt_surface5 = font.render(str(row[8]), True, [0, 0, 0])
                    txt_surface6 = font.render(str(row[1]), True, [0, 0, 0])
                    txt_surface7 = font.render(str(row[3]), True, [0, 0, 0])
                    txt_surface8 = font.render(str(row[5]), True, [0, 0, 0])
                    txt_surface9 = font.render(str(row[7]), True, [0, 0, 0])
                    txt_surface10 = font.render(str(row[9]), True, [0, 0, 0])

                conn.close()

                yPlus = 0
                j = 0
                for i in range(5):
                    if j == temp:
                        screen.blit(pygame.transform.scale(songSelected,
                                                           (round(width * 0.50364583), round(height * 0.09074074))),
                                    (width * 0.24791667, height * 0.24722222 + yPlus))
                    else:
                        screen.blit(
                            pygame.transform.scale(songSelect, (round(width * 0.50364583), round(height * 0.09074074))),
                            (width * 0.24791667, height * 0.24722222 + yPlus))
                    if j == 0:
                        screen.blit(txt_surface1, (width * 0.24791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                        screen.blit(txt_surface6, (width * 0.54791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                    elif j == 1:
                        screen.blit(txt_surface2, (width * 0.24791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                        screen.blit(txt_surface7, (width * 0.54791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                    elif j == 2:
                        screen.blit(txt_surface3, (width * 0.24791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                        screen.blit(txt_surface8, (width * 0.54791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                    elif j == 3:
                        screen.blit(txt_surface4,(width * 0.24791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                        screen.blit(txt_surface9, (width * 0.54791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                    elif j == 4:
                        screen.blit(txt_surface5,(width * 0.24791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                        screen.blit(txt_surface10, (width * 0.54791667 * 1.1, (height * 0.24722222 + yPlus) * 1.05))
                    j += 1
                    yPlus += height * 0.12962963

                pygame.display.flip()

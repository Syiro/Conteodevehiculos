import pyautogui as pg, time as tm

tm.sleep(4)
for i in range (80):

    pg.moveTo(188, 182,duration=1) #se mueve a esquina superior de la imagen
    pg.click()#clickea en ella

    
    pg.moveTo(1349,965,duration=1)#se mueve a la esquina inferior de la imagen
    pg.click()#clickea en ella
    
    
    pg.moveTo(1711,103,duration=2)#se mueve al boton de done
    pg.click() #click en el boton de done
    

    pg.moveTo(925,114,duration=2)#se mueve al boton de siguiente imagen
    pg.click()#click en el boton de siguiente imagen
    
    tm.sleep(3.5)
    

    pass
#Detección de Placas 
import cv2 
import numpy as np 
import os 
import pytesseract
from pytictoc import TicToc

lower_blue = np.array([90,105,0])
upper_blue = np.array([150,250,250])
kernel = np.ones((3,3),np.uint8)
try:
    for i, name in enumerate(os.listdir('data')):
        
        img = cv2.imread('data/'+name)
        img = cv2.resize(img,(400,200))
        
        original = np.copy(img)
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res = cv2.bitwise_and(img,img, mask= mask)  

        B = res[:,:,0]
        c=0
        ct=0

        for i in range (B.shape[0]):
            m = np.sum(B[i])/B.shape[1]
            if (m>=75):
                c+=m
                ct+=1

        if (ct==0):
            ct=1

        c=c/ct

        ret,B = cv2.threshold(B,int(c),255,cv2.THRESH_BINARY)
        aft = cv2.dilate(B,kernel,iterations = 1)
        
        high_m = 0
        width_m = 0 
        area = 0   
        extct = 0
        alt = []
        altos = []
        flag = np.copy(B)
        im,contornos, hierarchy=cv2.findContours(aft,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        for n,rect in enumerate((contornos)):
            
            (a,b,c,d) = cv2.boundingRect(rect)

            if (d>=30 and c<=80):

                alt.append(c) 
                altos.append(d)
                extct +=1

        alt = np.array(sorted(alt))
        altos = np.array(sorted(altos))
        med = []
        medw = []

        for i in range(altos.shape[0]):
            if (i>=5):
                media1 = int((altos[i-1]+altos[i])/2)
                media2 = int((altos[i-2]+altos[i-1]+altos[i])/3)
                media3 = int((altos[i-3]+altos[i-2]+altos[i-1]+altos[i])/4)
                media4 = int((altos[i-4]+altos[i-3]+altos[i-2]+altos[i-1]+altos[i])/5)
                media5 = int((altos[i-5]+altos[i-4]+altos[i-3]+altos[i-2]+altos[i-1]+altos[i])/6)
                if(media1-media2<=5):
                    if(media2-media3<=5):
                        if(media4-media4<=5):
                            if(media4-media5<=5):
                                media = int((media1+media2+media3+media4+media5)/5) 
                                med.append(media)


        for i in range(alt.shape[0]):
            if (i>=5):
                media1 = int((alt[i-1]+alt[i])/2)
                media2 = int((alt[i-2]+alt[i-1]+alt[i])/3)
                media3 = int((alt[i-3]+alt[i-2]+alt[i-1]+alt[i])/4)
                media4 = int((alt[i-4]+alt[i-3]+alt[i-2]+alt[i-1]+alt[i])/5)
                media5 = int((alt[i-5]+alt[i-4]+alt[i-3]+alt[i-2]+alt[i-1]+alt[i])/6)
                if(media1-media2<=5):
                    if(media2-media3<=5):
                        if(media4-media4<=5):
                            if(media4-media5<=5):
                                media = int((media1+media2+media3+media4+media5)/5) 
                                medw.append(media)

        med = np.array(med)
        medw = np.array(medw)

        tmed =  int((np.sum(med))/(med.shape[0]))   
        tmedw =  int((np.sum(medw))/(medw.shape[0]))  
        print("MEDIA")
        print(tmed)
        print(tmedw)
        print("************")

        L1=[]

        textstr = ""
        
        for n,rect in enumerate((contornos)):
            (a,b,c,d) = cv2.boundingRect(rect)
            if (d>=tmed-10 and d<=tmed+10 and c>=tmedw-30 and c<=tmedw+15):
                cv2.rectangle(img, (a, b), (a + c, b + d), (0, 255, 0), 5)

                crop_img = flag[b-10:b+d+10, a-5:a+c+5]
                cv2.imshow("crp",crop_img)
                cv2.waitKey()
                cv2.destroyAllWindows()
                
            
                text = pytesseract.image_to_string(crop_img, config='--psm 10')
                textstr +=text
                L1.append(i)
                print(text)

        print (textstr)
        cv2.imshow('B',B)
        cv2.imshow('hsv',res)
        cv2.imshow('aft',aft)
        cv2.imshow('ORIGINAL',img)

        cv2.waitKey()
        cv2.destroyAllWindows()

except Exception as e:
    print(str(e)) 
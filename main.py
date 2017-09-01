import numpy as np
import cv2;

cap  = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
Thres = 0;#150,200
Upper = 0;
Type = 0;
YellowLower = [0,160,160]
YellowUpper = [135,255,255]



def ThresChange(x):
    global Thres
    Thres = x
    pass

def UpperChange(x):
    global Upper
    Upper = x
    pass

def TypeChange(x):
    global Type
    Type = x
    pass


cv2.namedWindow("Frame")
cv2.createTrackbar("Thresh","Frame",Thres,250,ThresChange)
cv2.createTrackbar("Upper","Frame",Upper,250,UpperChange)
cv2.createTrackbar("Type","Frame",Type,5,TypeChange)


def fun():
    lower = np.array(YellowLower,dtype="uint8")
    upper = np.array(YellowUpper,dtype="uint8")

    while(1):
        ret,frame = cap.read()
        cv2.imshow("Clean",frame)
        #Reducing Image Blur
        MedBlur = cv2.medianBlur(frame,3)
        GusBlur = cv2.GaussianBlur(MedBlur,(3,3),2)

        #Selecting Color Range
        gray = cv2.inRange(GusBlur,lower,upper)
        cv2.imshow("Gray",gray)

        #Morphology Transofrmations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
        erode = cv2.erode(gray,kernel,iterations=5)

        #Finding Contours
        im,con,heir = cv2.findContours(erode,cv2.RETR_TREE,cv2.CHAIN_APPROX_TC89_KCOS)
        cv2.drawContours(frame,con,-1,(0,255,0),3)
        cv2.imshow("ConView",frame)
        '''
        gray = cv2.GaussianBlur(gray,(5,5),10)
        rep , thresh = cv2.threshold(gray,Thres,Upper,Type)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)

        
        im2,con,hier = cv2.findContours(thresh,2,1)
        #cv2.drawContours(frame,con,-1,(0,255,0),3)
        cnt = con[2]
        hull = cv2.convexHull(cnt,returnPoints=False)
        defects = cv2.convexityDefects(cnt,hull)
        if defects is not None:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.line(frame,start,end,(0,255,0),2)
                cv2.circle(frame,far,5,(0,0,255),-1)'''



        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break;
            print(Thres)
    cap.release()
    cv2.destroyAllWindows()
    return;


def main():
    print("INSIDE MAIN FUNCION")
    fun()
    return;

main()
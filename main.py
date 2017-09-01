import numpy as np
import cv2;

cap  = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2();
Thres = 0;#150,200
Upper = 0;
Type = 0;




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
    lower = np.array([0,10,60],dtype="uint8")
    upper = np.array([20,150,255],dtype="uint8")

    while(1):
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(5,5),10)
        #rep,thresh = cv2.threshold(gray,Thres,Upper,Type)
        #thresh = cv2.adaptiveThreshold(gray,Thres,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,4)
        rep, thresh = cv2.threshold(gray,153,140,cv2.THRESH_BINARY_INV)
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
                cv2.circle(frame,far,5,(0,0,255),-1)

        cv2.imshow('Frame',thresh)
        cv2.imshow('frame',frame)
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
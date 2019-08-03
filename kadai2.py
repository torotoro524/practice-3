import cv2

import numpy as np

from numpy import uint8

class mouseParam:
    def __init__(self, input_img_name):
        #マウス入力用のパラメータ
        self.mouseEvent = {"x":None, "y":None, "event":None, "flags":None}
        #マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)
    
    #コールバック関数
    def __CallBackFunc(self, eventType, x, y, flags, userdata):
        
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType    
        self.mouseEvent["flags"] = flags    

    #マウス入力用のパラメータを返すための関数
    def getData(self):
        return self.mouseEvent
    
    #マウスイベントを返す関数
    def getEvent(self):
        return self.mouseEvent["event"]                

    #マウスフラグを返す関数
    def getFlags(self):
        return self.mouseEvent["flags"]                

    #xの座標を返す関数
    def getX(self):
        return self.mouseEvent["x"]  

    #yの座標を返す関数
    def getY(self):
        return self.mouseEvent["y"]  

    #xとyの座標を返す関数
    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])



 #入力画像
im = cv2.imread("lenna.jpg",cv2.IMREAD_GRAYSCALE)
    
#オリジナル画像とパワースぺクトラムの表示
cv2.imshow("Original",im)
f = np.fft.fft2(im)
fshift = np.fft.fftshift(f)
spc = 20*np.log(np.abs(fshift))
M_spc = int(np.max(spc))
m_spc = int(np.min(spc))
cv2.imshow("Spectrum",((spc - m_spc)/(M_spc - m_spc) * 255).astype(uint8))



#初期の真っ黒な画像
height,width=im.shape
im1 = np.zeros((height,width))
im2 = np.zeros((height,width))
window_name = "input window"
cv2.imshow(window_name, im1)
    
#コールバックの設定
mouseData = mouseParam(window_name)


while 1:
    cv2.waitKey(20)
    #左クリックが押されたら1マスずつ表示
    if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
        im2[:,:] = 0
        im1[mouseData.getY(),mouseData.getX()] = 1
        im2[mouseData.getY(),mouseData.getX()] = 1
         
    if mouseData.getEvent() ==  cv2.EVENT_MOUSEMOVE:
        #左クリックがドラッグされたら1マスずつ表示   
        if mouseData.getFlags() == cv2.EVENT_FLAG_LBUTTON:
            im2[:,:] = 0
            im1[mouseData.getY(),mouseData.getX()] = 1
            im2[mouseData.getY(),mouseData.getX()] = 1
        #右クリックがドラッグされたら10マスずつ表示       
        if mouseData.getFlags() == cv2.EVENT_FLAG_RBUTTON:
            im2[:,:] = 0
            im1[mouseData.getY()-5:mouseData.getY()+5,mouseData.getX()-5:mouseData.getX()+5] = 1
            im2[mouseData.getY()-5:mouseData.getY()+5,mouseData.getX()-5:mouseData.getX()+5] = 1
            
    #右クリックが押されたらプログラム終了    
    if mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN:
        break;

        
    #input windowをクリックした点を白く表示
    cv2.imshow("input window",im1)
    
    #クリックしたところのsin波を表示
    fshift_2 = np.fft.fftshift(fshift*im2)
    fshift_im2=np.fft.ifft2(fshift_2)
    fshift_im2=np.abs(fshift_im2)
    M_fshift_2 = np.max(fshift_im2)
    m_fshift_2 = np.min(fshift_im2)
    cv2.imshow("This point's sin wave",((fshift_im2 - m_fshift_2)/(M_fshift_2 - m_fshift_2) * 255).astype(uint8))
    
    #クリックしたところのsin波を足し合わせることで元の画像に戻していく
    fshift_1 = np.fft.fftshift(fshift*im1)
    fshift_im1=np.fft.ifft2(fshift_1)
    fshift_im1=np.abs(fshift_im1)
    M_fshift_1 = np.max(fshift_im1)
    m_fshift_1 = np.min(fshift_im1)
    cv2.imshow("Total sin wave",((fshift_im1 - m_fshift_1)/(M_fshift_1 - m_fshift_1) * 255).astype(uint8))
    

cv2.destroyAllWindows()            
print("Finished")
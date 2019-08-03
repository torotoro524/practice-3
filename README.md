＃使い方

左クリックをされたら1マスを表示、左クリックをしながらドラッグをすれば同じように1マスを表示し、右クリックを押しながらドラッグすれば１０マス分表示し、右クリックを単体で押せばシステムは終了する

#依存ライブラリ

python 

#コード全体

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


1 ~ 9行目:高速フーリエ変換をつかうためにnumpyを実装し、astypeを使うためにuint8も実装

13 ~ 87行目:http://whitecat-student.hatenablog.com/entry/2016/11/09/225631（Opencvで表示した画像にマウスクリックした場所を取得する方法 (Python)）より、マウスイベントの処理をしめしている。

95 ~ 115行目:フーリエ変換をし、それをスぺクトラムで表示。(np.fft.fft2()やnp.fft.fftshift()が高速フーリエ変換を示す)

123 ~ 129, 195 ~ 197行目:マウスで指定するための真っ黒な画像（クリックされることで一部が白くなる使用）とその点でのsin波を出すための画像を表示。

131 ~ 139行目:どのウィンドウに対して行われたマウスでの処理をマウスイベントとしてとらえるかを指定。（コールバックの指定）

147 ~ 189行目:マウスイベントの処理。

201 ~ 213行目:クリックされた点でのsin波を表示。(102行目でクリックされた点と関連づけ、フーリエ変換をし直し、103~107行でnp.fft.ifft2()を用い逆フーリエ変換を行う)

217 ~ 229行目:今までにクリックされたすべての点に対してまとめて101~107行目に行ったことを同じように行うことで、sin波を重ねあわせ、表示する。

235行目:上のwhile文が終了すると同時に(breakされたら)ウィンドウをすべて消去する。

237行目:コンソールにプログラムが終わったことを表示する。

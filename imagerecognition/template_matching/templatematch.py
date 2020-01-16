from PIL import ImageGrab,Image
import os ,time,random


class ImageMatch:

    def  __init__(self):
        pass

    #通过给定的一张模版图片。找到模版图片在大图中的位置

    def find_image(self,filename):

        #获取图片对象
        small=Image.open(filename)

        #获取图片对象的宽高
        w,h=small.size


        #获取模版图片所有数据的对象
        sdata=small.load()

        #获取坐标为（0，0）的点的'RGBA'原组长度
        #small_data[0, 0]返回的是元组 ("R","G","B","A")
        color_length=len(sdata[0,0])



        #某些图像带Alpha通道数据，则为RGBA4位数据，而某些不带的只有3位数据

        # if color_length ==3:
        #
        #     #截取大图
        #     big=ImageGrab.grab()
        # else:
        #     big=ImageGrab.grab().convert('RGBA')
        big=Image.open("source/big.jpg")
        #获取大图所有数据的对象
        bdata=big.load()

        H=big.height
        W=big.width

        #外循环解决小图在大图中滑动的次数为
        for y in range(H-h):
             for x in range(W-w):
                 #先通过对比五个顶点的("R","G","B","A")来决定是不是要进行全面匹配

                    #x,y都是从0开始，假设大图的原点是（x,y）,模版图片的原点是（0，0），两个原点是重合的，共用一个坐标系
                    #左上角顶点
                  if (bdata[x,y]==sdata[0,0] and
                     
                     #右上角顶点
                     bdata[x+w-1,y]==sdata[w-1,0] and
                         
                     #左下角顶点
                     bdata[x,y+h-1]==sdata[0,h-1] and
                             
                     #右下角顶点
                     bdata[x+w-1,y+h-1]==sdata[w-1,h-1] and
                     
                     #中心点
                     bdata[int(x+w/2),int(y+h/2)]==sdata[int(w/2),int(h/2)]):

                     if self.check_match_dim(bdata,x,y,w,h,sdata):
                         return (int(x+w/2),int(y+h/2))



        # print("匹配失败")
        return (-1,-1)


    #大图与小图的对比
    def check_match(self,bdata,x,y,w,h,sdata):
        for i in range(h):
            for j in range(w):

                #比较每一个像素点,只要有一个像素点不同，就返回False
                if bdata[y+i,x+j] != sdata[i,j]:
                    return False

        #循环能够结束，说明没有不一致的点，是全部匹配的
        return True

    # 大图与小图的对比,返回匹配状态
    def check_match_dim(self, bdata, x, y, w, h, sdata):
        same=0
        diffrent=0

        for j in range(h):
            for i in range(w):

                # 计算相同与不同的点的个数所占比例
                if bdata[x + i, y + j] != sdata[i, j]:
                    diffrent+=1
                else:
                    same+=1

        match_score=int(same/(diffrent+same))
        if match_score >=0.9:
            return True
        else:
            return False




if __name__ == '__main__':
    A=ImageMatch()
    print(A.find_image("source/login.jpg"))





















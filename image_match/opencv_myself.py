import cv2 as cv
from PIL import ImageGrab
import os


class matchbycv:

    def find_image(self,target):

        #构造基础路径
        base_path=os.path.join(os.getcwd(),'source')

        #构造大图的保存路径
        screen_path=os.path.join(base_path,'screentest.png')

        #构造模版图片的保存路径
        template_path=os.path.join(base_path,target)

        #截取大图并保存
        ImageGrab.grab().save(screen_path)

        #从保存位置获取大图和模版图片的图片对象
        screen=cv.imread(screen_path)
        template=cv.imread(template_path)

        #进行匹配
        result=cv.matchTemplate(screen,template,cv.TM_CCOEFF_NORMED)
        min,max,min_loc,max_loc=cv.minMaxLoc(result)

        #按照匹配度筛选
        if max >=0.9:
            x=int(max_loc[0])+int(template.shape[1]/2)
            y=int(max_loc[1])+int(template.shape[0]/2)
            return x,y

        return -1,-1


    def check_exist(self,target):

        x,y=self.find_image(target)
        return x!=-1 and y!=-1

if __name__ == '__main__':
    a=matchbycv().check_exist("tmp.png")
    print(a)



















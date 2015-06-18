#coding=utf-8
#python 2.7
import urllib
import re
import shutil
import os
import sys
import getopt
import time
opts, args = getopt.getopt(sys.argv[1:],'hu:d:o:')

### get source page code 
def getHtml(url,filepath):
    page = urllib.urlopen(url)
    html = page.read()
    file_object = open(filepath+'/original.html','w')

    try:
        file_object.write(html)

    finally:
        file_object.close( )
    return html
	
### modify page source's path
def localhtml(filepath):
    file1_object = open(filepath+'/original.html')
    file2_object = open(filepath+'/index.html','w')

    try:
        html = file1_object.readlines()
        for line in html:
            reg1 = r'<img src="(.+?)"( original=".+?")?'
            imgurl = re.compile(reg1)
            imglist = re.findall(imgurl,line)

            reg2 = r'<script type="text/javascript" src="(.+?)"></script>'
            jsurl = re.compile(reg2)
            jslist = re.findall(jsurl,line)

            reg3 = r'type="text/css" href="(.+?)"'
            cssurl = re.compile(reg3)
            csslist = re.findall(cssurl,line)

            if len(imglist)!=0 or len(csslist) != 0 or len(jslist) != 0:
                if len(imglist) != 0:
                    for  img in imglist:
                        if (img[1]):
                            old_str=img[1].split('"')[1]
                        else:
                            old_str = img[0]


                        tmp = old_str.split("/")

                        new_str = "./images/" + tmp[len(tmp)-1]
                        line = line.replace(old_str,new_str)
                        #print line

                if len(csslist) != 0:
                    if len(csslist) != 0:
                        for  css in csslist:
                            old_str = css
                            tmp = old_str.split("/")

                            new_str = "./css/" + tmp[len(tmp)-1]
                            line = line.replace(old_str,new_str)
                            #print line
                if len(jslist) != 0:
                    if len(jslist) != 0:
                        for  js in jslist:
                            old_str = js
                            tmp = old_str.split("/")

                            new_str = "./js/" + tmp[len(tmp)-1]
                            line = line.replace(old_str,new_str)
                            #print line


            file2_object.write(line)
    finally:
        file1_object.close( )
        os.remove(filepath+'/original.html')
        file2_object.close( )

### download image source 	
def getImg(html,filepath):
    reg = r'<img src="(.+?)"( original=".+?")?'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    for imgurl in imglist:
        url=''
        img_name=''
        if(imgurl[1]):
            url=imgurl[1].split('"')[1]
            tmp = url.split('/')
            img_name = tmp[len(tmp)-1]
        else:
            url=imgurl[0]
            tmp = url.split('/')
            img_name =tmp[len(tmp)-1]

        img_name = filepath+"/images/" + img_name
        urllib.urlretrieve(url,img_name)
### download js code
def getJs(html,filepath):
    reg = r'<script type="text/javascript" src="(.+?)"></script>'
    jsre = re.compile(reg)
    jslist = re.findall(jsre,html)
    for urljs in jslist:
        strs=urljs.split('/')
        filename=strs[len(strs)-1]
        f=urllib.urlopen(urljs)
        if not os.path.exists(filepath+"/js/"+filename):
            with open(filename,'wb') as code:
                code.write(f.read())
            shutil.move(filename,filepath+'/js')
###download css code 
def getCss(html,filepath):
    reg = r'type="text/css" href="(.+?)"'
    cssre = re.compile(reg)
    csslist = re.findall(cssre,html)
    for urlcss in csslist:

        strs=urlcss.split('/')
        filename=strs[len(strs)-1]
        f=urllib.urlopen(urlcss)
        #print filepath+'/css/'+filename
        if not os.path.exists(filepath+'/css/'+filename):
            with open(filename,'wb') as code:
                code.write(f.read())
            shutil.move(filename,filepath+'/css')

def main(argv):
#def main():
    url = ''
    uptime = 0
    path = ''
    for op,value in opts:
        if op == '-d':
            uptime = value
        if op == '-u':
            url = value
        if op == '-o':
            path = value

    while True:
        Now_time = time.localtime(time.time())
        mon = ''
        day = ''
        hour = ''
        minute = ''
        second = ''

        if (Now_time.tm_mon < 10):
            mon = '0'+ str(Now_time.tm_mon)
        else:
            mon = str(Now_time.tm_mon)
        if (Now_time.tm_mday < 10):
            day = '0'+ str(Now_time.tm_mday)
        else:
            day = str(Now_time.tm_mday)
        if (Now_time.tm_hour < 10):
            hour = '0'+ str(Now_time.tm_hour)
        else:
            hour = str(Now_time.tm_hour)
        if (Now_time.tm_min < 10):
            minute = '0'+ str(Now_time.tm_min)
        else:
            minute = str(Now_time.tm_min)
        if (Now_time.tm_sec < 10):
            second = '0'+ str(Now_time.tm_sec)
        else:
            second = str(Now_time.tm_sec)
        path_time = ''+str(Now_time.tm_year)+mon+day+hour+minute+second
        #print path_time
        if not os.path.exists(path_time):
            os.makedirs(path+path_time)
            os.makedirs(path+path_time+'/js')
            os.makedirs(path+path_time+'/css')
            os.makedirs(path+path_time+'/images')
        file_path = path+path_time
        html = getHtml(url,file_path)
        getCss(html,file_path)
        getImg(html,file_path)
        getJs(html,file_path)
        localhtml(file_path)
        time.sleep(int(uptime))

if __name__ == '__main__':
    main(sys.argv)

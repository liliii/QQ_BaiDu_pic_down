#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from time import sleep
import sys,os
import requests,time
import threading
# 保存图片目录
save_file = 'E:/qq_f_0226/'
t_start = time.time()
#获取相册图片
def login(driver):
    b = False
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a == True:
        #浏览器可见登录
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()  # 选择用户名框3083567057
        driver.find_element_by_id('u').send_keys('3083567057')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('lxl3083567057')
        driver.implicitly_wait(10)  # 在一个时间范围内智能的等待。
        # driver.execute_script('var button = document.getElementById("login_button")')
        driver.find_element_by_id('login_button').click()
    driver.implicitly_wait(10)
    driver.switch_to.default_content()#防止出现selenium.common.exceptions.WebDriverException: Message: TypeError: can't access dead object问题，出现
    try:
        # driver.implicitly_wait(60)
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        print '允许访问空间1'
        b = True
    except:
        print '不允许访问空间1'
        # driver.close()
        # driver.quit()
    # if b == True:
    #     loadPic(qq, driver)
    return b
#下载相册中的资源
def loadPic(qq,driver,fp):
    print('====正在访问相册=====')
    try:
        driver.get('http://user.qzone.qq.com/{}/4'.format(qq))
        driver.implicitly_wait(10)
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        iframe = driver.find_element_by_xpath("//iframe[@name='app_canvas_frame']")  # phantomjs对xpath元素定位查找有较好的支持
        driver.switch_to.frame(iframe)
        allowaccess_ls = driver.find_elements_by_xpath("//div[@data-allowaccess='1' and @data-total>'1']/div/a")
        for i in range(0, len(allowaccess_ls)):
            driver.implicitly_wait(10)
            allowaccess_ls1 = driver.find_elements_by_xpath("//div[@data-allowaccess='1' and @data-total>'1']/div/a")
            # TODU 无界面不能使用click()
            driver.implicitly_wait(10)  # 在一个时间范围内智能的等待。
            allowaccess_ls1[i].click()
            print '点击可访问的第' + str(i + 1) + '个相册'
            img_ls = driver.find_elements_by_css_selector(".j-pl-photoitem-img")
            for j in range(0, len(img_ls)):
                img_ls1 = driver.find_elements_by_css_selector(".j-pl-photoitem-img")
                try:
                    link = img_ls1[j].get_attribute('src')
                    try:
                        link = link.strip()
                    except:
                        pass
                    str_m = link.index('/m/')
                    str_r = link.index('&rf=')
                    str_big_img = link[0:str_m + 1] + 'b' + link[str_m + 2:str_r] + '&rf=viewer_4'
                    fp.write(str_big_img + '\n')
                    print '相册图片地址===', str_big_img
                    # dowmloadPic(str_big_img, save_file + str(qq) + '/' + str(i) + '_' + str(j) + '_pic.jpg')
                except:
                    pass
            driver.implicitly_wait(10)
            driver.back()  # 返回上一页
        driver.switch_to.default_content()  # 返回iframe外面的内容
    except:
        print '不予许访问相册'
        # 释放信号量，信号量加一
    # get_shuoshuo(qq, driver, fp)
    # semaphore.release()
#下载说说里面的资源
def get_shuoshuo(qq,driver,fp):
        print('====即将访问说说=====')
        try:
            driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
        except:
            print '不予许访问说说'
        driver.implicitly_wait(10)
        driver.switch_to.default_content()
        driver.switch_to.frame('app_canvas_frame')
        hp = driver.find_elements_by_class_name('img-attachments-inner')
        img_number=0
        for ho in hp:
            hq = ho.find_elements_by_tag_name('a')
            for tg in hq:
                try:
                    linkF = tg.get_attribute('href')
                    try:
                        linkF = linkF.strip()
                    except:
                        pass
                    str_c = linkF.index('/c/')
                    str_big_img = linkF[0:str_c + 1] + 'b' + linkF[str_c + 2:-1] + '!&rf=viewer_311'
                    print '说说图片地址===', str_big_img
                    fp.write(str_big_img + '\n')
                    # urllib.request.urlretrieve(linkF[0:-1], 'F:/qq_friend/myself/%s.jpg' % str(x))
                    # dowmloadPic(str_big_img[0:-1], save_file+str(qq)+'/' + str(img_number) + '.jpg')
                    img_number += 1
                except:
                    pass

#下载图片
def dowmloadPic(url,save_file):
   try:
    pic = requests.get(url, timeout=20)
    fp = open(save_file.decode('utf-8').encode('cp936'),'wb')
    fp.write(pic.content)
    fp.close()
   except requests.exceptions.ConnectionError:
    pass
#新建文件目录
#参数path：目录文件名
#成功返回1
#失败返回0
def createfile(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在'
        return False
# 删除不能打开的文件和目录
def delcantopen(dir):
    for root, save_file, files in os.walk(dir):
        for file in files:
            try:
                im = Image.open(root + '//' + file)
            except:
                os.remove(root + '//' + file)
        try:
            os.rmdir(root)#删除不能打开的文件
        except:
            pass
#下载某个范围的QQ数据
def downQQPic(begin,end):
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = (
    #     "Mozilla/5.0 (Linux; Android 8.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    # )
    # driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver = webdriver.PhantomJS('E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    # driver = webdriver.Firefox()
    driver.get('http://qzone.qq.com')
    temp = login(driver)
    if temp == True:
      for qq in range(begin,end):
        # 获取qq
        # filepath = save_file + str(qq)
        # if createfile(filepath) == True:

        print '创建文件时间：', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        log_name = save_file+"/"+str(qq) + '_log.txt'.decode('utf-8')
        print 'log_name===',log_name
        fp = open(log_name, 'a')  # w会覆盖，a代表追加1164899794
        try:
                #获取QQ相册图片
            loadPic(qq, driver,fp)
                # 获取qq说说的图片
            get_shuoshuo(qq, driver, fp)
        except:
            continue
            fp.close()
    # driver.close()#使用浏览器访问，退出时需要关闭浏览器
    driver.quit()#使用无浏览器，退出的时候需要释放资源
def fun(semaphore, num):
    # 获得信号量，信号量减一
    semaphore.acquire()
    # 随机生成QQ号（1164867801----1164870024）1164869068 =====0213号，1164927801==
    downQQPic(1165037800, 1165047800)
    # 释放信号量，信号量加一
    semaphore.release()
if __name__ == '__main__':

    # 初始化信号量，数量为2
    semaphore = threading.Semaphore(2)
    # 运行4个线程
    for num in xrange(5000):
        t = threading.Thread(target=fun, args=(semaphore, num))
        t.start()
    # 删除空目录、删除不能打开的图片
    # delcantopen(save_file)
    t_end = time.time()
    print('the thread way take %s s' % (t_end - t_start))
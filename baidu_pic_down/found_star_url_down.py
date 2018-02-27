# -*- coding:utf-8 -*-


"""

    问答助手~

"""
import xlwt

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import PicDownloaderPeople
import configparser
#导入工具包copy
from xlutils.copy import copy
from xlrd import open_workbook
import os
conf = configparser.ConfigParser()
conf.read("config.ini")

data_directory = conf.get('config',"data_directory")

vm_name = conf.get('config',"vm_name")

app_name = conf.get('config',"app_name")

search_engine = conf.get('config',"search_engine")

hot_key = conf.get('config',"hot_key")

# ocr_engine = 'baidu'
ocr_engine = conf.get('config',"ocr_engine")

### baidu orc
app_id = conf.get('config',"app_id")
app_key = conf.get('config',"app_key")
app_secret = conf.get('config',"app_secret")

### 0 表示普通识别
### 1 表示精确识别
api_version = conf.get('config',"api_version")

### hanwang orc
hanwan_appcode = conf.get('config',"hanwan_appcode")

#读取txt，并保存
#先读取txt文件，line，按line的关键字读取，访问百度，将结果和line存入Excel中
def read_saveTXT():
    # 1.创建一个excell文件
    workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
    # 2.创建一个sheet
    sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    # 文件名
    file_x = open('E:\\名人名单\\中国企业.txt'.decode('utf-8').encode('cp936'))
    # file_y = open('E:\\model_output_log\\y\\_iter_36000_yhand_output.txt')
    # 临时变量，sheet的行
    temp = 0
    for line in file_x.readlines():
        line = line.strip('\n')
        try:
            # .出现的位置
            first = line.index('.')
            # 空格出现的位置
            last = line.index(' ')
            # 需要的字符串
            company = line[first + 1:last + 1].decode('cp936')
            # 将字符串写到sheet的第temp行0列
            sheet1.write(temp, 0, company)
        except:
            pass
        # 行加一
        temp += 1
        # 保存Excel文件到指定路径
    workbook.save('C:\\work\\worklog\\log\\20180108\\Fortune500Companies.xlsx')
    # 释放资源
    file_x.close()
#读txt文件
#param :file 文件的路径及名称
#return：company_list 返回读取到的字符列表
def read_TXT(file):
    company_list = []
    file_x = open(file)
    for line in file_x.readlines():
        line = line.strip('\n')
        try:
            # .出现的位置
            first = line.index('.')
            # 空格出现的位置
            last = line.index(' ')
            # 需要的字符串
            company = line[first + 1:last].decode('cp936')
            company_list.append(company)
        except:
            pass
    return company_list
#保存Excel文件:save_excel1
#param:
# excel：路径
#test_leader_list：列表名称
#row：当前为第几行
def save_excel1(excel,test_leader_list,row):
    rb = open_workbook(excel,formatting_info=True)
    wb=copy(rb)
    sheet = wb.get_sheet('sheet1')
    #copy Excel文件
    temp = 0
    for i in test_leader_list:
        # sheet1.write(row, temp, i)
        sheet.write(row, temp, i)
        temp += 1
    os.remove(excel)
    wb.save(excel)
#保存Excel文件:save_excel
#param:
# excel：路径
#value：值
#row：当前为第几行
def save_excel(excel, value, row):
        rb = open_workbook(excel, formatting_info=True)
        wb = copy(rb)
        os.remove(excel)
        sheet = wb.get_sheet('sheet1')
        # copy Excel文件
        # sheet1.write(row, temp, i)
        sheet.write(row, 0, value)
        wb.save(excel)
    # 2.创建一个sheet
    # sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
#百度根据关键字检索
#param：
#Word：关键字
#return：
#leader_list:查询到的公司主要领导列表
def baidu(word):
    browser = webdriver.PhantomJS('E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    browser.get(search_engine)
    # 测试
    keyword = word
    leader_list = []
    if len(keyword) < 2:
        print("没识别出来，随机选吧!!!\n")
        print("题目出现的时候按F2，我就自动帮你去搜啦~\n")
    print("我用关键词:\" ", keyword, "\"去百度答案啦!")
    browser.implicitly_wait(30)
    elem = browser.find_element_by_id("kw")
    # opr - recommends - merge - panel  opr - recommends - merge - mbGap
    elem.clear()
    elem.send_keys(keyword.decode('utf-8'))
    elem.send_keys(Keys.RETURN)
    name1 = browser.find_elements_by_xpath("//div[@class='c-gap-top-small']/a")
    for j in range(0, len(name1)):
        browser.implicitly_wait(30)
        name = browser.find_elements_by_xpath("//div[@class='c-gap-top-small']/a")
        # link = name[j].get_attribute('a').get_text()
    try:
     for i in range(0, len(name)):
        leader = name[i].get_attribute('title')
        if len(leader) >3:
            continue
        # print leader
        leader_list.append(leader)
    except:
        print 'error'
        leader_list.append(keyword)
    # browser.close()
    browser.quit()
    return leader_list

if __name__ == "__main__":
    #2.一个字符串读取主持人名字
    string = "刘雯 何穗 吕燕 周韦彤 于芷晴 金美辛 苏夏 谢梦 付欢欢 宋姗姗 王馨漪 王熙然 冒绮 刘雨晴 帕丽扎提 熊文丹 傅宗正 钟浠文 李沐航 章佳怡 孔媛媛 李艾 泷泽 张超谈 郝允祥 纪凌尘 王朱筱寅 奚梦瑶 杜诗博 游天翼 扈忠汉 李进 张伦硕 蒋劲夫 高云翔 张亮 张耀扬 郑元畅 向佐 贺军翔 高以翔 胡兵 蓝正龙 周柏豪 张晓晨 纪凌尘 马里山 高伟光 郭品超 刘畅 吕晓霖 黄觉 王东 吴建飞 李子峰 胡东 丁一 盛超 沈志明 罗弘证 巫迪文 黄靖翔 张勋杰 张继 米热（模特） 温升豪 杨一展 吴卓翰 鲁诺 吴慷仁 董晨 任言恺 徐开骋 金大川 袁奇峰 王乐乐 丁春诚 张爱朋 杜达雄 陈泽宇 柴格 曲鑫 赵磊 白梓轩 石乃文 顾成栋 陈伟成 宋海颉 朱晓辉 金磊 隋咏良 金浩森 甄志强 李沛旭 杜维瀚 周孝安 黄家诺 严昆 董春辉 蔡沛然 时诗（模特） 符晓 彦晞 卢希安 刘江波 jamesma 张雁名 张昊翔 苗韵桐 李至正 马月 王强新 赵骏亚 董波 钟子炫 曹英睿 黄宁 苏晗烨 余秉谚 许腾方 王星凯 王德枫 李雪明 傅正刚 陈超尉 宋文定 胡豆 李寅飞 王子灿 王子灿 梁传斌 邹文正 徐丁 艾克拜尔 邱彦臣 庄夏播 王嘉儒 张圣启 黄冠僖 何尚谦 周双健 方帅 彭松 李灏哲 杨楠峰 邱士峻 阮文涛 任雨 周恒远 齐晓龙 宁炜 杜艺龙 王增楠 李银龙 李奕辰 赵俊承 刘昊钧 郑大鹏 高崎纶 魏煜宇 董晓龙 莫合塔尔 赵梓铭 陈逸轩 苏泽轩 王子培 周士博 王仲焘 吕元浩 吴民凡 王辞景 程永博 孙家鹏 刘建喜 宗幽 温昇豪 温昇豪 温昇豪 连勋 扈忠汉 赵梦玥 文咏珊 李丽珍 蔡文静 郭美美 陈若仪 干露露 龚玥菲 赵韩樱子 张予曦 沈梦辰 金晨 许婧 熊黛林 张梓琳 闫凤娇 周秀娜 黄翠如 孙耀琦 章龄之 邓丽欣 乔欣 南笙 杜鹃 丁丁（模特） 吴亚馨 热依扎 柯蓝（模特） 叶梓萱 翟凌 陈静 马伊咪 郭书瑶 何佩瑜 刘心悠 母其弥雅 萧蔷 吴千语 瞿颖 何穗 厉娜 郭雪芙 潘霜霜 孟广美 寇静 高磊鑫 何泓姗 徐子淇 倪虹洁 米露（模特） 李斯丹妮 吴佩慈 关颖 贾晓晨 卢靖姗 方媛 隋棠 汤芳 曲栅栅 白歆惠 许玮甯 陈彦妃 小葡萄（模特） 刘羽琦 梁小冰 唐诗咏 莫绮雯 翁慧德 张籽沐 李毓芬 江语晨 秦舒培 曾恺玹 付梦妮 苏紫紫 冉莹颖 江祖平 汤加丽 林弯弯 任容萱 于娜 庄思敏 林宜芝 陈匡怡 安心亚 汪诗诗 任娇 陈静仪 杜蕾斯女孩 赖雅妍 温心（模特） 蒋怡 李颖芝 潘春春 皇甫圣华 郭颖儿 黄一琳 痣奶妹 洪小铃 林韦君 郭美玲 樊玲 吴晴晴 高丽虹 迪丽娜尔 陈庭妮 桃宝（模特） 卫诗雅 陈嘉桓 齐芳 陈露 杨紫璐 野猪桃桃宝 谢芷蕙 小灿（模特） 李欣聪 李珊珊 利菁 陈嘉宝 邢星 叶可儿 张婉悠 陈丹婷 牟星 陆翊 习云波 血纯茗雅 许龄月 王洁曦 梁又琳 韩熙庭 陈燃 王希怡 戚蓝尹 戚蓝尹 甄锡 林柯彤 梁靖琪 林娜冰 傲蕾 那笛 周泓 春晓（模特） 许维恩 夏如芝 王熙然 颜卓灵 喻可欣 周惠楠 房思瑜 于咏琳 李斯羽 周娇 王慧 曹安娜 吕慧仪 颜颖思 周采诗 王思平 何傲儿 赵洁 夏馨雨 林姮怡 陈欣予 林辰唏 徐佳琦 许秀琴 柳菁菁 刘伊心 李海鑫 苏瑾 王静莹 田晓天 魏蔓 钱韦杉 郑云灿 李昕岳 黎梦恬 丁小芹 张咏棋 周伟童 钟鹿纯 杨宝玲 王希维 瑞莎 张倩 张已桂 陈潇 沈可乐 陈庭欣 曹阳 古晨 赵欣颖 雎晓雯 王妍苏 蔡芷瑜 李玲 刘熏爱 端木云 文雯 邹杨 荆灵 穆熙妍 刘蕾 苏笠汶 陈玟予 徐莹 汪圆圆 佟晨洁 叶熙祺 杨梓瑶 陈慧玲 赖琳恩 简廷芮 林芊妤 陆舒媛 文凯玲 李亚红 覃霓 林采缇 徐淑敏 陈思琪 林若亚 马春瑞 汤洛雯 常春晓 王敏奕 崔漫莉 韩君婷 孟十朵 陈见飞 林瑞瑜 刘宸希 龚美琪 陈雅丽 高梦瑶 王海珍 冯婧 陈淑兰 丁贝莉 陆瑶 冯溪 于芷晴 叶倩云 谢欣颖 千夜未来 汤怡 黛欣霓 林嘉绮 连绮岚 金美辛 周汶锜 张筱婕 黄钰筑 钟恩淇 张名雅 赵越 李舒桐 巴哈古丽·热合木吐拉 赵悦童 谢语恩 王茜麟 刘雨柔 王妤涵 王祉萱 莫万丹 陈晴漪 倪雅伦 江伊涵 杨雨薇 徐贵樱 石天欣 裴蓓 林立雯 胡盈祯 李妍瑾 何昊阳 何昊阳 韩雪薇 程思 徐钰涵 王婧乔 彭静 朱佳希 吴雨婵 姚采颖 桂晶晶 陈兴瑜 于文霞 林钰轩 程予希 刘乐妍 关慧卿 王秋紫 江天佑 余薇薇  张钰凰 陈语安 简佩筠 蒋祖曼 姜培琳 孔肖吟 康倩雯 崔若涵 希莉娜依 温翠苹 曾安琪 王尹平 关关 李蕴 叶贤 符晓薇 王梓清 许安安 刁琳琳 子璇 陈维龄 银雪 陈娟红 陈倩扬 李艳冰 郭子千 范霞 刘凡菲 倪慕斯 柳侑绮 温健婷 邱箫婵 马伊娜 沈芳熙 王毓菲 薛婧 初家晴 黄嫀砚 曾佩瑜 张辛怡 游天翼 洪棠 罗漩 王泫伊 丹增白姆 贾永婕 陈雨涵 马诗慧 武潇 王美雪 帕丽扎提 温建婷 应媛 邓尘朵 陈莉莉 宗灵 郭玉良 苏子贤 徐靖雯 陈瑀希 柏妍安 林孟瑾 李宛仪 刘洛汐 德馨 伍娟 王静珊 乔雯婧 许薇 白莫菲 朱裕琳 李鸣惊 唐艺纯 李京恬 巧巧 柯佳青 陈瑀涵 李野 童唯佳 邹开云 陈昭昭 赵煜 董妮娜 宋姗姗 王家珧 赵诗梦 田璐菡 费伟妮 张琼姿 吴语晴 西瓜妹 陶妍霖 贺宏娟 毛妮卓玛 穆盈 李妍锡 张乃鸥 赵已晨 夏尉喻 郑靖雯 王迎莘 祁迹 李雨桦 王梦实 吉丽 褚颖颖 王欧 吕平滢 画嘉 佳琪 李冠仪 覃文静 瞿麟曼 熊文丹 陈维芊 张译文 林司敏 韩盼盼 孙一奇 陈娇 姚文婷 袁思怡 李沙沙 单麒汶青 王一婷 楚谨 艾薇微 金甜甜 邝敏慧 韩盼盼 孙一奇 陈娇 姚文婷 袁思怡 李沙沙 单麒汶青 王一婷 楚谨 艾薇微 金甜甜 邝敏慧 邱璐璠 姚乐碧 龙蕾 李晓涵 关文晶 王鲲鹏 杨诗吟 石佳灵 韩璐 谭志玲 曹珊珊 徐梦雅 正原未来 宋乐 袁璐婷 唐菱 王雯琴 郑伊菲 吴艳樱 秦梦擎 毛楚玉 戴小奕 林紫君 胥力文 李子涵 娜宝 张茜儿 薛萌 张子涵 莫西 陆遥 陈美里 邱佳妮 王梦雅 李叶 任莹露 陈春 肖辰 曹米娅 李楚君 林霞 大Ann 陈馨婷 邱心语 黄雪莹 彭慧中 潘婷婷 孙程程 沈梦瑶 唐心 郭梦瑶 崔紫轩 容子菲 龙馨悦 高智洋 许任媛 白钦惠 陈橙 陈沛嘉 赵雅琪 郭硕 郭思雅 张盼盼 樱萘 语嫣 温晓菁 吴迪雅 冯珂 何思谚 王心宜 陈心怡 刘芊妤 叶佳蓁 郭芷岑 王艺臻 马依热·艾… 谢梦恬 于娇娇 廖艺璇 薛丹 李小青 王淑 刘雨轩 蔡莹莹 刘子仟 张紫炜 黎月明 王嘉莹 马爱媛 黎伟珊 白丽娜 陈美美 杨慧娇 黄晓萌 魏子雅 谢佳诺 倪婷 杨暘 刘姝瑾 赵亚仪 姚西梦 江君 安钦云 徐瑶 易涵 武岳 范婷婷 王纡希 丁羽彤 王亭又 肖瑶瑶 吴美俞 党佳妮 胡诗琪 金焱 蒋梦瑶 卢怡榕 谢瑗 朱薇 米莎YOYO 张仪嘉 杨鑫婷 曹婷 段呈凤 王玉杨 沈妍 柳萌 刘思含 王逸宣 金禧 陈泳文 王文妍 郭文煊 刘沛蘅 陈思伊 潘旻嫣 索蕾娜 狐尘 谷悦 于岩 章晨佼 陈慧凝 王志君 李媛丽 邓萱萱 殷宏艳 马甜 朱芷仪 宗妮 赵雨洁 周星伶 薇拉贝儿 李思航 李恒敏 张中允 蔡紫琪 张晓婧 陈若若 顾一凝 林晓丹 左丹璐 赵晓颖 冒绮 方琪儿 颜夕子默凉… 胡雨薇 王卿文 傅晓莉 潘佳星 赖银霞 姚梦茹 程奇 陈彦彤 李馨蕊 王嘉敏 黄思齐 叶寒冰 徐熙素 张纯语 辛蕊 于净漫 李小瑶 官佳蓉 陈露西 黄唯 栗荟涵 丁姣姣 宋雨薇 周廷珊 蔡琰儿 李文祺 吴潇雨 刘荞溪 邹沂含 唐杨 相园园 冯开心 李华宇 李依丽 于舒靓 曹梦莹 王奕今 何郑君 凡思琪 籍爽 魏云博 王婷仪 邝萃莉 米日办·买… 高婉祯 布晓青 吴怡莎 刘巾薇 郑菓 晋梦蝶 李璇语 帕丽扎 刘菲雨 杜影 徐梦轩 韩金晔 马安黛 刑宇婷 陈艳儿 赵轩俪 杨静宁 吴雨蝉 罗慕儿 朱彩丽 郑雅菁 许歆苒 付婧炜 宋晋瑶 李彦楠 杜绍燕 钱丽玲 池金妍 耐吉 林苇茹 杨雅熙 宋美霖 崔雅婕 步小熙 李嘉琳 小怡怡"
    words = string.split(' ')
    excel_filepath = 'C:\\work\\worklog\\log\\20180108\\famous_model.xlsx'
    name_list = PicDownloaderPeople.MyTestFoundFamouse.read_excel(excel_filepath)
    # string = "林清玄 龙应台 林清玄 龙应台 123      "
    dict1 = {}
    l2 = {}.fromkeys(name_list).keys()
    filepath = ''
    for word in l2:
        if len(word) < 2:
            continue
        filepath = 'E://star_pic//' + word
        print 'file==', filepath
        if PicDownloaderPeople.createfile(filepath) == True:
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '的生活' + '&ct=201326592&v=flip'
            result = PicDownloaderPeople.requests.get(url)
            PicDownloaderPeople.dowmloadPic(result.text, word, filepath)
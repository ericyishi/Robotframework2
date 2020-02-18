#-*- coding: utf-8 -*-
import errno
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import math
import operator
import os
import imutils
from robot.api import logger
from PIL import Image, ImageChops
from skimage.measure import compare_ssim


from CusBase import CusBase


class ImageCompare(CusBase):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    """
    image compare类
    """

    def __init__(self,
                 running_param,
                 timeout=1.0,
                 implicit_wait=0.0,
                 run_on_failure='capture_page_screenshot',
                 screenshot_root_directory=None
                 ):
        super(ImageCompare, self).__init__(running_param,
                                           timeout=1.0,
                                           implicit_wait=0.0,
                                           run_on_failure='capture_page_screenshot',
                                           screenshot_root_directory=None
                                           )
        self.running_param = running_param
        self.expect_picture_dir = self.running_param['expect_picture_dir']
        self.result_picture_dir = self.running_param['result_picture_dir']
        self.diff_picture_dir = self.running_param['diff_picture_dir']

    def picture_compare(self, expect_picture_name, result_picture_name, rms_threshold=50):
        """
        图片比对算法,result的值越大,说明两者的差别越大,如果result=0,则说明两张图一模一样.
        sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
        operator.add(x,y)对应表达式：x+y
        这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)
        :param expect_picture_name: 比对标准的图片名称,不带.png后缀
        :param result_picture_name: 实际结果的图片名称,不带.png后缀
        :param rms_threshold: 比对标准图片和实际结果图片的RMS极限值
        :return: True一样/False不一样
        """
        expect_picture = os.path.abspath(os.path.join(self.expect_picture_dir, '%s') % (expect_picture_name + '.png')).replace(os.sep, '/')
        result_picture = os.path.abspath(os.path.join(self.result_picture_dir, '%s') % (result_picture_name + '.png')).replace(os.sep, '/')
        # print 'expect_picture_name is :', expect_picture_name
        # print 'result_picture_name is :', result_picture_name

        expect_picture_relative_path = (os.path.join('../TestData/Screen/Expect', (expect_picture_name + '.png'))).replace('/', os.sep)
        result_picture_relative_path = (os.path.join('../TestData/Screen/Result', (result_picture_name + '.png'))).replace('/', os.sep)

        exp = self._get_expect_name(expect_picture_name)
        rel = self._get_result_name(result_picture_name)

        logger.write('Picture comparing...', html=True)
        logger.write('expect_picture is : %s' % (expect_picture.decode()), html=True)
        logger.write('</td></tr><tr><td colspan="3">''<a href="%s"><img src="%s" width="800px"></a>'
                     % (expect_picture_relative_path.decode(), expect_picture_relative_path.decode()), html=True)
        logger.write('result_picture is : %s' % (result_picture.decode()), html=True)
        logger.write('</td></tr><tr><td colspan="3">''<a href="%s"><img src="%s" width="800px"></a>'
                     % (result_picture_relative_path.decode(), result_picture_relative_path.decode()), html=True)

        result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b)**2, exp, rel))) / len(exp))
        # print 'result is: ', result
        if result < 1:
            print 'Expect picture and result picture are the same!'
            return True
        else:
            with Image.open(r"%s" % (expect_picture.encode('gbk'))) as img_exp:
                expect_width, expect_height = img_exp_size = img_exp.size
            with Image.open(r"%s" % (result_picture.encode('gbk'))) as img_rel:
                result_width, result_height = img_rel_size = img_rel.size
            # print img_exp_size, img_rel_size
            # 尺寸一样
            if img_exp_size == img_rel_size:
                pass
            # 尺寸不一样,将预期图片尺寸更改成和结果图片一致
            else:
                # 预期图片的尺寸更大
                if img_rel_size < img_exp_size:
                    with Image.open(r"%s" % (expect_picture.encode('gbk'))) as expect_image:
                        box = (0, 0, result_width, result_height)
                        # print box
                        expect_image.crop(box).save(expect_picture.encode('gbk'))
                        # print 'change expect picture dimension'
                # 结果图片的尺寸更大
                else:
                    with Image.open(r"%s" % (result_picture.encode('gbk'))) as result_image:
                        box = (0, 0, expect_width, expect_height)
                        # print box
                        result_image.crop(box).save(result_picture.encode('gbk'))
                        # print 'change result picture dimension'
            image_expect = Image.open(r"%s" % (expect_picture.encode('gbk')))
            image_result = Image.open(r"%s" % (result_picture.encode('gbk')))
            diff = ImageChops.difference(image_expect, image_result)
            diff_pix = diff.getbbox()
            h = diff.histogram()
            sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
            sum_of_squares = sum(sq)
            rms = math.sqrt(sum_of_squares / float(image_expect.size[0] * image_expect.size[1]))    #root mean square均方根
            print 'rms is: ', rms
            # image_expect.close()
            # image_result.close()
            if diff_pix is None:
                return True
            elif rms <= float(rms_threshold):    # rms_threshold是经过系列图片测试出来的经验值
                return True
            else:
                # 加载两张图片并将他们转换为灰度
                import cv2
                print "rms值不一致灰度比较"
                image_expect_picture = cv2.imread(r"%s" % (expect_picture.encode('gbk')))
                image_result_picture = cv2.imread(r"%s" % (result_picture.encode('gbk')))
                # gray_expect_picture = cv2.cvtColor(image_expect_picture, cv2.COLOR_BGR2GRAY)
                # gray_result_picture = cv2.cvtColor(image_result_picture, cv2.COLOR_BGR2GRAY)
                gray_expect_picture = cv2.imread(r"%s" % (expect_picture.encode('gbk')), 0)
                gray_result_picture = cv2.imread(r"%s" % (result_picture.encode('gbk')), 0)
                # print gray_expect_picture.shape
                # print gray_result_picture.shape
                # 计算两个灰度图像之间的结构相似度指数
                (score, diff) = compare_ssim(gray_expect_picture, gray_result_picture, full=True)
                diff = (diff * 255).astype("uint8")
                # print("SSIM:{}".format(score))
                # 找到不同点的轮廓以致于我们可以在被标识为“不同”的区域周围放置矩形
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                # 找到一系列区域，在区域周围放置矩形
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(image_expect_picture, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(image_result_picture, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # 直接使用'/'进行分割会因为系统(Window,Linux)不一样而有bug，所以采用os.sep
                diff_folder_list = expect_picture_name.split(os.sep)[:-1]
                diff_picture_name = expect_picture_name.split(os.sep)[-1]
                # print 'diff_picture_name is :', diff_picture_name
                if len(diff_folder_list) == 0:
                    diff_picture = os.path.abspath(os.path.join(self.diff_picture_dir, '%s') % (expect_picture_name + '_diff.png'))
                    diff_picture_relative_path = (os.path.join('../TestData/Screen/Diff', (diff_picture_name + '_diff.png'))).replace('/', os.sep)
                else:
                    diff_folder_name = os.sep.join(diff_folder_list)
                    # print 'diff_folder_name is :', diff_folder_name
                    diff_picture_directory = os.path.abspath(os.path.join(self.diff_picture_dir, diff_folder_name))
                    self._create_folder(diff_picture_directory)
                    diff_picture = os.path.abspath(os.path.join(diff_picture_directory, '%s') % (diff_picture_name + '_diff.png'))
                    diff_picture_relative_path = (os.path.join('../TestData/Screen/Diff', os.path.join(diff_folder_name, (diff_picture_name + '_diff.png')))).replace('/', os.sep)
                    # print 'diff_picture is :', diff_picture

                # 用cv2.imshow展现最终对比之后的图片， cv2.imwrite保存最终的结果图片
                cv2.imshow("Modified", image_result_picture)
                cv2.imwrite(diff_picture.encode("gbk"), image_result_picture)
                cv2.destroyAllWindows()
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                logger.write('Expect picture and result picture are different!\n''Please check at %s' % (diff_picture.decode()), html=True)
                logger.write('</td></tr><tr><td colspan="3">''<a href="%s"><img src="%s" width="800px"></a>' % (diff_picture_relative_path.decode(), diff_picture_relative_path.decode()), html=True)
                return False


    def _get_expect_name(self, expect_picture_name):
        """
        获取预期结果图片的直方图数据
        :param expect_picture_name: 目标图片名称,不带.png后缀
        :return:
        """
        expect_picture = os.path.abspath(os.path.join(self.expect_picture_dir, '%s') % (expect_picture_name.encode('gbk') + '.png'))
        # print 'read expect_picture, %s' % expect_picture
        image1 = Image.open(expect_picture)
        h1 = image1.histogram()
        return h1

    def _get_result_name(self, result_picture_name):
        """
        获取实际结果图片的直方图数据
        :param result_picture_name: 实际结果的图片名称,不带.png后缀
        :return:
        """
        result_picture = os.path.abspath(os.path.join(self.result_picture_dir, '%s') % (result_picture_name.encode('gbk') + '.png'))
        # print 'read result_picture, %s' % result_picture
        image2 = Image.open(result_picture)
        h2 = image2.histogram()
        return h2

    def _create_folder(self, path):
        """
        Creates 'path' if it does not exist
        If creation fails, return False
        :param path: the path to ensure it exists
        :return True/False
        """
        if not os.path.exists(path):
            try:
                os.makedirs(path.encode('gbk'))
                print 'Creat directory of %s' % path
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    return True
                else:
                    print 'An error happened trying to create %s!' % path
                    return False

if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    running_param = {
        'BROWSER': 'Chrome',  # Chrome|ff
        'DELAY': 0.5,
        'BASE_URL': 'https://www.baidu.com/',
        'screenshot_dir': base_path + '/../../TestData/Screen/Result',
        'expect_picture_dir': base_path + '/../../TestData/Screen/Expect',
        'result_picture_dir': base_path + '/../../TestData/Screen/Result',
        'diff_picture_dir': base_path + '/../../TestData/Screen/Diff',
    }
    test=ImageCompare(running_param,
                        timeout=5.0,
                        implicit_wait=0.0,
                        run_on_failure='capture_page_screenshot',
                        screenshot_root_directory=None
                        )
    result=test.picture_compare('test\\aaa','test\\aaa',10)
    print result
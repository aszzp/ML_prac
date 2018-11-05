import imageio
from PIL import Image, ImageFont, ImageDraw
from pylab import *
from scipy.cluster.vq import *
from scipy.misc import imresize
import os


# steps*steps像素聚类
def clusterpixels_square(img, k, steps, mode):
    im = img
    # im.shape[0] 高 im.shape[1] 宽
    dx = im.shape[0] // steps
    dy = im.shape[1] // steps
    # 计算每个区域的颜色特征
    features = []
    for x in range(steps):
        for y in range(steps):
            R = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 0])
            G = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 1])
            B = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 2])
            features.append([R, G, B])
    features = array(features, 'f')     # 变为数组
    # 根据mode决定聚类初始化方式.聚类,k是聚类数目,code是每个点所对应的聚类标记序号
    if mode == 1:
        centroids, nothing  = kmeans(features, k)
        index, nothing = vq(features, centroids)
    elif mode == 2:
        centroids, index = kmeans2(features, k, iter=20, minit='random')
    centroids_list = []
    for i in range(len(centroids)):
        centroids_list.append(centroids[i][0]*0.299 + centroids[i][1]*0.587 + centroids[i][2]*0.114)
    for i in range(len(index)):
        index[i] = centroids_list[index[i]]
    # 用聚类标记创建图像
    codeim = index.reshape(steps, steps)
    codeim = imresize(codeim, im.shape[:2], 'nearest')
    return codeim


# stepsX*stepsY像素聚类
def clusterpixels_rectangular(img, k, stepsX, mode):
    im = img
    stepsY = stepsX * im.shape[1] // im.shape[0]

    # im.shape[0] 高 im.shape[1] 宽
    dx = im.shape[0] // stepsX
    dy = im.shape[1] // stepsY
    # 计算每个区域的颜色特征
    features = []
    for x in range(stepsX):
        for y in range(stepsY):
            R = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 0])
            G = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 1])
            B = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 2])
            features.append([R, G, B])
    features = array(features, 'f')     # 变为数组
    # 根据mode决定聚类初始化方式.聚类,k是聚类数目,code是每个点所对应的聚类标记序号
    if mode == 1:
        centroids, nothing = kmeans(features, k)
        index, nothing = vq(features, centroids)
    elif mode == 2:
        centroids, index = kmeans2(features, k, iter=20, minit='random')
    centroids_list = []
    for i in range(len(centroids)):
        centroids_list.append(centroids[i][0]*0.299 + centroids[i][1]*0.587 + centroids[i][2]*0.114)
    for i in range(len(index)):
        index[i] = centroids_list[index[i]]
    # 用聚类标记创建图像
    codeim = index.reshape(stepsX, stepsY)
    codeim = imresize(codeim, im.shape[:2], 'nearest')
    return codeim


# 计算最优steps 为保证速度以及减少噪点 最大值为maxsteps 其值为最接近且小于maxsteps 的x边长的约数
def getfirststeps(img, maxsteps):
    msteps = img.shape[0]
    n = 2
    while msteps > maxsteps:

        msteps = img.shape[0]//n
        n = n + 1
    return msteps


def gif_text(text, img_width, img_height):
    text_array = Image.new("L", (img_width, img_height), 255)
    dr = ImageDraw.Draw(text_array)
    font = ImageFont.truetype("simhei.ttf", 40)
    dr.text((0.45 * img_width, 5), text, font=font, fill="#000000")
    text_array = array(text_array)
    return text_array


def Test(file_path, k, k_top):

    # 图像文件 路径
    infiles = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            infiles.append(os.path.join(root, file))

    # 读取原图,根据参数生成对应的聚类结果,并将聚类结果合成为GIF文件
    for i in range(len(infiles)):
        img = Image.open(infiles[i])
        img_colorL = array(img.convert('L'))
        img = array(img)
        text_array = np.hstack((gif_text('原图的灰阶图', img.shape[1], 60), gif_text('矩形采样,随机', img.shape[1], 60), gif_text('优化采样,随机', img.shape[1], 60),
                                gif_text('矩形采样,高斯', img.shape[1], 60), gif_text('优化采样,高斯', img.shape[1], 60)))
        # img_colorL = np.vstack((text_array, np.hstack((img_colorL, img_colorL, img_colorL, img_colorL))))

        # 对原图执行k_top次聚类算法,并将结果矩阵保存在frames中
        frames = []
        for j in range(k_top):
            # 初始化聚簇中心的方式为:随机指定K个数据点作为聚簇中心
            # # 用改良矩形块对图片的像素进行聚类
            newim = clusterpixels_rectangular(img, j+1, getfirststeps(img, 128), 1)
            # 方形块对图片的像素进行聚类
            oldim = clusterpixels_square(img, j+1, 100, 1)

            # 初始化聚簇中心的方式为:通过估计数据的正态分布生成K个聚簇中心
            newim2 = clusterpixels_rectangular(img, j + 1, getfirststeps(img, 128), 2)
            # 方形块对图片的像素进行聚类
            oldim2 = clusterpixels_square(img, j+1, 100, 2)

            frames.append(np.hstack((img_colorL, oldim, newim, oldim2, newim2)))
            # 生成gif说明图片,转换为矩阵和两个聚类结果矩阵堆叠

        # save them as jpg_array into a jpg
        jpg_array = text_array
        for j in range(len(frames)):
            merge_array = gif_text("K=" + str(j + k), 5 * img.shape[1], 60)
            jpg_array = np.vstack((jpg_array, np.vstack((merge_array, frames[j]))))
        imageio.imwrite("C:\\Users\zzp\PycharmProjects\\"+str(i)+".jpg", jpg_array)

        # Save them as gif_frames into a gif
        for j in range(len(frames)):
            merge_array = np.vstack((gif_text("K=" + str(j + k), 5 * img.shape[1], 60), text_array))
            frames[j] = np.vstack((merge_array, frames[j]))
        imageio.mimsave("C:\\Users\zzp\PycharmProjects\\"+str(i)+".gif", frames, 'GIF', duration=1)


Test("C:\\Users\zzp\PycharmProjects\图片\原图", 1, 30)

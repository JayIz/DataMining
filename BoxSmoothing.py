import numpy as np
import copy

#数据导入，并进行异常点检测
def binning(filename,box_num):

    #数据导入及排序
    my_list = []
    noise_data = open(filename)
    for line in noise_data.readlines():
        dataline=line.strip()
        my_list.append(dataline)
    for i in range(0,len(my_list)):
        my_list[i]=int(my_list[i])
    my_list1=sorted(my_list)

    #异常点检测，使用箱型图分析
    Q1 = np.percentile(my_list1, 25)
    Q3 = np.percentile(my_list1, 75)
    IQR = Q3 - Q1
    step = 1.5 * IQR
    for nu in my_list1:
        if (nu < Q1 - step) | (nu > Q3 + step):
            my_list1.remove(nu)     #异常点直接去除
    #print (my_list1)

    #分箱
    box_list=[]
    len_box=int(np.ceil(len(my_list1)/float(box_num)))
    for i in range(0,box_num):
        each_box=my_list1[i*len_box:(i+1)*len_box]
        box_list.append(each_box)
    print('分箱结果：')
    print(box_list)

    return box_list

#平均值平滑
def box_mean_smooth(box_list_mean):

    for i in range(0,len(box_list_mean)):
        box_avg=int(np.average(box_list_mean[i]))
        for j in range(0,len(box_list_mean[i])):
            box_list_mean[i][j]=box_avg
    print('平均值平滑：')
    print(box_list_mean)

#中值平滑
def box_mid_smooth(box_list_mid):

    for i in range(0,len(box_list_mid)):
        box_mid=int(np.median(box_list_mid[i]))
        for j in range(0,len(box_list_mid[i])):
            box_list_mid[i][j]=box_mid
    print('中值平滑：')
    print(box_list_mid)

#边界值平滑
def box_boundary_smooth(box_list_boundary):

    for i in range(0,len(box_list_boundary)):
        left_bdy=box_list_boundary[i][0]
        right_bdy=box_list_boundary[i][-1]
        for j in range(0,len(box_list_boundary[i])):
            if abs(box_list_boundary[i][j]-left_bdy)<abs(box_list_boundary[i][j]-right_bdy):
                box_list_boundary[i][j]=left_bdy
            else:
                box_list_boundary[i][j]=right_bdy
    print('边界值平滑：')
    print(box_list_boundary)

#主函数
def main():

    filename= 'BoxSmoothing.txt'
    box_list=binning(filename,9)

    #将分箱后的列表拷贝给三个变量
    box_list_mean=copy.deepcopy(box_list)
    box_list_mid=copy.deepcopy(box_list)
    box_list_boundary=copy.deepcopy(box_list)
    #输出平滑结果
    box_mean_smooth(box_list_mean)
    box_mid_smooth(box_list_mid)
    box_boundary_smooth(box_list_boundary)

if __name__ == '__main__':
    main()

#创建database
samples = [
    ["A","C","D"],
    ["B","C","E"],
    ["A","B","C","E"],
    ["B","E"]
]

min_support = 1     #最小的支持度
min_confidence = 0.4    #最小的可信度
fre_list = list()


def get_c1():
    global record_list
    global record_dict
    new_dict = dict()

    #生成候选1项集
    for row in samples:
        for item in row:
            if item not in fre_list:
                fre_list.append(item)
                new_dict[item] = 1
            else:
                new_dict[item] = new_dict[item] + 1
    fre_list.sort()
    print ("candidate set:")
    print (dict(new_dict))

    #生成频繁1项集
    for key in fre_list:
        if new_dict[key] < min_support:
            del new_dict[key]
    print ("after pruning:")
    print (dict(new_dict))
    record_list = fre_list
    record_dict = record_dict

#自连接获取候选集
def get_candidateset():
    new_list = list()
    #自连接
    for i in range(0,len(fre_list)):
        for j in range(0,len(fre_list)):
            if i == j:
                continue
            #如果两个k项集可以自连接，必须保证它们有k-1项是相同的
            if has_samesubitem(fre_list[i],fre_list[j]):
                curitem = fre_list[i] + ',' + fre_list[j]
                curitem = curitem.split(",")
                curitem = list(set(curitem))
                curitem.sort()
                curitem = ','.join(curitem)
                #如果一个k项集要成为候选集，必须保证它的所有子集都是频繁的
                if has_infresubset(curitem) == False and already_constains(curitem,new_list) == False:
                    new_list.append(curitem)
    new_list.sort()
    return new_list

def has_samesubitem(str1,str2):
    str1s = str1.split(",")
    str2s = str2.split(",")
    if len(str1s) != len(str2s):
        return False
    nums = 0
    for items in str1s:
        if items in str2s:
            nums += 1
            str2s.remove(items)
    if nums == len(str1s) - 1:
        return True
    else:
        return False

#计算CK在数据集D中的支持度，并返回支持度大于min_support的数据集
def judge(candidatelist):
    # 计算候选集的支持度
    new_dict = dict()
    for item in candidatelist:
        new_dict[item] = get_support(item)
    print ("candidate set:")
    print (dict(new_dict))
    #剪枝
    #频繁集的支持度要大于最小支持度
    new_list = list()
    for item in candidatelist:
        if new_dict[item] < min_support:
            del new_dict[item]
            continue
        else:
            new_list.append(item)
    global fre_list
    fre_list = new_list
    print ("after pruning:")
    print (dict(new_dict))
    return new_dict


def has_infresubset(item):
    # 由于是逐层搜索的，所以对于Ck候选集只需要判断它的k-1子集是否包含非频繁集即可
    subset_list = get_subset(item.split(","))
    for item_list in subset_list:
        if already_constains(item_list,fre_list) == False:
            return True
    return False

#计算支持度
def get_support(item,splitetag=True):
    if splitetag:
        items = item.split(",")
    else:
        items = item.split("^")
    support = 0
    for row in samples:
        tag = True
        for curitem in items:
            if curitem not in row:
                tag = False
                continue
        if tag:
            support += 1
    return support

#获得itemset
def get_fullpermutation(arr):
    if len(arr) == 1:
        return [arr]
    else:
        newlist = list()
        for i in range(0,len(arr)):
            sublist = get_fullpermutation(arr[0:i]+arr[i+1:len(arr)])
            for item in sublist:
                curlist = list()
                curlist.append(arr[i])
                curlist.extend(item)
                newlist.append(curlist)
        return newlist

#获得项集的子集
def get_subset(arr):
    newlist = list()
    for i in range(0,len(arr)):
        arr1 = arr[0:i]+arr[i+1:len(arr)]
        newlist1 = get_fullpermutation(arr1)
        for newlist_item in newlist1:
            newlist.append(newlist_item)
    newlist.sort()
    newlist = remove_duplicate(newlist)
    return newlist

#移除重复的子集
def remove_duplicate(arr):
    newlist = list()
    for i in range(0,len(arr)):
        if already_constains(arr[i],newlist) == False:
            newlist.append(arr[i])
    return newlist


def already_constains(item,curlist):

    items = list()
    if type(item) ==str :
        items = item.split(",")
    else:
        items = item
    for i in range(0,len(curlist)):
        curitems = list()
        if type(curlist[i])==str :
            curitems = curlist[i].split(",")
        else:
            curitems = curlist[i]
        if len(set(items)) == len(curitems) and len(list(set(items).difference(set(curitems)))) == 0:
            return True
    return False

#主函数
if __name__ == '__main__':
    record_list = list()
    record_dict = dict()
    get_c1()
    # 不断进行自连接和剪枝，直到得到最终的频繁集为止;终止条件是，如果自连接得到的已经不再是频繁集
    # 那么取最后一次得到的频繁集作为结果
    while True:
        record_list = fre_list
        new_list = get_candidateset()
        judge_dict = judge(new_list)
        if len(judge_dict) == 0:
            break
        else:
            record_dict = judge_dict


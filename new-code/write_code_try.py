# 实现一个标准差函数
# 计算一组数据的标准差
# 参数：
#   data (list): 包含数值的列表
# 返回值：
#   float: 数据的标准差，如果列表为空则返回 0
def standard_deviation(data):
    if not data:  # 如果数据为空，返回 0
        return 0
    mean = sum(data) / len(data)  # 计算数据的均值
    squared_diffs = [(x - mean) ** 2 for x in data]  # 计算每个数据点与均值的差值的平方
    return (sum(squared_diffs) / len(data)) ** 0.5  # 计算方差并开平方得到标准差

#实现一个求中位数的函数
def median(data):
    if not data:
        return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]

# 测试标准差函数
if __name__ == "__main__":
    print("Running standard deviation tests...")
    # 运行测试
    test_data = [1, 2, 3, 4, 5]
    print("Test Standard Deviation:", standard_deviation(test_data))  # 输出标准差
    print("Test Median:", median(test_data))  # 输出中位数

    data = [10, 12, 23, 23, 16, 23, 21, 16]
    print("Standard Deviation:", standard_deviation(data))  # 输出标准差
    print("Median:", median(data))  # 输出中位数

    data_2 = [10, 12, 23, 23, 16, 23, 21, 16, 17]
    print("Standard Deviation:", standard_deviation(data))  # 输出标准差
    print("Median:", median(data_2))  # 输出中位数
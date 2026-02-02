def mergeMultiLists(lists):
    merged = []
    for lst in lists:
        merged.extend(lst)
    return merged





if __name__ == "__main__":
    # Example usage:
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    list3 = [True, False]
    all_lists = [list1, list2, list3]
    merged_list = mergeMultiLists(all_lists)
    print(merged_list)  # Output: [1, 2, 3, 'a', 'b', 'c', True, False]

    #生成5个列表变量，并初始化，每个列表包括2到10个元素
    list4 = [4, 5, 6]
    list5 = ['d', 'e', 'f']
    list6 = [False, True]
    all_lists_2 = [list1, list2, list3, list4, list5, list6]

    


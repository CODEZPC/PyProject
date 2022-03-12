def bubble(list1):
    if len(list1) <= 1:
        return list1
    else:
        for k in range(0, len(list1) - 1):
            for j in range(0, len(list1) - 1 - k):
                if list1[j] > list1[j + 1]:
                    a = list1[j]
                    list1[j] = list1[j + 1]
                    list1[j + 1] = a
        return list1

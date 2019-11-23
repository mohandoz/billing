




def find_rank (X):
    # spliting the text
    my_list = list(X.split(" "))

    # sort
    my_list.sort()

    # get unique
    unqiue_set = set(X)

    # convert to list
    unique_list = list(unqiue_set)

    # get len
    length = len(unique_list)

    sub_string = list()


    for i in range(length):
        for j in range(i, length):
            item = unique_list[i:j + 1]
            print(item)
            sub_string.append(item)


    sorted_sub_string = sub_string.sort()

    # i didn't know what the rank mean to calculate it

    return sorted_sub_string








x = "ereneeeeeeeeeeeeee"
find_rank(x)


# def get_all_substrings(input_string):
#   length = len(input_string)
#   return [input_string[i:j+1] for i in range(length) for j in range(i,length)]
#
# print (get_all_substrings('abcde'))

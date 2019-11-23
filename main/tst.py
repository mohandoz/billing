

class Cho:


    def __init__(self, numbers):
        self.numbers = numbers

    def clean(self):
        for i in self.numbers:
            print(i)
            print("")

    def __str__(self):
        return "hi"


# x = [2,6,1]

z = "125162"

obj = Cho(z)

obj.clean()

print(obj)

c = {"1": "val1", "2": "val2", "3":"val3"}


for key, val in c.items():
    print(key,val)
#
# for the_key, the_value in x.items():
#     print(the_key, 'corresponds to', the_value)

d = {'x': 1, 'y': 2, 'z': 3}
# for  key, value in d.items():
#    print( key, value)


v = [1, 2, 3, 4, 10, 11]


def simpleArraySum(*args):
    total = 0
    for x in args:
        total += x
        print(x)

    return total

simpleArraySum(*v)


def my_sum(*args):
    result = 0
    for x in args:
        result += x
    return result

list1 = [1, 2, 3]
list2 = [4, 5]
list3 = [6, 7, 8, 9]

print(my_sum(*list1, *list2, *list3))

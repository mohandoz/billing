def Solve(N,A):
    A.sort()

    last_val = A[-1]
    counter = -1

    # only one number
    if last_val != A[-2]:
        return last_val

    else:  # last num have more then one value
        while A[counter] == last_val:
           counter -= 1

    return A[counter]


# out  = Solve(8,[1, 2, 5, 3 ,3,4,4 ,5])
out  = Solve(8,[1, 2,3,4,4 ,5,5,5])

print(out)

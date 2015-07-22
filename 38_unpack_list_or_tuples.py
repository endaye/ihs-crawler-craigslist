# unpacking list
# number of variables must be equal number of list items
# from python cookbook
date, name, price = ['December 23, 2015', 'Bread Gloves', 8.51]
print(name)


# drop the first and last quiz grades, no mather how many quiz there are, and get the average grade.
def drop_first_last(grades):
    first, *middle, last = grades  # '*' is important
    avg = sum(middle) / len(middle)
    print(avg)

drop_first_last([65, 76, 98, 54, 21])
drop_first_last([65, 76, 98, 54, 21, 54, 65, 99, 88, 78])

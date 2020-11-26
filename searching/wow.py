import csv
from itertools import zip_longest
list1 = ['a', 'b', 'c', 'd', 'e']
list2 = ['f', 'g', 'i', 'j']
d = [list1, list2]
export_data = zip_longest(*d, fillvalue = '')
with open('numbers.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("List1", "List2"))
      wr.writerows(export_data)
myfile.close()

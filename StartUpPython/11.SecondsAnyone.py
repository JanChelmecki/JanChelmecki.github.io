time = input("Input time in the hh:mm:ss form: ")
h = int(time[:2:])
m = int(time[3:5:])
s = int(time[6::])
print("That is", 3600*h+60*m+s, "seconds.")

##ACS Good work
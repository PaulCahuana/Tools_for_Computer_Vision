import time
start = time.time() #tomamos medida del tiempo
end = time.time() #paramos el tiempo
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print()
print()
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

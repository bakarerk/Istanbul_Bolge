'''
>>matplotlib ile grafik çizdirme
import matplotlib.pyplot as plt
a = [1,2,3,4,5]
b =[0.1,0.2,0.3,0.4,0.5]
c = plt.plot(a,b)
plt.show()

>>exe ye çevirme
pyinstaller --onefile -w 'filename.py'

>>mevcut dosya folder:
import os
cwd = os.getcwd()

>>kod harcanan zamanı bulmak için
import time
t = time.process_time()
elapsed_time = time.process_time() - t
print("{}:{}".format(1,elapsed_time))
'''

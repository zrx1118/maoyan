dict = {}
dict['one'] = "1 - 菜鸟教程"
dict[2]     = "2 - 菜鸟工具"

tinydict = {'name': 'runoob','code':1, 'site': 'www.runoob.com'}


print (dict['one'])       # 输出键为 'one' 的值
print (dict[2])           # 输出键为 2 的值
print (tinydict)          # 输出完整的字典
print (tinydict.keys())   # 输出所有键
print (tinydict.values()) # 输出所有值

import sys
 
print('命令行参数如下:')
for i in sys.argv:
   print(i)

print('\n\nPython 路径为：', sys.path, '\n')
print(dir(sys))

for x in range(1, 11):
   print(repr(x).rjust(6), repr(x*x).rjust(3), end=' ')
   # 注意前一行 'end' 的使用
   print(repr(x*x*x).rjust(4))
   print(repr(x).ljust(6))
names = ['max', 'alina', 'sex', 'vladik']

# 1
print('---1---')
for name in names:
    print(len(name))

# 2
print('---2---')

for name in names:
    if len(name) > 5:
        print(name)
    

# 3
print('---3---')

for name in names:
    if 'n' in name or 'N' in name:
        print(name)

# 4 
print('---4---')

while len(names) > 0:
    names.pop()

print('empty')
print(names)

    
      
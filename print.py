token = ''

with open('keys') as keys:
    for  i in keys:
        token = i

print(token)

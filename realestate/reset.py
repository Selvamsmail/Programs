wrl = [0,7939]

for i in range(1,3):
    with open('real_comp_'+str(i)+'.txt', 'w') as file:
        file.write(str(wrl[i-1]))

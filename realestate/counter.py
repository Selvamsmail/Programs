
wrl = [0,7939]

l = []
for i in range(1,3):
    with open('real_comp_'+str(i)+'.txt', 'r') as file:
        st_rng = int(file.read())
        l.append(abs(st_rng-wrl[i-1]))

print(sum(l),'-',15879)
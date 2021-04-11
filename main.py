def do(sm):
    print(sm)

labels = [0, 1, 2]

funcs = [(l, lambda x=l: do(x)) for l in labels]

for l in labels:
    funcs.append(tuple([l, lambda: do(l)]))



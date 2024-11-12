from PIL import Image
import math
def haar_1d(arr:list[float]):
    hh = 128
    h = hh
    arr = [x / math.sqrt(hh) for x in arr]
    while h > 1:
        h = h // 2
        tAb = [x for x in arr]
        for x in range(h):
            tAb[x] = (arr[2*x] + arr[2*x + 1]) / math.sqrt(2)
            tAb[x+h] = (arr[2*x] - arr[2*x + 1]) / math.sqrt(2)
        arr = tAb
    return arr


SIZE_X = 128
SIZE_Y = SIZE_X

def apply_haar_on_matrix_col(maxtrix:list[list[float]]):
    for x in range(SIZE_X):
        arr = []
        for y in range(SIZE_Y):
            c = maxtrix[y][x]
            arr.append(c)
        arr = haar_1d(arr)
        for y in range(SIZE_Y):
            maxtrix[y][x] = arr[y]
    return maxtrix
def apply_haar_on_matrix_row(maxtrix:list[list[float]]):
    for x in range(SIZE_Y):
        arr = []
        for y in range(SIZE_X):
            c = maxtrix[y][x]
            arr.append(c)
        arr = haar_1d(arr)
        for y in range(SIZE_X):
            maxtrix[y][x] = arr[y]
    return maxtrix

def apply_haar_on_color(color:list[list[float]]):
    color = apply_haar_on_matrix_col(color)
    return apply_haar_on_matrix_row(color)

def flat(matrix:list[list]):
    r = []
    for m in matrix:
        r += m
    return r
def wv(o_im, Q=100):
    im = o_im.resize((SIZE_X,SIZE_Y))
    r = [[ im.getpixel((x,y))[0] for x in range(SIZE_X)] for y in range(SIZE_Y)]
    g = [[ im.getpixel((x,y))[1] for x in range(SIZE_X)] for y in range(SIZE_Y)]
    b = [[ im.getpixel((x,y))[2] for x in range(SIZE_X)] for y in range(SIZE_Y)]

    y = [[ (r*0.299 + g*0.587 + b*0.114)/256 for r,g,b in zip(ra,ga,ba)] for ra,ga,ba in zip(r,g,b)]
    i = [[ (r*0.596 + g*(-0.274) + b*(-0.322))/256 for r,g,b in zip(ra,ga,ba)] for ra,ga,ba in zip(r,g,b)]
    q = [[ (r*0.212 + g*(-0.523) + b*0.311)/256 for r,g,b in zip(ra,ga,ba)] for ra,ga,ba in zip(r,g,b)]


    # y = r*0.299 + g*0.587 + b*0.114
    # i = r*0.596 + g*(-0.274) + b*-0.322
    # q = r*0.212 + g*(-0.523) + b*0.311

    y = apply_haar_on_color(y)
    i = apply_haar_on_color(i)
    q = apply_haar_on_color(q)

    y = flat(y)
    i = flat(i)
    q = flat(q)

    y.sort(key=abs, reverse=True)
    i.sort(key=abs, reverse=True)
    q.sort(key=abs, reverse=True)
    return (y[:Q], i[:Q], q[:Q])

def comp(Im1:list[list[float]], Im2:list[list[float]]):
    assert len(Im1) == len(Im2)
    diff = 0
    for i1, i2 in zip(Im1,Im2):
        assert len(i1) == len(i2)
        for a1, a2 in zip(i1,i2):
            diff += abs(a1 - a2)
    # return math.sqrt(diff)
    return diff

def cossine(Im1:list[list[float]], Im2:list[list[float]]):
    Im1 = flat(Im1)
    Im2 = flat(Im2)
    # assert len(fm1) == len(fm2)
    diff = 0
    m_sum = sum(i1 * i2 for i1, i2 in zip(Im1,Im2))
    A_sum = sum(pow(i1,2) for i1 in Im1)
    B_sum = sum(pow(i2,2) for i2 in Im2)
    mul = math.sqrt(A_sum) * math.sqrt(B_sum)

    return m_sum/mul

    return diff

db: dict[str, tuple[int, int, int]] = {}

def open_calc(path:str):
    im = Image.open(path)
    im_comp = wv(im)
    db[path] = im_comp
    r = []
    for k,v in db.items():
        r.append((k, comp(im_comp,v)))
    r.sort(key=lambda x: x[1])
    for p in r:
        print(f"{p[0]:<16} : ",p[1])
    print("---------")
    return im_comp

# x = open_calc("95c.jpg")
# # x[0][4]
# open_calc("5aa.png")
# open_calc("100.jpg")
# open_calc("544700.jpg")
# open_calc("SUB.png")
# open_calc("507.jpg")
# crop_im.save("new.jpg")

import os
p = os.listdir()
for x in p:
    if x.endswith("jpg") or x.endswith("png") or x.endswith("webp"):
        print(x)
        open_calc(x)
print("*"*10)
for x in p:
    if x.endswith("jpg") or x.endswith("png") or x.endswith("webp"):
        print(x)
        open_calc(x)
from sklearn import tree
import mysql.connector
object=['brand','model' ,'weight' ,'cpu_brand' ,'cpu_seri' ,'cpu_model' ,'cpu_cache', 'ram'  ,'ram_type',
                   'hard' ,'hard_type','gpu_brand', 'gpu_model' ,'gpu_cap' ,'scr_res' ,'scr_touche' ]

cnx=mysql.connector.connect(user='root',password='224832',
                            host='localhost',
                            database='py')
mp={}
cnt=0

cursor=cnx.cursor()
cursor.execute('SELECT * FROM laptops')

for line in cursor:
    for info in line :
        if mp.get(info,0)==0 :
            cnt+=1
            if(type(info)==str):
                info=info.lower()
            mp[info]=cnt

x=[]
y=[]

cursor.execute('SELECT * FROM laptops')

for line in cursor:
    tmp=[]
    check=0
    for info in line[:-1]:
        check+=1
        if check==2:
            continue
        if type(info)==str :
            info=info.lower()
            tmp.append(mp[info])
        else :
            tmp.append(info)

    x.append(tmp)
    y.append(line[-1])

clf=tree.DecisionTreeClassifier()
clf = clf.fit(x,y)
new=[]
for i in object :
    if i=='model':
        continue
    tmp=input(i+' : ')
    try :
        tmp=float(tmp)
    except :
        tmp=tmp.lower()
        tmp=mp.get(tmp,0)
        while tmp==0:
            print('Wrong, Try again :')
            tmp=input()
            tmp = tmp.lower()
            tmp = mp.get(tmp, 0)
    new.append(tmp)

tmp=[]
tmp.append(new)
ans=clf.predict(tmp)
print(ans[0])

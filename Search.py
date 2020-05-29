import mysql.connector

cnx=mysql.connector.connect(user='root',password='224832',
                            host='localhost',
                            database='py')
cursor=cnx.cursor()

low=int(input('had aghal gheymat ra vared konid : '))
up=int(input('had aksar gheymat ra vared konid : '))

cursor.execute('SELECT * FROM laptops WHERE price>%i AND price<%i'%(low,up))

for i in cursor:
    print('brand : ',i[0])
    print('model : ',i[1])
    print('wei : ',i[2])
    print('cpu_brand : ',i[3])
    print('cpu_seri : ',i[4])
    print('cpu_model : ',i[5])
    print('cpu_cache : ',i[6])
    print('ram : ',i[7])
    print('ram_type : ',i[8])
    print('hard : ',i[9])
    print('hard_type : ',i[10])
    print('gpu_brand : ',i[11])
    print('gpu_model : ',i[12])
    print('gpu_cap : ',i[13])
    print('scr_res : ',i[14])
    print('scr_touch : ',i[15])
    print('price : ',i[16])
    print('NEXT ONE : ________________________________')
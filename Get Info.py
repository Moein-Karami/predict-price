#too poroje ma etalate tamam laptop haye mojood dar digikala ro
#be dast miyarim
#chon gheymate laptop ha besiyar moteghayere har bar table ro az
#no minevisism




import mysql.connector
import bs4
import requests
import re

def Create_Table():
    cursor.execute('SHOW TABLES;')
    check=False
    for line in cursor:
        if line[0]=='laptops':
            check=True
    if check:
        cursor.execute('DROP TABLE laptops;')
    cursor.execute('CREATE TABLE laptops(brand VARCHAR(100),'
                   'model VARCHAR(100),weight_kg FLOAT ,cpu_brand VARCHAR(100),'
                   'cpu_seri VARCHAR(100),cpu_model VARCHAR(100),'
                   'cpu_cache_mb INT, ram INT ,ram_type VARCHAR(100),'
                   'hard_gb INT ,hard_type VARCHAR(100),'
                   'gpu_brand VARCHAR(100), gpu_model VARCHAR(100),'
                   'gpu_cap_gb FLOAT,scr_res VARCHAR(100),'
                   'scr_touche_bool INT , price_tooman INT) ;')


cnx=mysql.connector.connect(user='root',password='224832',
                            host='localhost',
                            database='py')
cursor=cnx.cursor()
Create_Table()

cnt=1
cunt=0
main=requests.get('https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno=1&sortby=1')
main=bs4.BeautifulSoup(main.text,'html.parser')

while 1:

    all_laptops=main.find_all('a',attrs={'class':'c-product-box__img c-promotion-box__image js-url js-product-item',
                                         'target':'_blank',
                                         'data-snt-event':'dkProductClicked'})

    for link in all_laptops:

        page=requests.get('https://www.digikala.com'+link['href'])
        laptop=bs4.BeautifulSoup(page.text,'html.parser')

        #_____________________________________________________________________________get brand and model
        info = laptop.find('span',attrs={'class':'c-product__title-en'})
        info=info.text.strip().split()
        if len(info)==0:
            info=laptop.find('h1',attrs={'class':'c-product__title'})
            brand=info.text.strip()
            model=info.text.strip()
        else:
            brand=info[0]
            model=' '.join(info[1:])

        #___________________________________________________________________________get other info
        info=laptop.find_all('span',attrs={'class':'block'})
        for i in range(len(info)):
            if info[i].text.find('وزن')!=-1: #________________________________________WEIGHT
                i+=1
                wei=info[i].text.strip().split()
                wei=re.sub(r'/','.',wei[0])
                wei=float(wei)
            elif info[i].text.find('سازنده پردازنده گرافیکی')!=-1 : #______________________________GPU
                i+=1
                gpu_brand=info[i].text.strip()
                i+=2
                gpu_model=info[i].text.strip()
                gpu_model=re.sub(r'®','',gpu_model)
                i+=2
                gpu_cap=info[i].text.strip()
                bad=False
                if gpu_cap.find('MB')!=-1 :
                    bad=True
                gpu_cap=re.findall(r'\d+',gpu_cap)
                if len(gpu_cap)==0:
                    gpu_cap=0
                else:
                    gpu_cap=int(gpu_cap[0])
                if bad:
                  gpu_cap/=1000
            elif info[i].text.find('سازنده پردازنده')!=-1 :  #__________________________________CPU
                i+=1
                cpu_brand=info[i].text.strip().split()
                cpu_brand=cpu_brand[0]
                i+=2
                cpu_seri=info[i].text.strip().split('\n')
                cpu_seri=cpu_seri[0]
                i+=2
                cpu_model=info[i].text.strip()
                i+=6
                cpu_cache=info[i].text.strip().split()
                cpu_cache=int(cpu_cache[0])
            elif info[i].text.find('ظرفیت حافظه RAM')!=-1: #_________________________________RAM
                i+=1
                ram=info[i].text.strip().split()
                ram=int(ram[0])
                i+=2
                ram_type=info[i].text.strip()
            elif info[i].text.find('ظرفیت حافظه داخلی')!=-1 : #________________________________HARD
                i+=1
                tmp=info[i].text
                if tmp.find('ترابایت')!=-1:
                    if tmp.find('یک و نیم') !=-1:
                        hard=1500
                    elif tmp.find('یک') !=-1:
                        hard=1000
                    else:
                        hard=2000
                else:
                    hard=tmp.strip().split()
                    hard=int(hard[0])
                i+=2
                hard_type=info[i].text.strip()
            elif info[i].text.find('دقت صفحه نمایش')!=-1: #________________________________SCREEN
                i+=1
                scr_res=info[i].text.strip().split('\n')
                scr_res=scr_res[0]
                i+=4
                if info[i].text.find('بله') !=-1 :
                    scr_touch=1
                else :
                    scr_touch=0
        #___________________________________________________________________________get price

        info=laptop.find('a',attrs={'class':'btn-add-to-cart btn-add-to-cart--full-width js-add-to-cart js-cart-page-add-to-cart js-btn-add-to-cart',
                                    'data-event':'add_to_cart',
                                    'data-event-category':'ecommerce'})
        if info==None :
            continue
        price=info['data-event-label'].split()
        price=int(price[1])//10

        print(brand)
        print(model)
        print(wei)
        print(cpu_brand)
        print(cpu_seri)
        print(cpu_model)
        print(cpu_cache)
        print(ram)
        print(ram_type)
        print(hard)
        print(hard_type)
        print(gpu_brand)
        print(gpu_model)
        print(gpu_cap)
        print(scr_res)
        print(scr_touch)
        print(price)
        cunt+=1
        print('NEXT ONE ____________________________',cunt)
        cursor.execute('INSERT INTO laptops VALUES (\'%s\',\'%s\',%f,\'%s\',\'%s\',\'%s\',\'%s\',%i,\'%s\',%i'
                       ',\'%s\',\'%s\',\'%s\',%f,\'%s\',%i,%i)' %(brand,model,wei,cpu_brand,cpu_seri,cpu_model,cpu_cache,
                                                               ram,ram_type,hard,hard_type,gpu_brand,gpu_model,gpu_cap,
                                                               scr_res,scr_touch,price))
        cnx.commit()
    #break
    cnt+=1
    main = requests.get('https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno=%i&sortby=1' %cnt)
    main=bs4.BeautifulSoup(main.text,'html.parser')
    end=main.find('div',attrs={'class':'c-message-light__justify'})
    if end!=None:
        break

print('DONE')
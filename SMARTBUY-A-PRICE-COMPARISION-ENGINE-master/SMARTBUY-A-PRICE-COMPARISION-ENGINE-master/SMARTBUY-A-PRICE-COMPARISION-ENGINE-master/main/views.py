from django.shortcuts import render,redirect
from .models import Product_Database, dummy
from .forms import Search
from django.contrib import messages
from selenium import webdriver as wb
from bs4 import BeautifulSoup

def home(request):
  if request.method=='POST':
    fm=Search(request.POST)
    if fm.is_valid():
      name=fm.cleaned_data['name']
      return redirect('product',name)
  else:
    fm=Search()
  return render(request,'main/home.html', {'form':fm})

def product(request,product):  
  if request.method=='GET':
    options = wb.ChromeOptions()
    options.add_argument("headless")
    # driver = wb.Chrome(executable_path="C:\\Users\Sharan Prabhath\Downloads\chromedriver.exe",chrome_options=options)
    
    # driver = wb.Chrome(executable_path="C:\\Windows\chromedriver-win32\chromedriver-win32\chromedriver.exe",chrome_options=options)
    
    driver_path="C:\\Windows\chromedriver-win32\chromedriver-win32\chromedriver.exe"
    driver=wb.Chrome(options=options)
  
    
    Pname=product
    product_name = Pname.replace(" ","+")
    amazon_string = f'https://www.amazon.in/s?k={product_name}'
    driver.get(amazon_string)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find_all('div',{'data-component-type':'s-search-result'})
    price_list = []
    # print("Results are:",results)
    url = []
    description_list = []
    image_url = []
    for item in results:
      try:
        image_object = item.find('img')
        image = image_object.get('src')
        image_url.append(image)
        atag = item.h2.a
        description = atag.text.strip()
        description_list.append(description)
        redirection_URL = 'https://www.amazon.in' + atag.get('href')
        url.append(redirection_URL)
        price_parent_class = item.find('span','a-price')
        amazon_price = price_parent_class.find('span','a-offscreen').text
        # print("Amazon price are:",amazon_price)
        price = int(''.join(filter(lambda i: i.isdigit(), amazon_price)))
        # print("price is:",price)
        price_list.append(price)
        # print("price list is:",price_list)
        # break
      except:
        continue
    min_price = min(price_list)
    amazonP=min_price
    linkA=url[price_list.index(min_price)]
    imag_url= image_url[price_list.index(min_price)]

    # flipkart
    flipkart_string = f'https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    driver.get(flipkart_string)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find_all('div',{'class':'_1AtVbE col-12-12'})
    price_list = []
    url = []
    description_list = []
    for item in results:
      try:
        atag = item.a
        div_des = atag.find('div',{'class':'_4rR01T'})
        description = div_des.text.strip()
        description_list.append(description)
        redirection_URL = 'https://www.flipkart.com'+ atag.get('href')
        url.append(redirection_URL)
        flipkart_price = atag.find('div',{'class':'_30jeq3 _1_WHN1'}).text
        price = int(''.join(filter(lambda i: i.isdigit(), flipkart_price)))
        price_list.append(price)
        # break
      except:
        continue
        
    min_price = min(price_list)
    flipkartP=min_price
    linkF= url[price_list.index(min_price)]
    linkC= url[price_list.index(min_price)]
    des=description_list[price_list.index(min_price)]

    
    # croma_string = f'https://croma.com/search/?text={product_name}'
    # print("croma",croma_string)
    # driver.get(croma_string)
    # soup = BeautifulSoup(driver.page_source,'html.parser')
    # print("soup",soup)
    # results = soup.find_all('li',{'class':'product-item'})
    # print("results:",results)
    # print("hello mr.chaand")
    # price_list = []
    # url = []
    # description_list = []
    # for item in results:
    #   try:
    #     atag = item.h3.a
    #     description = atag.text.strip()
    #     description_list.append(description)
    #     redirection_URL = 'https://www.croma.com' + atag.get('href')
    #     url.append(redirection_URL)
    #     croma_price = item.find('span',{'data-testid':'price'}).text
    #     price = int(int(''.join(filter(lambda i: i.isdigit(), croma_price)))/100)
    #     print("Price is:",price)
    #     price_list.append(price)
    #     print("Price liist:",price_list)
    #     break
    #   except:
    #     continue
    # min_price = min(price_list)
    # cromaP=min_price
    # linkC=url[price_list.index(min_price)]

    driver.quit()

    fm={
      'pname':Pname,
      'des':des,
      'imagurl':imag_url,
      'linkA':linkA,
      'linkF':linkF,
      'linkC':linkC,
      'priceA':amazonP,
      'priceF':flipkartP,
      'priceC':flipkartP,
      'fm2':Search(),
    }
    obj=dummy(id=1,des=des,imag_url=imag_url,linkA=linkA,linkC=linkC,linkF=linkF,amazonP=amazonP,flipkartP=flipkartP,cromaP=flipkartP)
    obj.save()
    
    return render(request,'main/product.html',fm)
  else:
      Pname=product
      pro=Product_Database.objects.filter(email=request.user.email,product_name=Pname)
      if pro.exists():
        pro.delete()
      obj=dummy.objects.get(id=1)
      pro1=Product_Database( email= request.user.email, name='amazon', price=obj.amazonP,product_name=Pname, link=obj.linkA)
      pro1.save()
      pro2=Product_Database( email= request.user.email, name='flipkart', price=obj.flipkartP,product_name=Pname, link=obj.linkF)
      pro2.save()
      pro3=Product_Database( email= request.user.email, name='croma', price=obj.cromaP,product_name=Pname, link=obj.linkC)
      pro3.save()

      data={'p': Pname,'a': obj.linkA, 'f': obj.linkF, 'c': obj.linkC , 'pA': obj.amazonP,'pF': obj.flipkartP,'pC': obj.cromaP}
      fm={
        'pname':Pname,
        'des':obj.des,
        'imagurl':obj.imag_url,
        'linkA':obj.linkA,
        'linkF':obj.linkF,
        'linkC':obj.linkC,
        'priceA':obj.amazonP,
        'priceF': obj.flipkartP,
        'priceC': obj.cromaP,
        'fm2':Search(),
      }
      messages.info(request,'success')
      return render(request,'main/product.html',fm)


def p_list(request,search):
  List=[]
  options = wb.ChromeOptions()
  options.add_argument("headless")
  # driver = wb.Chrome(executable_path="C:\\Users\Sharan Prabhath\Downloads\chromedriver.exe",chrome_options=options)
  
  # driver = wb.Chrome(executable_path="C:\Windows\chromedriver-win32\chromedriver-win32\chromedriver.exe",chrome_options=options)
  
  driver_path="C:\Windows\chromedriver-win32\chromedriver-win32\chromedriver.exe"
  driver=wb.Chrome(options=options)
  
  # product_name = search.replace(" ","+")
  # croma_string = f'https://croma.com/search/?text={product_name}'
  # driver.get(croma_string)
  # #time.sleep(10)
  # soup = BeautifulSoup(driver.page_source,'html.parser')
  # results = soup.find_all('li',{'class':'product-item'})
  # #time.sleep(20)
  # print('total results: ', len(results))
  # price_list = []
  # url = []
  # description_list = []
  # image_url = []
  # for item in results:
  #   try:
  #     image_object = item.find('img')
  #     image = image_object.get('src')
  #     image_url.append(image)
  #     atag = item.h3.a
  #     description = atag.text.strip()
  #     description_list.append(description)
  #     redirection_URL = 'https://www.croma.com' + atag.get('href')
  #     url.append(redirection_URL)
  #     croma_price = item.find('span',{'data-testid':'price'}).text
  #     price = (int(''.join(filter(lambda i: i.isdigit(), croma_price))))/100
  #     price_list.append(price)
  #   except:
  #     continue

  # for iterator in range(len(description_list)):
  #   try:
  #     List.append({
  #       'number':number+1,
  #       'des_list': description_list[iterator],
  #       'price':price_list[iterator],
  #       'imag_url':image_url[iterator],
  #       'link':url[iterator],
  #     })
  #     print(iterator)
  #   except:
  #     continue
    
  ## for amazon
  product_name = search.replace(" ","+")
  amazon_string = f'https://www.amazon.in/s?k={product_name}'
  driver.get(amazon_string)
  soup = BeautifulSoup(driver.page_source,'html.parser')
  results = soup.find_all('div',{'data-component-type':'s-search-result'})
  print('total results: ',len(results))
  price_list = []
  url = []
  description_list = []
  image_url = []
  for item in results:
    try:
      image_object = item.find('img')
      image = image_object.get('src')
      image_url.append(image)
      atag = item.h2.a
      description = atag.text.strip()
      s=description.split("(",1)
      s=s[0]
      description_list.append(s)
      redirection_URL = 'https://www.amazon.in' + atag.get('href')
      url.append(redirection_URL)
      price_parent_class = item.find('span','a-price')
      amazon_price = price_parent_class.find('span','a-offscreen').text
      price = int(''.join(filter(lambda i: i.isdigit(), amazon_price)))
      price_list.append(price)
    except:
      continue

  for iterator in range(len(description_list)):
    try:
      List.append({
        'des_list': description_list[iterator],
        'price':price_list[iterator],
        'imag_url':image_url[iterator],
        'link':url[iterator],
      })
    except:
      continue
  driver.quit()  
  return render(request, 'main/productlist.html',{'data':List, 'fm2': Search()})




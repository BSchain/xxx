# -*- coding: utf-8 -*-
# @Time    : 01/02/2018 4:25 PM
# @Author  : 伊甸一点
# @FileName: function.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from django.db import connection
from BSCapp.root_chain.utils import *
from BSCapp.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def generate_sort_sql(table_name, sort_name, sort_type):
    sort_sql = 'order by ' + table_name + '.' + sort_name+' '+sort_type+';'
    return sort_sql

def buyData_sql(request, buyer_id, sort_sql):
    context = {}
    cursor = connection.cursor()

    sql = 'select data_id, user_id, data_name, data_info, timestamp, ' \
          'data_tag, data_status, data_md5, data_size, data_price, data_address ' \
          'from BSCapp_data where BSCapp_data.user_id != %s and BSCapp_data.data_status = 1 '
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'and {} like %s '.format(search_base)
    except Exception as e:
        print(e) 
    sql = sql + search_sql + sort_sql
    try:
        if search_sql:
            cursor.execute(sql, [buyer_id, "%"+search_field+"%"])
        else:
            cursor.execute(sql, [buyer_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(e)
        cursor.close()
        return context
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['data_id'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1]).user_name
        data['seller'] = seller
        data['name'] = content[i][2]
        data['info'] = content[i][3]
        data['timestamp'] = time_to_str(content[i][4])
        data['tag'] = content[i][5]
        data['md5'] = content[i][7]
        data['size'] = content[i][8]
        data['price'] = content[i][9]
        data['address'] = content[i][10]
        datas.append(data)
    return datas

def orderData_sql(request, user_id, sort_sql):

    context = {}
    cursor = connection.cursor()
    sql = 'select BSCapp_data.data_id,BSCapp_data.user_id, BSCapp_data.data_name, BSCapp_data.data_info,BSCapp_data.data_source,' \
          'BSCapp_data.data_type, BSCapp_transaction.timestamp, BSCapp_transaction.price, BSCapp_data.data_address from BSCapp_data \
          ,BSCapp_transaction where BSCapp_data.data_id = BSCapp_transaction.data_id and BSCapp_transaction.buyer_id = %s '
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'and {} like %s '.format(search_base)
    except:
        pass
    sql = sql + search_sql + sort_sql
    try:
        if search_sql:
            cursor.execute(sql, [user_id, "%"+search_field+"%"])
        else:
            cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(e)
        cursor.close()
        return context
    
    orders = []
    len_content = len(content)
    for i in range(len_content):
        order = dict()
        order['dataid'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1])
        order['seller'] = seller.user_name
        order['name'] = content[i][2]
        order['info'] = content[i][3]
        order['source'] = content[i][4]
        order['type'] = content[i][5]
        order['timestamp'] = time_to_str(content[i][6])
        order['price'] = content[i][7]
        order['address'] = content[i][8]
        orders.append(order)
    return orders

def uploadData_sql(user_id):
    context = {}
    cursor = connection.cursor()
    sql = 'select data_name, data_info, timestamp, data_tag, data_download, data_status, data_purchase, data_price ' \
          'from BSCapp_data where BSCapp_data.user_id = %s order by timestamp DESC;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
        return context
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['name'] = content[i][0]
        data['info'] = content[i][1]
        data['timestamp'] = time_to_str(content[i][2])
        data['tag'] = content[i][3]
        data['download'] = content[i][4]
        # status = 0 审核中
        # status = 1 审核通过
        # status = 2 审核不通过
        # data['status'] = content[i][5]
        if content[i][5] == 0:
            data['status'] = '审核中'
        elif content[i][5] == 1:
            data['status'] = '审核通过'
        else:
            data['status'] = '审核不通过'
        data['purchase'] = content[i][6]
        data['price'] = content[i][7]
        datas.append(data)
    return datas

def adminData_sql(sort_sql, request):
    cursor = connection.cursor()
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'where {} like %s '.format(search_base)
    except Exception as e:
        print(e)
    
    sql = 'select data_id, user_id, data_name, data_info, timestamp,  \
           data_source, data_type, data_status, data_price from BSCapp_data '
    sql = sql + search_sql + sort_sql
    try:
        if search_sql:
            cursor.execute(sql, ["%"+search_field+"%"])
        else:
            cursor.execute(sql) 
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
        return {}
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['dataid'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1])
        data['seller'] = seller.user_realName
        data['name'] = content[i][2]
        data['info'] = content[i][3]
        data['timestamp'] = time_to_str(content[i][4])
        data['source'] = content[i][5]
        data['type'] = content[i][6]
        if content[i][7] == 0:
            data['status'] = '审核中'
        elif content[i][7] == 1:
            data['status'] = '审核通过'
        else:
            data['status'] = '审核不通过'
        data['price'] = content[i][8]
        datas.append(data)
    return datas

def rechargeData_sql(user_id):
    content = {}
    cursor = connection.cursor()
    sql = 'select timestamp,credits,before_account,after_account from BSCapp_recharge where BSCapp_recharge.user_id = %s order by timestamp DESC;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    recharges = []
    for i in range(len(content)):
        recharge = dict()
        recharge['timestamp'] = time_to_str(content[i][0])
        recharge['credits'] = content[i][1]
        recharge['before_account'] = content[i][2]
        recharge['after_account'] = content[i][3]
        recharges.append(recharge)
    return recharges

def pagingData(request, datas, each_num):
    paginator = Paginator(datas, each_num)
    page = request.GET.get('page', 1)
    try:
        paged_recharges = paginator.page(page)
    except PageNotAnInteger:
        paged_recharges = paginator.page(1)
    except EmptyPage:
        paged_recharges = paginator.page(paginator.num_pages)
    return paged_recharges


def GetAccount(user_id):
    #get the wallet account
    content = {}
    cursor = connection.cursor()
    sql = 'select account from BSCapp_wallet where BSCapp_wallet.user_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    return content[0][0]

def GetUploadData(user_id):
    #get upload data
    content = {}
    cursor = connection.cursor()
    sql = 'select data_id from BSCapp_data where BSCapp_data.user_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    return content

def GetPurchaseData(user_id):
    #get purchase data
    content = {}
    cursor = connection.cursor()
    sql = 'select data_id from BSCapp_purchase where BSCapp_purchase.user_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    return content

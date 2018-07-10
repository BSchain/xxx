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
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class JuncheePaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=4, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num

    def page(self, number):
        self.page_num = (int)(number)
        return super(JuncheePaginator, self).page(number)

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
            return range(1, self.num_pages + 1)
        num_list = []
        num_list.append(self.page_num)
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)

            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)
        num_list.sort()
        return num_list

    page_range_ext = property(_page_range_ext)

def generate_sort_sql(table_name, sort_name, sort_type):
    sort_sql = 'order by ' + table_name + '.' + sort_name+' '+sort_type+';'
    return sort_sql

def buyData_sql(request, buyer_id, sort_sql):
    context = {}
    cursor = connection.cursor()

    sql = 'select data_id, user_id, data_name, data_info, timestamp, ' \
          'first_title, second_title, data_type, data_size ' \
          'from BSCapp_sciencedata where BSCapp_sciencedata.user_id != %s and BSCapp_sciencedata.data_status = 1 '
    search_sql = ''

    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'and {} like %s '.format(search_base)
    except Exception as e:
        # print(e)
        pass
    sql = sql + search_sql + sort_sql
    try:
        if search_sql:
            cursor.execute(sql, [buyer_id, "%"+search_field+"%"])
        else:
            cursor.execute(sql, [buyer_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return context
    datas = []
    len_content = len(content)

    for i in range(len_content):
        data = dict()
        data['data_id'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1]).user_name
        data['user_id'] = seller
        data['data_name'] = content[i][2]
        data['data_info'] = content[i][3]
        data['timestamp'] = time_to_str(content[i][4])
        data['first_title'] = content[i][5]
        data['second_title'] = content[i][6]
        data['data_type'] = content[i][7]
        data_size = content[i][8]

        if data_size < 1:
            data['data_size'] = str(round(data_size * 1024.0, 3)) + ' KB'
        else:
            data['data_size'] = str(round(data_size, 3)) + ' MB'
        datas.append(data)
    return datas, len_content

def orderData_sql(request, user_id, sort_sql):

    context = {}
    cursor = connection.cursor()
    sql = 'select BSCapp_data.data_id,BSCapp_data.user_id, BSCapp_data.data_name, BSCapp_data.data_info,BSCapp_data.data_source,' \
          'BSCapp_data.data_type, BSCapp_transaction.timestamp, BSCapp_transaction.price, BSCapp_data.data_address, ' \
          'BSCapp_data.data_score, BSCapp_data.comment_number, BSCapp_transaction.data_score ' \
          'from BSCapp_data, BSCapp_transaction ' \
          'where BSCapp_data.data_id = BSCapp_transaction.data_id and BSCapp_transaction.buyer_id = %s '
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
        # print(e)
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
        data_avg_score = content[i][9]
        comment_number = content[i][10]
        if comment_number == 0 or data_avg_score == 0.0:
            order['avg_score'] = '0 (暂无评级)'
            order['comment_number'] = '0 '
        else:
            order['avg_score'] = data_avg_score
            order['comment_number'] = comment_number
        data_score = content[i][11]
        if data_score ==0:
            order['self_score'] = 0
        else:
            order['self_score'] = data_score

        orders.append(order)
    return orders

def uploadData_sql(request, user_id, sort_sql):
    context = {}
    cursor = connection.cursor()
    sql = 'select data_name, data_info, timestamp, first_title, second_title, ' \
          'data_type, data_status, data_size ' \
          'from BSCapp_sciencedata where BSCapp_sciencedata.user_id = %s '
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'and {} like %s '.format(search_base)
    except:
        pass
    sql = sql + search_sql + sort_sql
    # print(sql)
    try:
        if search_sql:
            cursor.execute(sql, [user_id, "%" + search_field + "%"])
        else:
            cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return context
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['data_name'] = content[i][0]
        data['data_info'] = content[i][1]
        data['timestamp'] = time_to_str(content[i][2])
        data['first_title'] = content[i][3]
        data['second_title'] = content[i][4]
        data['data_type'] = content[i][5]
        # status = 0 审核中
        # status = 1 审核通过
        # status = 2 审核不通过
        if content[i][6] == 0:
            data['data_status'] = '审核中'
        elif content[i][6] == 1:
            data['data_status'] = '审核通过'
        else:
            data['data_status'] = '审核不通过'
        data['data_size'] = content[i][7]
        data_size = data['data_size']
        if data_size < 1 :
            data['data_size'] = str(round(data_size * 1024.0,3)) + ' KB'
        else:
            data['data_size'] = str(round(data_size, 3)) + ' MB'

        datas.append(data)
    return datas, len_content

def adminData_sql(request, sort_sql):
    cursor = connection.cursor()
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'where {} like %s '.format(search_base)
    except Exception as e:
        # print(e)
        pass
    sql = 'select data_id, user_id, timestamp, data_name, data_source,   \
           data_info, data_type, first_title, second_title, data_status, data_size ' \
          ' from BSCapp_sciencedata '
    sql = sql + search_sql + sort_sql
    # print(sql)
    try:
        if search_sql:
            cursor.execute(sql, ["%"+search_field+"%"])
        else:
            cursor.execute(sql) 
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return {}
    datas = []
    len_content = len(content)
    for i in range(len_content):
        data = dict()
        data['data_id'] = content[i][0]
        seller = User.objects.get(user_id=content[i][1])
        data['user_id'] = seller.user_name
        data['timestamp'] = time_to_str(content[i][2])
        data['data_name'] = content[i][3]
        data['data_source'] = content[i][4]
        data['data_info'] = content[i][5]
        data['data_type'] = content[i][6]
        data['first_title'] = content[i][7]
        data['second_title'] = content[i][8]

        if content[i][9] == 0:
            data['data_status'] = '审核中'
        elif content[i][9] == 1:
            data['data_status'] = '审核通过'
        else:
            data['data_status'] = '审核不通过'

        data['data_size'] = round((float)(content[i][10]),5)
        data_size = data['data_size']
        if data_size < 1 :
            data['data_size'] = str(round(data_size * 1024.0,3)) + ' KB'
        else:
            data['data_size'] = str(round(data_size , 3)) + ' MB'
        datas.append(data)

    return datas

def txLog_sql(user_id):
    content = {}
    cursor = connection.cursor()
    sql = 'select science_data_id, timestamp, action ' \
          'from BSCapp_downloadLog where BSCapp_downloadLog.user_id = %s order by timestamp DESC;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    tx_logs = []
    for i in range(len(content)):
        tx_log = dict()
        sciencd_data = ScienceData.objects.get(data_id=content[i][0])
        tx_log['science_data_id'] = sciencd_data.data_name
        tx_log['timestamp'] = time_to_str(content[i][1])
        tx_log['first_title'] = sciencd_data.first_title
        tx_log['second_title'] = sciencd_data.second_title
        tx_log['data_source'] = sciencd_data.data_source
        tx_log['data_type'] = sciencd_data.data_type
        tx_log['action'] = content[i][2]
        tx_logs.append(tx_log)
    return tx_logs
#
# def rechargeData_sql(user_id):
#     content = {}
#     cursor = connection.cursor()
#     sql = 'select timestamp,credits,before_account,after_account from BSCapp_recharge where BSCapp_recharge.user_id = %s order by timestamp DESC;'
#     try:
#         cursor.execute(sql, [user_id])
#         content = cursor.fetchall()
#         cursor.close()
#     except Exception as e:
#         cursor.close()
#     recharges = []
#     for i in range(len(content)):
#         recharge = dict()
#         recharge['timestamp'] = time_to_str(content[i][0])
#         recharge['credits'] = content[i][1]
#         recharge['before_account'] = content[i][2]
#         recharge['after_account'] = content[i][3]
#         recharges.append(recharge)
#     return recharges


def noticeData_sql(user_id, sort_sql):
    content = {}
    cursor = connection.cursor()
    sql = 'select notice_id, sender_id, notice_type, notice_info, timestamp, if_check from BSCapp_notice where receiver_id = %s and if_delete = False '

    sql = sql + sort_sql
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        # print(e)
        cursor.close()
        return content
    notices = []
    len_content = len(content)
    unread_number = 0
    unread_notices = []
    show_unread_number = 5

    for i in range(len_content):
        notice = dict()
        notice['notice_id'] = content[i][0]
        sender_id = content[i][1]
        notice_type = content[i][2]
        if notice_type == 1 or notice_type == 2: # review pass or reject
            notice['sender'] = Admin.objects.get(admin_id=sender_id).admin_name
        elif notice_type == 3 or  notice_type == 4: # recharge success
            notice['sender'] = '系统'
        else:
            notice['sender'] = '系统'
        notice['info'] = content[i][3]
        notice['timestamp'] = time_to_str(content[i][4])
        if_check= content[i][5]
        if if_check == True:
            notice['if_check'] = '已读'
        else:
            notice['if_check'] = '未读'
            unread_number+=1
            if (unread_number <= show_unread_number):
                unread_notices.append(notice)
        notices.append(notice)

    return notices, unread_notices, unread_number

# Done add config number = 7
def pagingData(request, datas, each_num=7):
    # paginator = Paginator(datas, each_num)
    # print(each_num)
    paginator = JuncheePaginator(datas, each_num)
    page = request.GET.get('page', 1)
    try:
        paged_recharges = paginator.page(page)
    except PageNotAnInteger:
        paged_recharges = paginator.page(1)
    except EmptyPage:
        paged_recharges = paginator.page(paginator.num_pages)
    return paged_recharges


def get_notices(request, user_id):
    Notice_sort_name_and_type = request.session['Notice_sort_name_and_type']
    result = Notice_sort_name_and_type.split('&')
    default_sort_name = result[0]
    default_sort_type = result[1]

    table_name = 'BSCapp_notice'
    sort_sql = generate_sort_sql(table_name, default_sort_name, default_sort_type)
    notices, unread_notices, unread_number = noticeData_sql(user_id, sort_sql)
    return notices, unread_notices, unread_number

def GetUploadData(user_id):
    #get upload data
    content = {}
    cursor = connection.cursor()
    sql = 'select data_id from BSCapp_sciencedata where BSCapp_sciencedata.user_id = %s;'
    try:
        cursor.execute(sql, [user_id])
        content = cursor.fetchall()
        cursor.close()
    except Exception as e:
        cursor.close()
    return content

def GetDownloadData(user_id):
    #get purchase data
    content = {}
    cursor = connection.cursor()
    sql = 'select log_id from BSCapp_downloadlog where BSCapp_downloadlog.user_id = %s;'
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

def generate_sort_class(sort_name, sort_type, sort_list):
    sort_class = {}
    for item in sort_list :
        sort_class[item] = ''

    if sort_type == 'DESC':
        sort_class[sort_name] = 'fa fa-caret-down text-danger' # DESC down
    else:
        sort_class[sort_name] = 'fa fa-caret-up text-success' # ASC up
    return sort_class

def newChainData_sql(request, default_sort_name, default_sort_type):
    context = {}
    cursor = connection.cursor()
    sql = 'select block_height, prev_hash, tx_id, block_timestamp, nonce, block_hash ' \
          'from BSCapp_NewBlock '
    try:
        cursor.execute(sql)
        content = cursor.fetchall()
    except Exception as e:
        print(e)
        return context, 0

    len_content = len(content)

    search_sql = ''
    search_base = ''
    search_field = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'where {} like %s '.format(search_base)
    except Exception as e:
        # print(e)
        pass

    blocks = []
    for i in range(len_content):
        block = dict()
        block['block_height'] = content[i][0]
        block['prev_hash'] = content[i][1]
        block['tx_id'] = content[i][2]
        block['block_timestamp'] = content[i][3]
        block['nonce'] = content[i][4]
        block['block_hash'] = content[i][5]
        if block['tx_id']=='2018': # the gensis block
            continue

        item_log = OperationLog.objects.get(tx_id=block['tx_id'])
        # 确保存在此数据
        if(default_sort_type == 'ASC'):
            item_log = item_log.order_by('-'+default_sort_name)
        else:
            item_log = item_log.order_by(default_sort_name)
        # print('search_base',search_base)
        if search_base == 'tx_id':
            item_log.filter(tx_id__contains=search_field)
        elif search_base == 'first_title':
            item_log.filter(first_title__contains=search_field)
        elif search_base == 'second_title':
            item_log.filter(second_title__contains=search_field)


        # print(sort_data)
        # item_log = OperationLog.objects.get(tx_id=block['tx_id'])

        # print(item_log)
        block['user_id'] = item_log.user_id
        block['timestamp'] = time_to_str(item_log.timestamp)
        science_data_id_list = item_log.science_data_id_list
        block['conference_data_id_list'] = item_log.conference_data_id_list
        block['journal_data_id_list'] = item_log.journal_data_id_list
        block['patent_data_id_list'] = item_log.patent_data_id_list

        block['action'] = item_log.action
        block['reviewer'] = item_log.reviewer
        block['first_title'] = item_log.first_title
        block['second_title'] = item_log.second_title
        block['data_type'] = '待补充'
        if len(science_data_id_list) == 0 and block['conference_data_id_list'] =='' and \
                block['journal_data_id_list']=='' and block['patent_data_id_list'] == '':
            continue
        # only have science data
        else:
            science_data_id = science_data_id_list
            science_data = ScienceData.objects.get(data_id= science_data_id)
            block['first_title'] = science_data.first_title
            block['second_title'] = science_data.second_title
            block['data_type'] = '其他'
            block['science_data_name'] = science_data.data_name
            block['science_data_info'] = science_data.data_info
            block['science_data_source'] = science_data.data_source
            block['science_data_size'] = str(round(science_data.data_size,3))+'MB'
        blocks.append(block)

        if block['conference_data_id_list']!='':
            conference_data_id_list = block['conference_data_id_list'].split(',')
            for item_id in conference_data_id_list:
                block[item_id] = {}
                conference_data = Conference.objects.get(article_id=item_id)
                # get article name
                block[item_id]['article_name'] = conference_data.article_name

                # get authors
                article_authors_list = conference_data.article_authors.split('%')
                authors_str = ''
                for item_author in article_authors_list:
                    single_author = item_author.split('^')[1][1:-1]
                    if authors_str =='':
                        authors_str += single_author
                    else:
                        authors_str += ','+single_author
                block[item_id]['article_authors'] = authors_str

                #get conference name
                block[item_id]['conference_name'] = conference_data.conference_name

                # get keywors
                keywords_list = conference_data.keywords.split[',']
                keywords_str = ''
                for item_keyword in keywords_list:
                    if keywords_str == '':
                        keywords_str += item_keyword
                    else:
                        item_keyword += ','+item_keyword

                block[item_id]['keywords'] = conference_data.keywords

                # get abstract
                block[item_id]['abstract'] = conference_data.abstract

        if block['journal_data_id_list']!='':
            journal_data_id_list = block['journal_data_id_list'].split(',')
            for item_id in journal_data_id_list:
                block[item_id] = {}
                journal_data = Journal.objects.get(article_id=item_id)
                # get article name
                block[item_id]['article_name'] = journal_data.article_name

                # get authors
                article_authors_list = journal_data.article_authors.split('%')
                authors_str = ''
                for item_author in article_authors_list:
                    if authors_str == '':
                        authors_str += item_author
                    else:
                        authors_str += ',' + item_author
                block[item_id]['article_authors'] = authors_str

                # get conference name
                block[item_id]['journal_name'] = journal_data.journal_name

                # get keywors
                keywords_list = journal_data.keywords.split[',']
                keywords_str = ''
                for item_keyword in keywords_list:
                    if keywords_str == '':
                        keywords_str += item_keyword
                    else:
                        item_keyword += ',' + item_keyword

                block[item_id]['keywords'] = journal_data.keywords
                # get abstract
                block[item_id]['abstract'] = journal_data.abstract

        if block['patent_data_id_list']!='':
            patent_data_id_list = block['patent_data_id_list'].split(',')
            for item_id in patent_data_id_list:
                block[item_id] = {}
                patent_data = Patent.objects.get(patent_id=item_id)
                # get article name
                block[item_id]['patent_openId'] = patent_data.patent_openId
                block[item_id]['patent_name'] = patent_data.patent_name
                block[item_id]['patent_applicant'] = patent_data.patent_applicant
                block[item_id]['patent_authors'] = patent_data.patent_authors
                block[item_id]['patent_keywords'] = patent_data.patent_keywords
                block[item_id]['patent_province'] = patent_data.patent_province
    return blocks, len_content


def chainData_sql(request, sort_sql):
    context = {}
    cursor = connection.cursor()
    sql = 'select tx_id, user_id, timestamp, science_data_id_list, conference_data_id_list, journal_data_id_list, ' \
          ' patent_data_id_list, action, reviewer, first_title, second_title ' \
          'from BSCapp_OperationLog '
    search_sql = ''
    try:
        search_base = request.POST["searchBase"]
        search_field = request.POST["searchField"]
        search_sql = 'where {} like %s '.format(search_base)
    except Exception as e:
        # print(e)
        pass

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
        return context
    blocks = []
    len_content = len(content)
    for i in range(len_content):
        block = dict()
        tx_id = content[i][0]
        block['tx_id'] = tx_id
        print(tx_id)
        try:
            newBlock = NewBlock.objects.get(tx_id=tx_id)
            block['detail'] = {}
            block['detail']['block_height'] = newBlock.block_height
            block['detail']['prev_hash'] = newBlock.prev_hash
            block['detail']['block_timestamp'] = newBlock.block_timestamp
            block['detail']['nonce'] = newBlock.nonce
            block['detail']['block_hash'] = newBlock.block_hash
        except Exception as e:
            print(e)
            pass
        block['user_id'] = content[i][1]
        block['timestamp'] = time_to_str(content[i][2])
        science_data_id_list = content[i][3] # split by  only one!!!
        block['conference_data_id_list'] = content[i][4]
        block['journal_data_id_list'] = content[i][5]
        block['patent_data_id_list'] = content[i][6]

        block['action'] = content[i][7]
        block['reviewer'] = content[i][8]
        first_title = content[i][9]
        second_title = content[i][10]
        block['data_type'] = '待补充'

        if len(science_data_id_list) == 0 and block['conference_data_id_list'] =='' and \
                block['journal_data_id_list']=='' and block['patent_data_id_list'] == '':
            continue
        # only have science data
        else:
            science_data_id = science_data_id_list
            science_data = ScienceData.objects.get(data_id= science_data_id)
            block['first_title'] = science_data.first_title
            block['second_title'] = science_data.second_title
            block['data_type'] = '其他'
            block['science_data_name'] = science_data.data_name
            block['science_data_info'] = science_data.data_info
            block['science_data_source'] = science_data.data_source
            block['science_data_size'] = str(round(science_data.data_size,3))+'MB'
        blocks.append(block)

        if block['conference_data_id_list']!='':
            conference_data_id_list = block['conference_data_id_list'].split(',')
            for item_id in conference_data_id_list:
                block[item_id] = {}
                conference_data = Conference.objects.get(article_id=item_id)
                # get article name
                block[item_id]['article_name'] = conference_data.article_name

                # get authors
                article_authors_list = conference_data.article_authors.split('%')
                authors_str = ''
                for item_author in article_authors_list:
                    single_author = item_author.split('^')[1][1:-1]
                    if authors_str =='':
                        authors_str += single_author
                    else:
                        authors_str += ','+single_author
                block[item_id]['article_authors'] = authors_str

                #get conference name
                block[item_id]['conference_name'] = conference_data.conference_name

                # get keywors
                keywords_list = conference_data.keywords.split[',']
                keywords_str = ''
                for item_keyword in keywords_list:
                    if keywords_str == '':
                        keywords_str += item_keyword
                    else:
                        item_keyword += ','+item_keyword

                block[item_id]['keywords'] = conference_data.keywords

                # get abstract
                block[item_id]['abstract'] = conference_data.abstract

        if block['journal_data_id_list']!='':
            journal_data_id_list = block['journal_data_id_list'].split(',')
            for item_id in journal_data_id_list:
                block[item_id] = {}
                journal_data = Journal.objects.get(article_id=item_id)
                # get article name
                block[item_id]['article_name'] = journal_data.article_name

                # get authors
                article_authors_list = journal_data.article_authors.split('%')
                authors_str = ''
                for item_author in article_authors_list:
                    if authors_str == '':
                        authors_str += item_author
                    else:
                        authors_str += ',' + item_author
                block[item_id]['article_authors'] = authors_str

                # get conference name
                block[item_id]['journal_name'] = journal_data.journal_name

                # get keywors
                keywords_list = journal_data.keywords.split[',']
                keywords_str = ''
                for item_keyword in keywords_list:
                    if keywords_str == '':
                        keywords_str += item_keyword
                    else:
                        item_keyword += ',' + item_keyword

                block[item_id]['keywords'] = journal_data.keywords
                # get abstract
                block[item_id]['abstract'] = journal_data.abstract

        if block['patent_data_id_list']!='':
            patent_data_id_list = block['patent_data_id_list'].split(',')
            for item_id in patent_data_id_list:
                block[item_id] = {}
                patent_data = Patent.objects.get(patent_id=item_id)
                # get article name
                block[item_id]['patent_openId'] = patent_data.patent_openId
                block[item_id]['patent_name'] = patent_data.patent_name
                block[item_id]['patent_applicant'] = patent_data.patent_applicant
                block[item_id]['patent_authors'] = patent_data.patent_authors
                block[item_id]['patent_keywords'] = patent_data.patent_keywords
                block[item_id]['patent_province'] = patent_data.patent_province


    return blocks, len_content

def sendResetPwdEmail(receiver, secretKey):

    BSC_ip = 'http://' + '127.0.0.1'
    BSC_port = '8000'

    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "bsc_admin@126.com"  # 用户名
    mail_pass = "bscadmin2018"  # 口令
    receivers = []
    receivers.append(receiver)

    reset_path = BSC_ip + ':' + BSC_port + '/' + str(secretKey)

    message = MIMEText('本邮件发送时间: '+time_to_str(time())+' 重设密码链接: '+reset_path + '  请勿回复本邮件，30分钟后此链接将会失效.', 'plain', 'utf-8')
    message['From'] = mail_user
    message['To'] = receiver
    subject = '重置密码( BSC系统 )'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        return True
    except smtplib.SMTPException as e:
        return False


# coding:utf-8
import cx_Oracle
import os
import datetime
from WindPy import *
import re
import numpy
import calendar
class oracle_insert():
    def getAllFile(self,path):
            result = []  # 所有的文件
            path = path.decode('utf-8').encode('gbk')
            for maindir, subdir, file_name_list in os.walk(path):
                for filename in file_name_list:
                    apath = os.path.join(maindir, filename)  # 合并成一个完整路径
                    apath = apath.decode('gbk').encode('utf-8')
                    result.append(apath)
            return result
    def saveManayValues(self,sql,values):
        cr.executemany(sql,values)
        db.commit()
    def get_value_symbols(self,pattern1,objs,sql,nation_code,whole_last_symbol,date):
        pattern2 = re.compile('..$')
        nation_number=0
        while nation_number < len(nation_code):  # 遍历此symbol列表
            temp_symbol = pattern1.findall(nation_code[nation_number])
            temp_nation_symbol=nation_code[nation_number]
            if '-' in nation_code[nation_number]:
                nation_number+=1
                continue
            temp_month = pattern2.findall(str(nation_code[nation_number]).split('.')[0])
            if len(str(nation_code[nation_number]).split('.')[0].split(temp_symbol[0])[1]) == 3:
                temp_nation_symbol = temp_symbol[0] + '1' + str(nation_code[nation_number]).split(temp_symbol[0])[1]
            print temp_month
            if int(temp_month[0]) == 1 or int(str(temp_nation_symbol).split('.')[0].split(temp_symbol[0])[1][:2]) < 18:
                print nation_code[nation_number]
                nation_number+=1
                continue
            temp_same_symbol = []
            temp_same_symbol.append(nation_code[nation_number])  # 初始的symbol元素放入此列表中
            nation_number += 1
            if nation_number < len(nation_code):
                while pattern1.findall(nation_code[nation_number]) == temp_symbol:  # 将后续相同的小symbol放入temp_same_symbol中
                    if '-' in nation_code[nation_number] or int(temp_month[0]) == 1 or int(str(temp_nation_symbol).split('.')[0].split(temp_symbol[0])[1][:2]) < 18:
                        nation_number+=1
                        if nation_number < len(nation_code):
                            continue
                        else:break
                    temp_month = pattern2.findall(nation_code[nation_number].split('.')[0])
                    if len(nation_code[nation_number].split('.')[0].split(temp_symbol[0])[1]) == 3:
                         temp_nation_symbol= temp_symbol[0] + '1' + nation_code[nation_number].split(temp_symbol[0])[1]
                    temp_same_symbol.append(nation_code[nation_number])  # 相同的symbol的元素放入此列表中
                    print temp_same_symbol
                    nation_number += 1
                    if nation_number < len(nation_code):
                        continue
                    else:
                        break
                (temp_same_symbol,whole_last_symbol) = oracle_insert.get_volume_end_list(temp_same_symbol,date,whole_last_symbol,temp_symbol[0])
                if len(temp_same_symbol)==0:
                    continue
                objs = oracle_insert.get_wind_objs(temp_same_symbol, date, objs, sql, temp_symbol)  # 取前三
        return objs
    def get_volume_end_list(self,temp_same_symbol,date,whole_last_symbol,temp_symbol):#用temp_same_symbol代替volume_end_list
        volume_dict = {}
        for each_symbol in temp_same_symbol:  # 此for创建字典
            volume_list =w.wsd(each_symbol, "volume", date, date, "ShowBlank=0").Data[0]
            print volume_list, each_symbol, date
            if type(volume_list[0])!=float or volume_list[0] < 100:
                continue
            else:
                volume_dict[each_symbol] = volume_list[0]
        temp_same_symbol = []  # 这里用上面的列表代替volume_dict_list_end
        volume_dict_list = sorted(volume_dict.items(), key=lambda d: d[1],reverse=True)  # [('b', 4), ('c', 2), ('a', 1)]
        if len(volume_dict_list) != 0:
            if len(volume_dict_list) > 2:
                temp_same_symbol = [volume_dict_list[0][0], volume_dict_list[1][0], volume_dict_list[2][0]]
            else:
                for volume_element in volume_dict_list:
                    temp_same_symbol.append(volume_element[0])  #[('d','dd'),('dd','ddd')]
            last_symbols=whole_last_symbol[temp_symbol]
            for j_temp in range(0,len(temp_same_symbol)):
                if len(last_symbols)>j_temp:
                    if int(str(last_symbols[j_temp]).split('.')[0].split(temp_symbol)[1])>int(str(temp_same_symbol[j_temp]).split('.')[0].split(temp_symbol)[1]):
                        temp_same_symbol=last_symbols
                        break
                    if j_temp==len(temp_same_symbol)-1:#如果在最后一次比较中last_symbols还小于temp_same_symbos，则该替换
                        whole_last_symbol[temp_symbol]=temp_same_symbol
                        break
                else:
                    whole_last_symbol[temp_symbol]=temp_same_symbol
                    break
        return temp_same_symbol,whole_last_symbol
    def get_wind(self,objs,sql):
        pattern1 = re.compile('^\D+')
        date = '2018-' + str(datetime.now().month) + '-' + str(datetime.now().day)
        strr = w.wset("sectorconstituent", "date=%s;sectorid=1000028001000000;field=date,wind_code" % (date))
        nation_code = strr.Data[1]
        whole_last_symbol={}
        temp_symbol = pattern1.findall(nation_code[0])
        whole_last_symbol[temp_symbol[0]]=[]
        for i_number in range(1,len(nation_code)):
            temp_symbol=pattern1.findall(nation_code[i_number])
            print temp_symbol
            if whole_last_symbol.has_key(temp_symbol[0])==False:
                whole_last_symbol[temp_symbol[0]]=[]        #初始化whole_last_symbol
        print whole_last_symbol
        for i_month in range(1,datetime.now().month+1):
            if i_month==datetime.now().month:
                day_range=datetime.now().day+1
            else:day_range=calendar.monthrange(2018,i_month)[1]+1
            for j_day in range(1,day_range):
                date = '2018-' + str(i_month) + '-' + str(j_day)
                objs=oracle_insert.get_value_symbols(pattern1,objs,sql,nation_code,whole_last_symbol,date)
        return objs
    def get_wind_objs(self,symbols,date,objs,sql,temp_symbol):
        strr = w.wsi(symbols, "open,close,high,low,volume,oi", date + ' ' + '00:00:00', date + ' ' + '23:59:59',"ShowBlank=0")
        if len(symbols) == 1:
            symbol = str(symbols[0]).split('.')[0]
            if len(symbol.split(temp_symbol[0])[1]) == 3:
                symbol = temp_symbol[0] + '1' + symbol.split(temp_symbol[0])[1]
            for i_time in range(0, len(strr.Times)):
                volume = strr.Data[4][i_time]
                if volume == 0:
                    continue
                factor = (symbol, strr.Times[i_time], strr.Data[0][i_time], strr.Data[1][i_time], strr.Data[2][i_time],strr.Data[3][i_time], volume, strr.Data[5][i_time])
                objs.append(factor)
        else:
            for number in range(0,len(symbols)):
                first_position = len(strr.Times) / len(symbols) * number
                end_position = len(strr.Times) / len(symbols) * (number + 1)
                symbol = str(symbols[number]).split('.')[0]
                if len(symbol.split(temp_symbol[0])[1]) == 3:
                    symbol = temp_symbol[0] + '1' + symbol.split(temp_symbol[0])[1]
                for i_time in range(first_position, end_position):
                    volume = strr.Data[6][i_time]
                    if volume == 0:
                        continue
                    factor = (symbol, strr.Data[0][i_time], strr.Data[2][i_time], strr.Data[3][i_time], strr.Data[4][i_time],strr.Data[5][i_time], volume, strr.Data[7][i_time])
                    objs.append(factor)
        if len(objs) > 500:
            oracle_insert.saveManayValues(sql, objs)
            objs = []
        return objs
if __name__=='__main__':
    tns = cx_Oracle.makedsn(IP, port, name1)
    db = cx_Oracle.connect(name2, name3, tns)
    cr = db.cursor()
    w.start()
    sql = "insert into QUOTE_1MIN6 (symbol,trad_dt,open_price,close_price,high,low,volume,cje) values(:1,:2,:3,:4,:5,:6,:7,:8)"
    oracle_insert=oracle_insert()
    objs = []
    objs=oracle_insert.get_wind(objs,sql)
    oracle_insert.saveManayValues(sql, objs)
    print 'dddd'

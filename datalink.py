import csv
import re
from prettytable import PrettyTable


class HelpingModule:

        def compare_date(date, start_date):
            list_date = date.split('/')
            try:
                if int(list_date[0]) < int(start_date[0]):
                    return False
                elif int(list_date[1]) < int(start_date[1]):
                    return False
                elif int(list_date[2]) < int(start_date[2]):
                    return False
            except:
                return False
            return True
        
        '''
        def compare_type(type_sn, in_type):
            list_type = type_sn.split(',')
            for item in list_type:
                if len(item) > 2:
                    item = item[0:1:1]
                if item == in_type:
                    return True
        HelpingModule.compare_type(item['claimedtype'], self.type)
        '''

class DataLink(HelpingModule):

    def __init__(self, phang_path, sn_path, outpath, start_date, type):
        self.phang_path = phang_path
        self.sn_path = sn_path
        self.start_date = start_date.split('/')
        self.type = type
        self.dict_sn = []
        self.dict_ph = []
        self.dict_out = []
        self.list_ph = []

    def csv_reader_ph(self):
        with open(self.phang_path) as csvfile:
            reader_ph = csv.DictReader(csvfile)
            for row in reader_ph:
                self.dict_ph.append(
                    {'Name': row['Name']})
            for item in self.dict_ph:
                self.list_ph.append(item['Name'])
            self.list_ph.pop(0)

    def csv_reader_sn(self):
        with open(self.sn_path, encoding='utf-8') as csvfile:
            reader_sn = csv.DictReader(csvfile)
            for row in reader_sn:
                self.dict_sn.append(
                    {'event': row['event'], 'claimedtype': row['claimedtype'], 'host': row['host'], 'discoverdate': row['discoverdate']})
    

    def main(self):
        for item in self.dict_sn:
            
            names_ngc_ic = item['host'].split(',')
            
            for j in range(len(names_ngc_ic)):
                for i in range(len(self.list_ph)):
                    if re.sub(' ', '', names_ngc_ic[j]) == self.list_ph[i] and HelpingModule.compare_date(item['discoverdate'], self.start_date):
                        self.dict_out.append(item)

    def plotting(self):
        table = PrettyTable()
        table.field_names = ['Event', 'Type', 'Host', 'Date']
        for item in self.dict_out:
            row = [item['event'], item['claimedtype'], item['host'], item['discoverdate']]
            table.add_row(row)
        print(table)

if __name__ == '__main__':
    obj = DataLink('PHANGS.csv', 'SNDATA.csv', 'output.csv', '2017/1/1', 'Ia')
    obj.csv_reader_ph()
    obj.csv_reader_sn()
    obj.main()
    obj.plotting()
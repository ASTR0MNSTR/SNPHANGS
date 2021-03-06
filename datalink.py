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
        
        def compare_type(type_sn, in_type):
            list_type = type_sn.split(',')
            for i in range(len(in_type)):
                for item in list_type:
                    if item.startswith(in_type[i]):
                        return True
    

class DataLink(HelpingModule):

    def __init__(self, phang_path, sn_path, outpath, start_date, types):
        self.phang_path = phang_path
        self.sn_path = sn_path
        self.start_date = start_date.split('/')
        self.outpath = outpath
        self.types = types.split(', ')
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
            
    
    def txt_reader_ph(self):
        with open(self.phang_path) as inputfile:
            lines = inputfile.readlines()
            content = [item.strip() for item in lines]
            for item in content:
                names = item.split(' ')
                self.list_ph.append(names)

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
                    for k in range(len(self.list_ph[i])):
                        if re.sub(' ', '', names_ngc_ic[j]) == self.list_ph[i][k] and HelpingModule.compare_date(item['discoverdate'], self.start_date) and HelpingModule.compare_type(item['claimedtype'], self.types):
                            self.dict_out.append(item)
            
            for i in range(len(self.dict_out)):
                try:
                    if self.dict_out.count(self.dict_out[i]) > 1:
                        self.dict_out.pop(i)
                except:
                    pass

    def plotting(self):
        table = PrettyTable()
        table.field_names = ['Event', 'Type', 'Host', 'Date']
        for item in self.dict_out:
            row = [item['event'], item['claimedtype'], item['host'], item['discoverdate']]
            table.add_row(row)
        print(table)
    
    def file_output(self):
        with open(self.outpath, 'w', newline = '') as out:
            writer = csv.writer(out, quotechar=',')
            for item in self.dict_out:
                writer.writerow([item['event'], item['claimedtype'], item['host'], item['discoverdate']])


if __name__ == '__main__':
    start_date = input('Start date in YY/MM/DD: ')
    types = input('Write types you look for here (II, Ia, Ib etc.): ')
    obj = DataLink('out_mod.txt', 'SNDATA.csv', 'output.csv', start_date, types)
    obj.txt_reader_ph()
    obj.csv_reader_sn()
    obj.main()
    obj.plotting()
    obj.file_output()
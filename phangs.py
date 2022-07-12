import csv
import re

class GalaxyNames:

    def __init__(self, phang_path, txt_inpath, txt_outpath):
        self.phang_path = phang_path
        self.intxt_path = txt_inpath
        self.txt_out_path = txt_outpath
        self.dict_ph = []
        self.out_list = []
        self.list_ph = []
    
    def reading_ph(self):
        with open(self.phang_path) as csvfile:
            reader_ph = csv.DictReader(csvfile)
            for row in reader_ph:
                self.dict_ph.append(
                    {'Name': row['Name']})
            for item in self.dict_ph:
                self.list_ph.append(item['Name'])
            self.list_ph.pop(0)

    def main(self):
        with open(self.intxt_path, 'r') as input:
            lines = input.readlines()
        content = [item.strip() for item in lines]
        for item in content:
            out_chunk = ''
            splitted = item.split('; ')
            for item in splitted:
                item = re.sub(' ', '', item)
                if item.startswith('NGC'):
                    if item[3] == '0':
                        item = item[0:2] + item[4:]
                if item.startswith('MESSIER'):
                    item = 'M' + re.sub(r'[A-Z]', '', item)
                    if item[1] == '0':
                        item = item[0] + item[2:]
                out_chunk = out_chunk + item + ' '
            self.out_list.append(out_chunk)
    
    def writing_txt(self):
        with open(self.txt_out_path, 'w') as out:
            for item in self.out_list:
                out.writelines(f'{item}\n')

if __name__ == '__main__':
    obj = GalaxyNames('PHANGS.csv', 'galaxy_names.txt', 'out.txt')
    obj.reading_ph()
    obj.main()
    obj.writing_txt()
    


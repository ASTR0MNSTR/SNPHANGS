import csv

class Helper:

    def help():
        pass

class SearchHost(Helper):

    def __init__(self, txt_inpath, txt_outpath, sndata_path):
        self.txt_inpath = txt_inpath
        self.txt_outpath = txt_outpath
        self.sndata_path = sndata_path

        self.full_names = []
        self.sn_list = []
        self.sn_dict = {}
        self.hosts = []
        self.by_host_list = []
        self.wider_sn_dict = {}
        self.output_dict = {}

    def reading_txt(self):
        with open(self.txt_inpath, 'r') as f:
            content = f.readlines()
            self.full_names = [item.strip() if item.strip().startswith('PSN') else 'SN' + item.strip() for item in content]
    
    def reading_csv(self):
        with open(self.sndata_path, encoding = 'utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.sn_list.append({'event': row['event'], 'host': row['host']})
    
    def main(self):
        for item in self.sn_list:
            self.sn_dict.update({item['event'] : item['host']})
        
        for item in self.full_names:
            try:
                self.hosts.append(self.sn_dict[item])
            except:
                print(f"Sorry, I didn't find the {item}")
        print(self.hosts)
    
    def looking_for_hosts(self):
        for hosts in self.hosts: 
            for item in hosts.split(','):
                print(item)
                for key in self.sn_dict:
                    for host in self.sn_dict[key].split(','):
                        if host == item:
                            self.output_dict.update({key : self.sn_dict[key]})
        
        k = 0
        for item in self.full_names:
            try:
                self.output_dict.pop(item)
            except:
                print(f'Occured problem with {item}')
                pass
            k += 1
        
    def outputting(self):
        with open(self.txt_outpath, 'w') as out:
            for key in self.output_dict:
                out.writelines(f'{key} ... {self.output_dict[key]}\n')

if __name__ == '__main__':
    obj = SearchHost('sample.txt', 'NewSNs.txt', 'SNDATA.csv')
    obj.reading_csv()
    obj.reading_txt()
    obj.main()
    obj.looking_for_hosts()
    obj.outputting()
    print('Thanks for using OR software')

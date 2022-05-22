import csv
from glob import glob
import pandas as pd
import os
from sklearn.utils import shuffle

pd.set_option('max_colwidth', 85)

class CSVCreator:
    HEADER = ['labels', 'log']

    NAMES = ['Proxifier', 'Switch', 'Router', 'Firewall', 'Android', 'Linux', 'Mac', 'Windows', 'Browser', 'Cloud',
             'Analytics', 'Process', 'DNS', 'Apache', 'Antivirus', 'Auth', 'Botnet', 'Honeypot', 'Snort', 'Threat']

    sources = {
        'Proxifier_data.log': {
            'lesCategory': 0
        },
        'Switch_data.txt': {
            'lesCategory': 1
        },
        'Router_data.txt': {
            'lesCategory': 2
        },
        'Firewall_data.txt': {
            'lesCategory': 3
        },
        'Android_data.log': {
            'lesCategory': 4
        },
        'Linux_data.log': {
            'lesCategory': 5
        },
        'Mac_data.log': {
            'lesCategory': 6
        },
        'Windows_data.log': {
            'lesCategory': 7
        },
        'Browser_data.txt': {
            'lesCategory': 8
        },
        'Cloud_data.log': {
            'lesCategory': 9
        },
        'Analytics_data.log': {
            'lesCategory': 10
        },
        'Process_data.log': {
            'lesCategory': 11
        },
        'DNS_data.txt': {
            'lesCategory': 12
        },
        'Apache_data.txt': {
            'lesCategory': 13
        },
        'Antivirus_data.txt': {
            'lesCategory': 14
        },
        'Auth_data.txt': {
            'lesCategory': 15
        },
        'Botnet_data.txt': {
            'lesCategory': 16
        },
        'Honeypot_data.txt': {
            'lesCategory': 17
        },
        'Snort_data.txt': {
            'lesCategory': 18
        },
        'Threat_data.txt': {
            'lesCategory': 19
        }
    }

    def __init__(self):
        pass

    def create_csv(self, name, les):
        txtfile = open('logs/' + name, 'r')

        csvfname = os.path.splitext(name)[0] + '.csv'

        file = open('csv/' + csvfname, 'w', newline='')
        writer = csv.writer(file, delimiter=',')

        writer.writerow(self.HEADER)
        for line in txtfile:
            writer.writerow([les, line.strip()])

        txtfile.close()
        file.close()

    def create_all(self):
        for name, column_vals in self.sources.items():
            self.create_csv(name, column_vals['lesCategory'])

    def split_csv(self, fname):
        reader = csv.DictReader(open('csv/' + fname, 'r'), delimiter=',')
        self._write_lines(reader, 1200, 'csv_train/' + os.path.splitext(fname)[0] + '_train' + '.csv')
        self._write_lines(reader, 400, 'csv_validate/' + os.path.splitext(fname)[0] + '_validate' + '.csv')
        self._write_lines(reader, 400, 'csv_test/' + os.path.splitext(fname)[0] + '_test' + '.csv')

    def _write_lines(self, reader, count, fpath):
        file = open(fpath, 'w', newline='')
        writer = csv.writer(file, delimiter=',')

        writer.writerow(self.HEADER)
        i = 0
        for line in reader:
            writer.writerow([line[self.HEADER[0]], line[self.HEADER[1]]])

            i += 1
            if i >= count:
                break

    def split_all(self):
        for instance in self.NAMES:
            self.split_csv(instance + '_data.csv')

    def merge_train(self, file_out):
        result_obj = pd.concat([pd.read_csv(file, delimiter=',') for file in glob('csv_train/*_data_train.csv')])
        result_obj.to_csv(file_out, index=False, encoding="utf-8")

    def merge_validate(self, file_out):
        result_obj = pd.concat([pd.read_csv(file, delimiter=',') for file in glob('csv_validate/*_data_validate.csv')])
        result_obj.to_csv(file_out, index=False, encoding="utf-8")

    def merge_test(self, file_out):
        result_obj = pd.concat([pd.read_csv(file, delimiter=',') for file in glob('csv_test/*_data_test.csv')])
        result_obj.to_csv(file_out, index=False, encoding="utf-8")

    def shuffle_train(self, file_out):
        in_obj = pd.read_csv('csv_merged/Train_data_merged.csv', delimiter=',')
        shuffled = shuffle(in_obj)
        shuffled.to_csv(file_out, index=False, encoding="utf-8")

    def shuffle_validate(self, file_out):
        in_obj = pd.read_csv('csv_merged/Validate_data_merged.csv', delimiter=',')
        shuffled = shuffle(in_obj)
        shuffled.to_csv(file_out, index=False, encoding="utf-8")

    def shuffle_test(self, file_out):
        in_obj = pd.read_csv('csv_merged/Test_data_merged.csv', delimiter=',')
        shuffled = shuffle(in_obj)
        shuffled.to_csv(file_out, index=False, encoding="utf-8")

    # list_of_files = [file for file in glob('*_data_train.csv')]
    # print(list_of_files)

    # list_of_files = [file for file in glob('*.txt')]
    # print(list_of_files)

    # for key, value in sources.items():
    #     print(key, ' : ', value)


if __name__ == '__main__':

    creator = CSVCreator()

    creator.create_all()

    creator.split_all()

    creator.merge_train('csv_merged/Train_data_merged.csv')
    creator.merge_validate('csv_merged/Validate_data_merged.csv')
    creator.merge_test('csv_merged/Test_data_merged.csv')

    creator.shuffle_train('csv_merged_shuffled/Train_data_merged_shuffled.csv')
    creator.shuffle_validate('csv_merged_shuffled/Validate_data_merged_shuffled.csv')
    creator.shuffle_test('csv_merged_shuffled/Test_data_merged_shuffled.csv')

    # dftrainm = pd.read_csv('csv_merged/Train_data_merged.csv', delimiter=',')
    # print('')
    # print('Trénovací datová sada merged')
    # print(dftrainm)
    # dfvalidatem = pd.read_csv('csv_merged/Validate_data_merged.csv', delimiter=',')
    # print('')
    # print('Validační datová sada merged')
    # print(dfvalidatem)
    # dftestm = pd.read_csv('csv_merged/Test_data_merged.csv', delimiter=',')
    # print('')
    # print('Testovací datová sada merged')
    # print(dftestm)

    dftrainms = pd.read_csv('csv_merged_shuffled/Train_data_merged_shuffled.csv', delimiter=',')
    print('')
    print('Trénovací datová sada:')
    print('##################################################################################################')
    print(dftrainms)
    print('##################################################################################################')
    dfvalidatems = pd.read_csv('csv_merged_shuffled/Validate_data_merged_shuffled.csv', delimiter=',')
    print('')
    print('Validační datová sada:')
    print('#################################################################################################')
    print(dfvalidatems)
    print('#################################################################################################')
    dftestms = pd.read_csv('csv_merged_shuffled/Test_data_merged_shuffled.csv', delimiter=',')
    print('')
    print('Testovací datová sada:')
    print('#################################################################################################')
    print(dftestms)
    print('#################################################################################################')
# načíst soubory logů do proměnných (každý nový řádek, nový log)
# název kategorie - ID (dictionary)
# přiřadit category name, category ID, LES category
# merge -> uložit do csv
# randomize rows -> uložit finální soubor
import csv
from glob import glob
import pandas
import os


class CSVCreator:
    HEADER = ['Log', 'srcID', 'lesID']

    sources = {
        'Proxifier_data.txt': {
            'sourceCategory': 0,
            'lesCategory': 00
        },
        'Android_data.txt': {
            'sourceCategory': 1,
            'lesCategory': 10
        },
        'Linux_data.txt': {
            'sourceCategory': 1,
            'lesCategory': 11
        },
        'Mac_data.txt': {
            'sourceCategory': 1,
            'lesCategory': 12
        },
        'Windows_data.txt': {
            'sourceCategory': 1,
            'lesCategory': 13
        },
        'DNS_data.txt': {
            'sourceCategory': 2,
            'lesCategory': 20
        },
        'Apache_data.txt': {
            'sourceCategory': 2,
            'lesCategory': 20
        },
        'Avast_data.txt': {
            'sourceCategory': 3,
            'lesCategory': 30
        },
        'Snort_data.txt': {
            'sourceCategory': 3,
            'lesCategory': 32
        },
        'SSHD_data.txt': {
            'sourceCategory': 3,
            'lesCategory': 33
        }
    }

    def __init__(self):
        pass

    def create_csv(self, name, source, les):
        txtfile = open(name, 'r')

        csvfname = os.path.splitext(name)[0] + '.csv'

        file = open(csvfname, 'w', newline='')
        writer = csv.writer(file, delimiter=';')

        writer.writerow(self.HEADER)
        for line in txtfile:
            writer.writerow([line.strip(), source, les])

        txtfile.close()
        file.close()

    def create_all(self):
        for name, column_vals in self.sources.items():
            self.create_csv(name, column_vals['sourceCategory'], column_vals['lesCategory'])

    def split_csv(self, fname):
        reader = csv.DictReader(open(fname, 'r'), delimiter=';')
        self._write_lines(reader, 1200, os.path.splitext(fname)[0] + '_train' + '.csv')
        self._write_lines(reader, 400, os.path.splitext(fname)[0] + '_validate' + '.csv')
        self._write_lines(reader, 400, os.path.splitext(fname)[0] + '_test' + '.csv')

    def _write_lines(self, reader, count, fpath):
        file = open(fpath, 'w', newline='')
        writer = csv.writer(file, delimiter=';')

        writer.writerow(self.HEADER)
        i = 0
        for line in reader:
            writer.writerow([line[self.HEADER[0]], line[self.HEADER[1]], line[self.HEADER[2]]])

            i += 1
            if i >= count:
                break

    def merge_train(self, file_out):
        result_obj = pandas.concat([pandas.read_csv(file, delimiter=';') for file in glob('*_data_train.csv')])
        result_obj.to_csv(file_out, index=False, encoding="utf-8")

    def merge_validate(self, file_out):
        result_obj = pandas.concat([pandas.read_csv(file, delimiter=';') for file in glob('*_data_validate.csv')])
        result_obj.to_csv(file_out, index=False, encoding="utf-8")

    def merge_test(self, file_out):
        result_obj = pandas.concat([pandas.read_csv(file, delimiter=';') for file in glob('*_data_test.csv')])
        result_obj.to_csv(file_out, index=False, encoding="utf-8")

    # list_of_files = [file for file in glob('*_data_train.csv')]
    # print(list_of_files)


if __name__ == '__main__':
    creator = CSVCreator()
    # creator.create_all()

    # creator.split_csv('Android_data.csv')
    # creator.split_csv('Apache_data.csv')
    # creator.split_csv('Avast_data.csv')
    # creator.split_csv('DNS_data.csv')
    # creator.split_csv('Linux_data.csv')
    # creator.split_csv('Mac_data.csv')
    # creator.split_csv('Proxifier_data.csv')
    # creator.split_csv('Snort_data.csv')
    # creator.split_csv('SSHD_data.csv')
    # creator.split_csv('Windows_data.csv')

    # creator.merge_train('Train_data_merged.csv')
    # creator.merge_validate('Validate_data_merged.csv')
    # creator.merge_test('Test_data_merged.csv')

    dftrain = pandas.read_csv('Train_data_merged.csv', delimiter=',')
    print(dftrain)

    dfvalidate = pandas.read_csv('Validate_data_merged.csv', delimiter=',')
    print(dfvalidate)

    dftest = pandas.read_csv('Test_data_merged.csv', delimiter=',')
    print(dftest)

# colab
# inicializovat neuronovou síť
# def kategorie
# naučit model
# otestovat model
# df.to_csv('part1.csv')

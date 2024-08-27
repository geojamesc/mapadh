import csv
import os

# TODO: what is the psql /copy command again?
#  mapadh=> \copy geocrud.geolytix_census_2011 from 'CensusUK11Data.csv' delimiter ',' csv;


def transform_data(path_to_src_txt):

    if os.path.exists(path_to_src_txt):
        out_csv_fname = path_to_src_txt.replace('.txt', '.csv')
        with open(path_to_src_txt, 'r') as inpf:
            my_reader = csv.reader(inpf, delimiter='\t')
            with open(out_csv_fname, 'w') as outpf:
                my_writer = csv.writer(outpf, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                c = 1
                for r in my_reader:
                    if c == 1:
                        col_defs = []
                        header = []
                        for i in r:
                            if i == 'oacode':
                                col_type = 'varchar(9)'
                            else:
                                col_type = 'numeric'
                            col_defs.append(" ".join([i.lower(), col_type]))
                            header.append(i.lower())
                        sql = 'CREATE TABLE geocrud.geolytix_census_2011({});\n'.format(','.join(col_defs))
                        with open(os.path.join(os.path.dirname(path_to_src_txt), 'create_table.sql'), 'w') as outpf:
                            outpf.write(sql)
                    else:
                        out_record = []
                        for i in range(0, len(header), 1):
                            inVal = r[i]
                            if i == 1:
                                outVal = inVal
                            else:
                                try:
                                    outVal = int(inVal)
                                except ValueError:
                                    outVal = float(inVal)
                            out_record.append(outVal)
                        my_writer.writerow(out_record)
                    c += 1


if __name__ == '__main__':
    transform_data(
        path_to_src_txt = '/home/james/geodata/GeoLytix2011/OpenCensusPack/CensusUK11Data.txt'
    )


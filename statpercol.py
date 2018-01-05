# this provides a stats count of all values per field
import pandas as pd
import numpy as np
import csv

infile = 'C:/Users/midavis/Documents/CURE/Data/Final/raw.csv'
df = pd.read_csv(infile)

hdr = list(df)
skips = ['tcga_id']

with open(infile + '-stats.tsv', 'w') as csvfile:

    csvfile.write('FIELD\tVALUES\tCOUNT\n')    
    for col in hdr:     
        skip = -1
        try:
           skip = skips.index(col)
        except:
            pass
        
        if skip < 0:
            csvfile.write(col)
            #csvfile.write('\n')
            x = df[col].value_counts()
            if len(x) > 0:
                for k, v in x.iteritems():
                    s = "\t{}\t{}".format(k, v)
                    csvfile.write(s)
                    csvfile.write('\n')
            else:
                csvfile.write("\t<This variable has no associated values available>")
                csvfile.write('\n')
            csvfile.write('\n')
csvfile.close()
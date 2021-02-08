"""
Script for producing rebinned versions of the ATLAS_2014_I1300647 analysis
ATLAS_REBINNED10_I1300647 for example only has bins up to 10GeV, Histograms then re-normalised

Saved in copy yoda files denoted with _rebinnedPTZ.yoda

"""

import yoda
import numpy as np
import glob
import argparse
parser = argparse.ArgumentParser(description='Submit wildcard string of yoda files...')
parser.add_argument('instring', type=str, help='Wildcard for submission')
parser.add_argument("-v", "--verbose", action="store_true", default=0)
args = parser.parse_args() 

ANALYSIS_BINS = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 22.0, 26.0, 30.0, 34.0, 38.0, 42.0, 46.0, 50.0, 54.0, 60.0, 70.0, 80.0, 100.0, 150.0, 200.0, 300.0, 800.0]
cut_vals = [10.0, 12.0, 14.0, 16.0, 18.0, 22.0, 26.0, 30.0, 34.0, 38.0, 42.0, 46.0, 50.0, 54.0, 60.0, 70.0, 80.0, 100.0, 150.0, 200.0, 300.0, 800.0]

def make_rebinned_file(input_file):

    out_file = input_file.replace(".yoda","_rebinnedPTZ.yoda")

    output_aos = {}

    aos = yoda.read(input_file)
    for ana in aos:
        if "ATLAS_2014_I1300647" not in ana:
            output_aos[ana] = aos[ana].clone()
            continue

        for cut_value in cut_vals:
            out_ana = ana.replace("2014","REBINNED{}".format(int(cut_value)))
            
            new_binning = [x for x in ANALYSIS_BINS if x <= cut_value]
            print(cut_value)
            print(new_binning)
            print(out_ana)
        
            temp_histo1d = aos[ana].clone()
            temp_histo1d.rebinTo(new_binning)

            if "RAW" not in ana:
                temp_histo1d.scaleW(1.0 / temp_histo1d.sumW(includeoverflows=False))

            temp_histo1d.setAnnotation("Path", out_ana)
            #temp_histo1d.setPath(out_ana)
            output_aos[out_ana] = temp_histo1d
        

    yoda.writeYODA(output_aos, out_file)

if "yoda" in args.instring: 
    filepathlist = glob.glob(args.instring)
    print(args.instring)
    for f in filepathlist:
        make_rebinned_file(f)
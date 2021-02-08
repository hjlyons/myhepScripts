import yoda
import numpy as np

def make_rebinned_file(cut_value):
    ana_file = "ATLAS_2014_I1300647.yoda"
    out_file = ana_file.replace("2014","REBINNED{}".format(int(cut_value)))
    print(out_file)
    
    output_aos = {}

    aos = yoda.read(ana_file)
    for ana in aos:
        out_ana = ana.replace("2014","REBINNED{}".format(int(cut_value)))

        out_scatter = yoda.core.Scatter2D(out_ana)
        for point in aos[ana]:
            if point.x > cut_value:
                break
            else:
                out_scatter.addPoint(point)

        x_widths = np.array(out_scatter.xMaxs() - out_scatter.xMins())
        y_vals = np.array(out_scatter.yVals())
        area = x_widths.dot(y_vals)
        out_scatter.scaleY(1.0 / area)

        output_aos[out_ana] = out_scatter.clone()
        if not output_aos[out_ana].hasAnnotation("IsRef"):
            output_aos[out_ana].setAnnotation("IsRef", 1)
        if output_aos[out_ana].hasAnnotation("Variations"):
            output_aos[out_ana].rmAnnotation("Variations")

    yoda.writeYODA(output_aos, out_file)

cut_vals = [10.0, 12.0, 14.0, 16.0, 18.0, 22.0, 26.0, 30.0, 34.0, 38.0, 42.0, 46.0, 50.0, 54.0, 60.0, 70.0, 80.0, 100.0, 150.0, 200.0, 300.0, 800.0]
for c in cut_vals:
    make_rebinned_file(c)
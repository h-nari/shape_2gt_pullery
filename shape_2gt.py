import argparse
import math
import pyclipper
import svgGen
import sys

def gen( **kwargs ):
    start = kwargs.get('start', -1)
    end   = kwargs.get('end', 1)
    r1 = 0.56
    a1 = -64.01077
    r2 = 1.0
    a2 = -18.49452
    r3 = 0.15
    a3 = -(a1+a2)
    s1 = 0.51965
    
    p = svgGen.SvgPolygon()
    p.lineTo( 2 * start, -0.38)
    p.rlineTo( 0, 1.38)
    for i in range(start, end):
        p.rarcTo( 0, -0.56, a1)
        p.rarcTo( -0.89888, -0.43820, a2)
        p.rarcTo( 0.14872, 0.01957, a3);
        p.rlineTo( s1, 0)
        p.rarcTo(0, r3, a3)
        p.rarcTo(0.99146, -0.13043, a2)
        p.rarcTo(0.49888, -0.24320, a1 + 5)
        p.lineTo(i*2+2, 1)
    p.rlineTo( 0, -1.38)
    p.close()

    return p

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='generate 2gt belt shape svg file')
    parser.add_argument('-s','--scale',type=float, default = 100.0)
    parser.add_argument('-x',type=float, default = 300.0)
    parser.add_argument('-y',type=float, default = 100.0)
    parser.add_argument('--start',type=int, default=-1 )
    parser.add_argument('--end',type=int, default=1)
    parser.add_argument('-o','--outfile',default=',2gt_belt.svg')
    
    args = parser.parse_args()

    svg = svgGen.SvgGen();
    belt = gen(start= args.start, end=args.end)
    belt.scale( args.scale);
    belt.translate( args.x, args.y)
    belt.stroke('black','0.25px').fill('red',0.1);
    svg.add(belt)
    svg.write(args.outfile)

    print("output to %s" % args.outfile)
    
    
    
    
    


import argparse
import math
import pyclipper
import svgGen
import sys
import shape_2gt

def gen(num_of_teeth, div=4, offset=0, calc_scale=10000 ):
    tp = 2.0
    nt = num_of_teeth
    rp = nt * tp / math.pi / 2  # pitch radius
    
    c = svgGen.SvgCircle( rp * calc_scale) # pitch circle
    pc = pyclipper.Pyclipper();
    pc.AddPath(c.points, pyclipper.PT_SUBJECT, True)
    
    x = math.ceil(math.sqrt(rp * 2 - 1) / 2);

    t = nt * div;
    for i in range( t ):
        a = math.pi * 2 * i / t
        s = math.sin(a)
        c = math.cos(a)

        belt = shape_2gt.gen(start=-x, end=x+1)
        shift = math.fmod( -a * rp, tp)
        belt.translate(shift, 0)
        belt.rotate(a)
        belt.translate( s * rp, -c * rp)

        belt.scale(calc_scale)
        pc.AddPath(belt.points, pyclipper.PT_CLIP, True)

    result = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO,
                        pyclipper.PFT_NONZERO)

    p = svgGen.SvgPolygon();

    if offset > 0:
        po = pyclipper.PyclipperOffset()
        po.AddPaths(result, pyclipper.PT_SUBJECT, 1)
        result2 = po.Execute( offset * calc_scale);
        p.addPolygon(result2[1])   # inside offset
    else:
        p.addPolygon(result[0])
    p.scale( 1 / calc_scale)
    return p
    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='generate 2gt pulley shape svg file')
    parser.add_argument('num_of_teeth', type=int)
    parser.add_argument('--dpi', type=float, default=96.0 )
    parser.add_argument('-d','--div', type=int, default=10)
    parser.add_argument('--offset', type=float, default=0.0);
    parser.add_argument('-o','--outfile')
    parser.add_argument('--calc_scale', type=float, default=10000.0) 
    
    args = parser.parse_args()
    
    if args.outfile:
        outfile = args.outfile;
    else:
        outfile = ',2gt_%d.svg' % args.num_of_teeth
        
    svg = svgGen.SvgGen()
    pullery = gen(args.num_of_teeth, div=args.div, calc_scale=args.calc_scale,
                  offset=args.offset)

    pullery.scale( args.dpi / 25.4)
    pullery.stroke('black', '0.25px').fill('none')
    svg.add(pullery)

    line = svgGen.SvgPolygon()
    line.lineTo(0,0)
    line.lineTo(0,10)
    line.scale(args.dpi / 25.4)
    line.stroke('red','1px').fill('none')
    svg.add(line)

    svg.write(outfile)
    print("output to ",outfile)
    

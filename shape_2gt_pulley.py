import argparse
import math
import pyclipper
import svgGen
import sys
import shape_2gt
import numpy as np
import fc

norm = np.linalg.norm

def gen(num_of_teeth, div=4, offset=0, calc_scale=10000, error=0.05,
        no_bezier=False ):
    tp = 2.0
    nt = num_of_teeth
    rp = nt * tp / math.pi / 2  # pitch radius

    if no_bezier:
        c = svgGen.SvgCircle( rp * calc_scale) # pitch circle
    else:
        c = svgGen.SvgPolygon()
        a = math.pi / nt
        c.lineTo(0,0)
        c.lineTo(0, -rp)
        c.lineTo(-rp * math.sin(a), -rp * math.cos(a))
        c.close()
        c.scale(calc_scale)

    pc = pyclipper.Pyclipper();
    pc.AddPath(c.points, pyclipper.PT_SUBJECT, True)
    
    x = math.ceil(math.sqrt(rp * 2 - 1) / 2)

    t = nt * div
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
    p.addPolygon(result[0])

    p.scale( 1 / calc_scale)
    
    g = svgGen.SvgGroup()
    p.attr('stroke','blue')
    g.add(p);

    g.attr('stroke-width','0.01').attr('fill','none')
    g.attr("transform","translate(200 700) scale(100)")

    for i in range(len(p.points)):
        if p.points[i][0] == 0.0 and p.points[i][1] == 0.0:
            pos = i
            break
        
    pts = p.points[i+1:]
    pts.extend(p.points[:i])

    biz = fc.fitCurve(pts, error)
    print('len:',(len(biz)-1)/3)
    
    b = svgGen.SvgPath()
    b.attr('stroke','green')
    g.add(b);

    template = np.empty([len(biz)*2-1,2])
    center = len(biz)-1;
    if biz[0][0] == 0.0 :
        template[center] = biz[0]
        for i in range(1,len(biz)):
            template[center-i] = ( -biz[i][0], biz[i][1])
            template[center+i] =  biz[i]
    else:
        template[center] = biz[center]
        for i in range(1,len(biz)):
            template[center-i] = ( -biz[center-i][0], biz[center-i][1])
            template[center+i] =  biz[center-i]
            
    b.moveTo(template[0])
    for i in range(0, nt):
        a = 2.0 * math.pi * i / nt;
        s = math.sin(a)
        c = math.cos(a)
        r = np.array(((c, -s),(s, c)))
        
        rtemp = np.matmul(template,r)
        for j in range(1, len(rtemp), 3):
            b.curveTo(rtemp[j],rtemp[j+1],rtemp[j+2])
    b.closePath()

    svg = svgGen.SvgGen();
    svg.add(g);
    svg.write(',test.svg');
    
    return b

    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='generate 2gt pulley shape svg file')
    parser.add_argument('num_of_teeth', type=int)
    parser.add_argument('--dpi', type=float, default=96.0 )
    parser.add_argument('-d','--div', type=int, default=10)
    parser.add_argument('--offset', type=float, default=0.0);
    parser.add_argument('-o','--outfile')
    parser.add_argument('--calc_scale', type=float, default=10000.0) 
    parser.add_argument('-e','--bezierError', type=float, default=0.05)
    parser.add_argument('-n','--noBezier', action='store_true')
    
    
    args = parser.parse_args()
    
    if args.outfile:
        outfile = args.outfile;
    else:
        outfile = ',2gt_%d.svg' % args.num_of_teeth
        
    svg = svgGen.SvgGen()
    pullery = gen(args.num_of_teeth, div=args.div, calc_scale=args.calc_scale,
                  offset=args.offset, error=args.bezierError,
                  no_bezier=args.noBezier)

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
    

import math

class SvgObj:
    def __init__(self):
        self.dict = {};
    
    def setDict(self, dict):
        for i in dict.items():
            self.dict[i[0]] = i[1]

    def svg(self):
        return ""

    def attr(self, key, value):
        self.dict[key] = value
        return self

    def stroke(self, color, width):
        self.dict['stroke'] = color
        self.dict['stroke-width'] = width;
        return self

    def fill(self, color, opacity=1.0):
        self.dict['fill'] = color
        self.dict['fill-opacity'] = opacity;
        return self

class SvgPolygon(SvgObj):
    def __init__(self):
        super().__init__()
        self.points = []
    
    def svg(self):
        s = "<polygon"
        for i in self.dict.items():
            s += ' ' + i[0] + '="' + str(i[1]) + '"'
        s += ' points="'
        s += ' '.join(map( lambda p: ','.join(map(str,p)), self.points))
        s += '"'
        s += " />\n"
        return s

    def cur(self):
        if len(self.points) > 0:
            return self.points[-1]
        else:
            [Nan,Nan]
            
    def lineTo(self,x,y):
        self.points.append([x,y])
        return self

    def rlineTo(self,x,y):
        if len(self.points) > 0:
            p = self.points[-1]
            self.points.append([p[0]+x,p[1]+y])
        else:
            self.points.append([x,y])
        return self

    def close(self):
        p = self.points[0]
        self.points.append([p[0],p[1]])

    def bbox(self):
        p = self.points[0]
        x0 = x1 = p[0]
        y0 = y1 = p[1]
        for p in self.points[1:]:
            x0 = min(x0, p[0])
            x1 = max(x1, p[0])
            y0 = min(y0, p[1])
            y1 = max(y1, p[1])
        return [x0,y0,x1,y1]


    def rarcTo(self, cx, cy, angle, verbose = False):
        (x,y) = self.points[-1]
        a0 = math.atan2(-cy,-cx)
        r = math.sqrt(cx * cx + cy * cy)
        if verbose:
            print("angle:%f r:%f" % (angle, r)) 
        (x,y) = (x+cx, y+cy)
        step = 10
        if angle > 0:
            for i in range(step):
                a = angle * (i + 1)/ step;
                aa = a0 + a / 180.0 * math.pi
                self.lineTo( x + r * math.cos(aa), y + r * math.sin(aa))
        else:
            for i in range(step):
                a = -angle * (i + 1) / step;
                aa = a0 - a / 180.0 * math.pi
                self.lineTo( x + r * math.cos(aa), y + r * math.sin(aa))
        return self

    def rotate(self, rad):
        s = math.sin(rad)
        c = math.cos(rad)
        for i in range(len(self.points)):
            (x, y) = self.points[i]
            self.points[i][0] = c * x - s * y;
            self.points[i][1] = s * x + c * y;
        return self

    def translate(self, x, y):
        for i in range(len(self.points)):
            self.points[i][0] += x
            self.points[i][1] += y
        return self

    def scale(self, scale):
        for i in range(len(self.points)):
            self.points[i][0] *= scale
            self.points[i][1] *= scale
        return self

    def addPolygon(self, polygon):
        for p in polygon:
            self.points.append(p)
        return self
        

class SvgCircle(SvgPolygon):
    def __init__(self, r, x=0, y=0, step=10):
        super().__init__()
        for a in range(0,360,step):
            a2 = a / 180.0 * math.pi
            self.lineTo( r * math.cos(a2), r * math.sin(a2))
        
        
class SvgGroup(SvgObj):
    def __init__(self):
        super().__init__()
        self.data = []

    def add(self,obj):
        self.data.append(obj)

    def svg(self):
        s = "<g"
        for i in self.dict.items():
            s += ' ' + i[0] + '="' + i[1] + '"'
        s += ">\n"
        for obj in self.data:
            s += obj.svg()
        s += "</g>\n";
        return s

        
class SvgGen:
    def __init__(self):
        self.data = []

    def add(self, obj):
        self.data.append(obj)
        
    def addPolygon(self, polygon, **kwargs):
        poly = SvgPolygon()
        poly.setPoints(polygon)
        poly.setDict(kwargs)
        self.data.append(poly)
            
    def addPolygons(self, polygons, **kwargs):
        for p in polygons:
            poly = SvgPolygon()
            poly.setPoints(p)
            poly.setDict(kwargs)
            self.data.append(poly)
        
    def write(self,path):
        with open(path, mode='w') as f:
            f.write('<?xml version="1.0" encoding="utf-8" ?>\n' +
                    '<svg baseProfile="full" version="1.1"' +
                    ' xmlns="http://www.w3.org/2000/svg"' +
                    ' xmlns:ev="http://www.w3.org/2001/xml-events"' +
                    ' xmlns:xlink="http://www.w3.org/1999/xlink">\n')
            for obj in self.data:
                f.write(obj.svg())
            f.write('</svg>\n')
            

if __name__ == '__main__':
    p = SvgPolygon()
    p.lineTo(100,100)
    p.lineTo(200,200)
    p.translate(10,20)
    print(p.points)
    

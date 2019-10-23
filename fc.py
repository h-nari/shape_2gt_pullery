import numpy as np

def fitCurve( points, error):
    pts = np.array(points)
    tHat1 = computeTangent(pts[0], pts[1])
    tHat2 = computeTangent(pts[-1],pts[-2])
    bz = fitCubic(pts, tHat1, tHat2, error)
    return bz

def computeTangent(u, v):
    v = v - u
    r = np.linalg.norm(v)
    return v / r

def fitCubic(pts, tHat1, tHat2, error):
    maxIterations = 4
    iterationError = error * error

    if(len(pts) == 2):
        dist = np.linalg.norm(pts[0] - pts[1]) / 3.0
        return [pts[0], pts[0] + dist * tHat1, pts[1] - dist * tHat2, pts[1]]

    u = chordLengthParameterized(pts)
    bezCurve = generateBezier(pts, u, tHat1, tHat2)

    maxError,splitPoint = computeMaxError(pts, bezCurve, u)
    if(maxError < error):
        return bezCurve

    if maxError < iterationError:
        for i in range(maxIterations):
            uPrime = reparameterize(pts, u, bezCurve)
            bezCurve = generateBezier(pts, uPrime, tHat1, tHat2)
            maxError,splitPoint = computeMaxError(pts, bezCurve, prime)
            if maxError < error:
                return bezCurve
            u = uPrime
            
    tHat3 = computeTangent(pts[splitPoint],pts[splitPoint-1])
    bz1 = fitCubic(pts[0:splitPoint+1], tHat1,tHat3, error)
    tHat4 = computeTangent(pts[splitPoint],pts[splitPoint+1])
    bz2 = fitCubic(pts[splitPoint:], tHat4,tHat2, error)
    bz1.extend(bz2[1:])
    return bz1

def chordLengthParameterized(pts):
    u = np.zeros(len(pts))
    for i in range(1,len(pts)):
        u[i] = u[i-1] + np.linalg.norm(pts[i] - pts[i-1])
    
    u /= u[-1]
    return u

def b0(t): return (1.0-t)* (1.0-t)* (1.0-t) 
def b1(t): return 3*(1.0-t)* (1.0-t)* t
def b2(t): return 3*(1.0-t)* t * t
def b3(t): return t*t*t

def generateBezier(pts, uPrime, tHat1, tHat2):
    a = np.empty([len(pts),2,2])
    for i in range(len(pts)):
        a[i][0] = tHat1 * b1(uPrime[i])
        a[i][1] = tHat2 * b2(uPrime[i])
    c = np.zeros([2,2])
    x = np.zeros(2)
    for i in range(len(pts)):
        c[0][0] += np.dot(a[i][0], a[i][0])
        c[0][1] += np.dot(a[i][0], a[i][1])
        c[1][0] += np.dot(a[i][1], a[i][0])
        c[1][1] += np.dot(a[i][1], a[i][1])
        tmp = pts[i] - (pts[0] * b0(uPrime[i]) + pts[0] * b1(uPrime[i]) + 
                        pts[-1] * b2(uPrime[i]) + pts[-1] * b3(uPrime[i]))
        x[0] += np.dot(a[i][0], tmp)
        x[1] += np.dot(a[i][1], tmp) 

    det_c0_c1 = c[0][0] * c[1][1] - c[1][0] * c[0][1]
    det_c0_x  = c[0][0] * x[1]    - c[0][1] * x[0]
    det_x_c1  = x[0]    * c[1][1] - x[1]    * c[0][1]
    if det_c0_c1 == 0.0:
        det_c0_c1 = c[0][0] * c[1][1] * 10e-12
    alpha_l = det_x_c1 / det_c0_c1
    alpha_r = det_c0_x / det_c0_c1

    if alpha_l < 1.0e-6 or alpha_r < 1.0e-6:
        print('pts[0]:',pts[0],'pts[-1]:',pts[-1])
        dist = np.linalg.norm(pts[0] - pts[-1]) / 3.0
        alpha_l = alpha_r = dist

    return [pts[0], pts[0]+tHat1 *alpha_l, pts[-1]+tHat2*alpha_r, pts[-1]]


def computeMaxError(pts, bezCurve, u):
    splitPoint = int((len(pts) + 1)/ 2)
    maxDist = 0.0
    for i in range(1,len(pts)):
        p = bezierII(3, bezCurve, u[i])
        v = p - pts[i]
        dist = np.linalg.norm(v)
        if dist >= maxDist:
            maxDist = dist
            splitPoint = i
    return maxDist, splitPoint

def bezierII(degree, v, t):
    vtemp = np.array(v[0:degree+1])
    for i in range(1, degree+1):
        for j in range(degree-i+1): 
            vtemp[j] = (1.0 - t) * vtemp[j] + t * vtemp[j+1]
    return vtemp[0]

def reparameterize(pts, u, bezCurve):
    uPrime = np.empty(len(pts))
    for i in range(len(pts)):
        uPrime[i] = newtonRaphsonRootFind(bezCurve, pts[i], u[i])
    return uPrime

def newtonRaphsonRootFind(q, p, u):
    q1 = np.empty([3,2])
    q2 = np.empty([2,2])

    q_u = bezierII(3, q, u)
    for i in range(3):
        q1[i] = (q[i+1] - q[i]) * 3;
    for i in range(2):
        q2[i] = (q1[i+1] - q1[i]) * 2;
    q1_u = bezierII(2, q1, u)
    q2_u = bezierII(1, q2, u)

    numerator = np.dot(q_u - p, q1_u)
    denominotor = np.dot(q1_u, q1_u) + np.dot(q_u - p, q2_u)
    return u - numerator / denominator;


if __name__ == '__main__':
    bz = fitCurve([ ( 0.0, 0.0 ), ( 0.0, 0.5 ), ( 1.1, 1.4 ), ( 2.1, 1.6 ),
	            ( 3.2, 1.1 ), ( 4.0, 0.2 ), ( 4.0, 0.0 )], 4)
    print('bz:',bz)
    

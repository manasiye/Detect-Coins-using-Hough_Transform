import numpy as np
import cv2
from scipy import signal as sp
import scipy.ndimage as ndi
import math,random,scipy,cv2

class Points:
    
    def __init__(self,v1,v2):
        self.x = v1
        self.y = v2

class houghTransform:
    
    def __init__(self, filename):
        self.filename = filename;
        self.loadImage();
        self.preprocess();
        self.blur();
        self.convolution();    
        self.thinningEdges();
        self.applyThreshold();
        self.collectEdgePts()
        self.circleDetect();
        #self.bonusDetectCntr();
        self.showNSaveImage();
            
    def preprocess(self):
        self.minimmRadii = 30
        self.maximmRadii = 53
        self.sobelVertKernel = np.array((-1,0,1,-2,0,2,-1,0,1))
        self.sobelVertKernel = np.reshape(self.sobelVertKernel,[3,3])
    
        self.sobelHoriKernel = np.array((-1,-2,-1,0,0,0,1,2,1))
        self.sobelHoriKernel = np.reshape(self.sobelHoriKernel,[3,3])
        
    def showNSaveImage(self):
        cv2.imshow('image',self.HoughDetectCircles)
        cv2.imwrite('DetectCirclesHoughTransform.jpg', self.HoughDetectCircles)    
        cv2.imwrite('convolutionDetectedCirclesGradHori.jpg', self.gradHori)    

    def collinear(self,pt1,pt2,pt3):
        val = ((pt2.x - pt1.x)*(pt3.y - pt1.y))
        val = (val - (pt3.x - pt1.x)*(pt2.y - pt1.y))
        if val == 0:
            return 1
        return 0
        
    def calcRadii(self,pt,cntr):
        return math.sqrt(math.pow(pt.x-cntr.x,2)+math.pow(pt.y-cntr.y,2))

        
    def streCirclePts(self, pt, index):
        self.circlePts.append(Points(pt[index].x,pt[index].y))
        del pt[index]
        
    def putBackAll(self):
        for i in range(np.shape(self.circlePts)[0]):
            self.edgePts.append(Points(self.circlePts[i].x,self.circlePts[i].y))
        del self.circlePts
    
    def putBack(self,index):
        self.edgePts.append(Points(self.circlePts[index].x,self.circlePts[index].y))
        del self.circlePts[index]
    
    def assignCoord(self,pts):
        notFull = 1
        thresd = 10
        thresA = 30
        thresB = 100
        i = 1
        cntr = Points(0,0)
        r = 0
        while notFull:
            if i > 20:
                i = 1
            self.circlePts = []
            inp = np.shape(pts)[0]/2
            index1 = random.randrange(1,inp)
            index2 = random.randrange(1,inp)
            index3 = random.randrange(1,inp)
            if index1 == index2 or index1 == index3 or index2 == index3:
                continue
            self.streCirclePts(pts,index1)
            self.streCirclePts(pts,index2)
            self.streCirclePts(pts,index3)
            d2 = self.calcRadii(self.circlePts[0],self.circlePts[1])
            d3 = self.calcRadii(self.circlePts[2],self.circlePts[0])
            d31 = self.calcRadii(self.circlePts[2],self.circlePts[1])
            collinear = self.collinear(self.circlePts[0],self.circlePts[1],self.circlePts[2])
            if collinear:
                continue
            cntr = self.findCentr(self.circlePts)
            r = self.calcRadii(self.circlePts[0],cntr)
            if (r > 53 or r < 30 or d2 < thresA or d2 > thresB) or (d3 < thresA or d3 > thresB) or (d31 < thresA or d31 > thresB):
                self.putBackAll()
                continue
                
            notFull = 0
        print " Whatave you try I wouldn't come here ",r
        return [cntr,r]
            
                
    def findCentr(self,circlePts):
        ## Applying Cramer's rule
        pt1 = circlePts[0]
        pt2 = circlePts[1]
        pt3 = circlePts[2]

        first = math.pow(pt2.x,2)+math.pow(pt2.y,2)-math.pow(pt1.x+pt1.y,2)
        third = math.pow(pt3.x,2)+math.pow(pt3.y,2)-math.pow(pt1.x+pt1.y,2)
        second = 2*(pt2.y-pt1.y)
        forth = 2*(pt3.y-pt1.y)
        denominator = 4*((pt2.x - pt1.x)*(pt3.y - pt1.y) - (pt3.x - pt1.x)*(pt2.y - pt1.y))
        a = ((first*forth)-(second*third))/denominator
        
        first = 2*(pt2.x - pt1.x)
        third = 2*(pt3.x - pt1.x)
        second = math.pow(pt2.x,2)+math.pow(pt2.y,2)-math.pow(pt1.x+pt1.y,2)
        forth = math.pow(pt3.x,2)+math.pow(pt3.y,2)-math.pow(pt1.x+pt1.y,2)
        b = ((first*forth)-(second*third))/denominator
        
        cntr = Points(0,0)
        cntr.x = a
        cntr.y = b
        return cntr
        
    
    def colctptsCircle(self,cntr,r,listSz):
        thresd = 3
        Np = 0
        i = 0
        while 1:
            if  i >= np.shape(self.edgePts)[0]-1:
                break
            d = self.calcRadii(self.edgePts[i],cntr)
            if d - r < thresd:
                self.streCirclePts(self.edgePts,i)
                Np = Np + 1
            i = i + 1
        return Np
            
    def markCntrPt(self,cntr,r):
        self.cntrPts.append([cntr.x,cntr.y,r])
        self.copyCircletoOrig()
    
    def bonusDetectCntr(self):
        thresR = 0.4
        thresMin = 10 ## minimum number of points left in edge vector when to stop detecting circle
        self.cntrPts = []
        while np.shape(self.edgePts)[0] > thresMin:
            [cntr,r] = self.assignCoord(self.edgePts)
            print "aa gaya bahar"
            listSz = np.shape(self.edgePts)[0]
            Np = self.colctptsCircle(cntr,r,listSz)
            if Np>= 2*3.14*r*thresR:
                print r
                self.markCntrPt(cntr,r)
                del self.circlePts
                print "found circle"
                break
            else:
                self.putBackAll()

    def copyCircletoOrig(self):
        self.HoughDetectCircles = cv2.imread(self.filename)  
        numOfCntrPts = np.shape(self.cntrPts)[0]                             
        for i in range(numOfCntrPts):
            x = self.cntrPts[i][0]
            y = self.cntrPts[i][1]
            r = self.cntrPts[i][2]+2
            for theta in range(360):
                a = round(x+r*math.cos(theta));
                b = round(y+r*math.sin(theta));
                if(self.checkBoundary(a,b)):
                    continue;
                self.HoughDetectCircles[a,b,0]=255
                self.HoughDetectCircles[a,b,1]=255
                self.HoughDetectCircles[a,b,2]=255
                self.gradHori[a,b] = 255
        self.numOfEdge = np.shape(self.edgePts)[0]
        
    def collectEdgePts(self):
        self.edgePts = []
        for i in range(self.width):
            for j in range(self.height):
                if(self.gradHori[i,j] >= 1):
                    self.edgePts.append(Points(i,j))  
                
        self.numOfEdge = np.shape(self.edgePts)[0]
        
    def circleDetect(self):
        ## for hough circle finding
        self.accumulator  = np.zeros((self.width,self.height));
        self.minR = self.minimmRadii
        self.maxR = self.minR + 3
        self.intenThres = 46
        self.cntrPts = []
        while self.maxR <= self.maximmRadii:
            self.countIntrsct = np.zeros((self.width, self.height,self.maxR));
            self.findCircles();
            self.storeCentrs();
            self.minR = self.maxR + 1
            self.maxR = self.minR + 3
            self.intenThres = self.intenThres + 1
        self.copyCircletoOrig()
     
## errorrng = 20 at intensity > 53
## 34 to 37 
## 38 to 41
## 42 to 45
## 46 to 49 
## 50 to 53 
    def findCircles(self):
        minR = self.minR;
        maxR = self.maxR;
        [width, height] = [self.width,self.height]
           
        for i in range(self.numOfEdge):
            x = self.edgePts[i].x
            y = self.edgePts[i].y
            for r in range(minR,maxR):
                r = (r - minR)/5+minR
                
                for theta in range(0,360,5):
                    a = round(x+r*math.cos(theta));
                    b = round(y+r*math.sin(theta));
                    if(self.checkBoundary(a,b)):
                        continue;
                    self.countIntrsct[a,b,r] = self.countIntrsct[a,b,r] + 1;
                            
    def checkBoundary(self,x,y):
        return ( x < 0 or y < 0 or x >= self.width or y >= self.height)
         
    def checkIfNoLocalMaxima(self,i,j,regRadii):
        notMaxima = False
        for x in range(i-regRadii,i+regRadii):
            for y in range(j-regRadii,j+regRadii):
                if  self.checkBoundary(x,y):
                    continue
                if self.countIntrsct[i,j].max() < self.countIntrsct[x,y].max() or self.accumulator [x,y] > 0:
                    notMaxima = True
                    break
            if notMaxima:
                break
        return notMaxima
               
    def maxIntenRadii(self,i,j):
        max = self.minR
        for r in range(self.minR+1,self.maxR):
            if self.countIntrsct[i,j,max] < self.countIntrsct[i,j,r]:
                max = r
        return max
    
    def emptyRegion(self,i,j,regRadii):
        for x in range(i-regRadii,i+regRadii):
            for y in range(j-regRadii,j+regRadii):
                if self.checkBoundary(x,y):
                    continue
                for z in range(self.minR,self.maxR):
                    self.countIntrsct[x,y,z] = 0

    def storeCentrs(self):
        minR = self.minR;
        maxR = self.maxR;
        regRadii = 20
        for i in range(self.width):
            for j in range(self.height):
                if  self.gradHori[i,j] <= 0 and self.countIntrsct[i,j].max() > self.intenThres :
                    if self.checkIfNoLocalMaxima(i,j,regRadii):
                        continue
                    r = self.maxIntenRadii(i,j)
                    self.emptyRegion(i,j,regRadii)
                    self.accumulator[i,j] = r
                    self.cntrPts.append([i,j,r])
        
    ## Find and fill all the adjacent pixels which may have accidently been removed      
    def neighbours(self,i, j):
        #self.saveCircleAround(i,j);
        for x in range(-2,3):
            for y in range(-2,3):
                if x == 0 and y == 0:
                    continue;
                if self.gradHori[i+x][j+y]==0 and self.gradVert[i+x][j+y]!=0:
                    self.gradHori[i+x][j+y]=255
                    self.neighbours(i+x, j+y)
                
    def floodFillNeihbour(self):
        for i in range(1, self.width-1):
            for j in range(1, self.height-1):
                if self.gradHori[i][j]:
                    self.gradHori[i][j] = 255
                    self.neighbours(i, j)
        return self.gradHori
    
    ## approximate edge angles to nearest degrees and find the significant edges and thin according to the intensity
    def thinningEdges(self):
        self.gradDir = scipy.arctan2(self.gradDY, self.gradDX)

        self.gradCopy = self.grad.copy();
        for currRow in range(1, self.width-1):
            for currCol in range(1, self.height-1):
                up = currCol - 1;
                down = currCol + 1;
                left = currRow - 1;
                right = currRow + 1;
                error = 22.5
                
                if self.gradDir[currRow][currCol] >= 0 and self.gradDir[currRow][currCol] < 0 + error or \
                    self.gradDir[currRow][currCol] >= 360 and self.gradDir[currRow][currCol] < 360 - error or \
                    self.gradDir[currRow][currCol] >= 180 - error and self.gradDir[currRow][currCol] < 180 + error :
	                if self.gradCopy[currRow][currCol] <= self.gradCopy[currRow][down] or \
                            (self.gradCopy[currRow][currCol] <= self.gradCopy[currRow][up]):
                            self.grad[currRow][currCol] = 0
                elif self.gradDir[currRow][currCol] >= 45 - error and self.gradDir[currRow][currCol] < 45 + error or \
                    self.gradDir[currRow][currCol] >= 135 - error and self.gradDir[currRow][currCol] < 135 + error:
                    if (self.gradCopy[currRow][currCol] <= self.gradCopy[left][down]) or \
                        (self.gradCopy[currRow][currCol] <= self.gradCopy[right][up]):
                        self.grad[currRow][currCol] = 0
                elif self.gradDir[currRow][currCol] >= 90 - error and self.gradDir[currRow][currCol] < 90 + error or \
                    self.gradDir[currRow][currCol] >= 270 - error and self.gradDir[currRow][currCol] < 270 + error:
                    if (self.gradCopy[currRow][currCol] <= self.gradCopy[right][currCol]) or \
                        (self.gradCopy[currRow][currCol] <= self.gradCopy[left][currCol]):
                        self.grad[currRow][currCol] = 0
 	        else: ## for angles in second and forth quadrant
                    if (self.gradCopy[currRow][currCol] <= self.gradCopy[right][down]) or \
                        (self.gradCopy[currRow][currCol] <= self.gradCopy[left][up]):
                        self.grad[currRow][currCol] = 0

    def applyThreshold(self):
        maxPx = self.grad.max();
    
        threshHori = 0.32
        threshVert = 0.24
        
        self.gradHori = self.grad.copy();
        self.gradVert = self.grad.copy();
        
        for x in range(self.width):
            for y in range(self.height):
                if self.grad[x][y]<threshHori*maxPx:
                    self.gradHori[x][y]=0;
                if self.grad[x][y]<threshVert*maxPx:
                    self.gradVert[x][y]=0;
                    
        self.gradVert = self.gradVert-self.gradHori
        self.floodFillNeihbour();
        
        
    def convolution(self):
        
        ## Apply convolutions with sobelKernels for edge detection
        self.gradDX = np.zeros((self.width,self.height), dtype = float)                        
        self.gradDY = np.zeros((self.width,self.height), dtype = float)
        
        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                pixH = 0
                pixV = 0
                for q in range(-1,2):
                    for t in range(-1,2):
                        pixH = pixH + (self.sobelVertKernel[1+t][1+q] * self.Blurred[x+q][y+t]);
                        pixV = pixV + (self.sobelHoriKernel[1+t][1+q] * self.Blurred[x+q][y+t]);
                self.gradDX[x][y] = pixH
                self.gradDY[x][y] = pixV
        
        
        self.grad = np.sqrt(self.gradDX * self.gradDX + self.gradDY * self.gradDY)
        self.grad = abs(self.grad);

    def blur(self):
        kernel = np.ones((5,5),np.uint8)
        self.Eroded = cv2.erode(self.image,kernel,iterations=5);
        self.Dilated = cv2.dilate(self.Eroded,kernel,iterations=5);
        self.Blurred = ndi.filters.gaussian_filter(self.Dilated,2.4)                   
        
    def loadImage(self):            
        self.image = cv2.imread(self.filename,0)
        [self.width,self.height]=self.image.shape;


if __name__ == "__main__":
    hough = houghTransform('HoughCircles.jpg');
    

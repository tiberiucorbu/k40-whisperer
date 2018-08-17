from math import sqrt


class ECoord():
    def __init__(self):
        self.reset()

    def reset(self):
        self.image      = None
        self.reset_path()

    def reset_path(self):
        self.ecoords    = []
        self.len        = 0
        self.move       = 0
        self.sorted     = False
        self.bounds     = (0,0,0,0)
        self.gcode_time = 0

    def make_ecoords(self,coords,scale=1):
        self.reset()
        self.len  = 0
        self.move = 0

        xmax, ymax = -1e10, -1e10
        xmin, ymin =  1e10,  1e10
        self.ecoords=[]
        Acc=.001
        oldx = oldy = -99990.0
        first_stroke = True
        loop=0
        for line in coords:
            x1 = line[0]*scale
            y1 = line[1]*scale
            x2 = line[2]*scale
            y2 = line[3]*scale
            dxline= x2-x1
            dyline= y2-y1
            len_line=sqrt(dxline*dxline + dyline*dyline)

            dx = oldx - x1
            dy = oldy - y1
            dist   = sqrt(dx*dx + dy*dy)

            # check and see if we need to move to a new discontinuous start point
            if (dist > Acc) or first_stroke:
                loop = loop+1
                self.ecoords.append([x1,y1,loop])
                if not first_stroke:
                    self.move = self.move + dist
                first_stroke = False

            self.len = self.len + len_line
            self.ecoords.append([x2,y2,loop])
            oldx, oldy = x2, y2
            xmax=max(xmax,x1,x2)
            ymax=max(ymax,y1,y2)
            xmin=min(xmin,x1,x2)
            ymin=min(ymin,y1,y2)
        self.bounds = (xmin,xmax,ymin,ymax)

    def set_ecoords(self, ecoords, data_sorted=False):
        self.ecoords = ecoords
        self.computeEcoordsLen()
        self.sorted = data_sorted

    def set_image(self,PIL_image):
        self.image = PIL_image

    def computeEcoordsLen(self):
        xmax, ymax = -1e10, -1e10
        xmin, ymin =  1e10,  1e10

        if self.ecoords == []:
            return
        on = 0
        move = 0
        time = 0

        for i in range(2,len(self.ecoords)):
            x1 = self.ecoords[i-1][0]
            y1 = self.ecoords[i-1][1]
            x2 = self.ecoords[i][0]
            y2 = self.ecoords[i][1]
            loop      = self.ecoords[i  ][2]
            loop_last = self.ecoords[i-1][2]

            xmax=max(xmax,x1,x2)
            ymax=max(ymax,y1,y2)
            xmin=min(xmin,x1,x2)
            ymin=min(ymin,y1,y2)

            dx = x2-x1
            dy = y2-y1
            dist = sqrt(dx*dx + dy*dy)

            if len(self.ecoords[i]) > 3:
                feed = self.ecoords[i][3]
                time = time + dist/feed*60

            if loop == loop_last:
                on   = on + dist
            else:
                move = move + dist

        self.bounds = (xmin,xmax,ymin,ymax)
        self.len = on
        self.move = move
        self.gcode_time = time

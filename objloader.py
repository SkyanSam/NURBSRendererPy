class ObjSurface:
    def __init__(self):
        self.cstype = ""
        self.degU = 0
        self.degV = 0
        self.startU = 0
        self.startV = 0
        self.endU = 0
        self.endV = 0
        self.vertices = []
        self.pts = []
        self.ptsIndices = []

class ObjTriangle:
    def __init__(self):
        self.vertices = []
        self.pts = []
        self.ptsIndices = []

class ObjLoader:
    filename = ""
    surfaces = []
    current = ObjSurface()
    def __init__(self, _filename):
        self.filename = _filename
        self.current = ObjSurface()
        self.surfaces = []
        f = open(self.filename, "r")
        lines = f.readlines()
        thistype = ""
        thisindex = 0
        self.surfaces.append(ObjSurface())
        for line in lines:
            split = line.split(' ')
            if not split[0].isnumeric():
                thistype = split[0]
                thisindex = 0
            match thistype:
                case "surf":
                    for e in split:
                        if e != "/":
                            if (thisindex == 1): self.current.startU = float(e)
                            if (thisindex == 2): self.current.endU = float(e)
                            if (thisindex == 3): self.current.startV = float(e)
                            if (thisindex == 4): self.current.endV = float(e)
                            elif (thisindex >= 5):
                                self.current.ptsIndices.append(int(e))
                                #self.current.pts.append(self.current.vertices[int(e)])
                                v = self.current.vertices[int(e)]
                                self.current.pts.append(v[0])
                                self.current.pts.append(v[1])
                                self.current.pts.append(v[2])
                case "deg":
                    self.current.degU = int(split[1])
                    self.current.degV = int(split[2])
                case "v":
                    self.current.vertices.append((float(split[1]), float(split[2]), float(split[3])))
                case "end":
                    self.surfaces.append(self.current)
                    self.current = ObjSurface()
                #case "parm":
                case "cstype":
                    self.cstype = split[1]
            thisindex += 1
objloader = ObjLoader("bezierpatch3.obj")
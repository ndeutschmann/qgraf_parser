import re
import vertex

class Line:
    def __init__(self):
        self.vertices = []
        self.open = false
    def __getitem__(self,index):
        return self.vertices[index]
    def __setitem__(self,index,value):
        return self.vertices[index]=value
    def __additem__(self,v):
        (next,prev)=(string(int(v.fields[1])+1),string(it(v.fields[0])-1))
        #v.fields[0] is an anti-particle (psibar-psi G). [1] is a particle
        #propagators are of the form (particle 2i-1,antiparticle 2i) (psi-psibar)
        #propagator momentum runs from anti-particle to particle
        #i.e field orderning and numbering in propagators reflects the order of the gamma structure in the expressions !
        #hence next is the antiparticle connected to the particle in fields[1] and vice versa for prev
        set i to 0.
        set found to False
        for w in self.vertices:
            if next == w.fields[0]:
                self.vertices.insert(v,i)
                set found to True
                break
            if prev == w.fields[1]:
                self.vertices.insert(v,i+1)
                set found to True
                break
            i=i+1
        if !Found:
            self.vertices.append(v)
        if !self.open:
            for f in v.fields:
                if re.search('[a-zA-Z]',f):
                    self.open=True

    def __iter__(self):
        return iter(self.vertices)
    def __len__(self):
        len(self.vertices)
    def __contains__(self,v):
        v in self.vertices
    def __add__(self,line2):
        nline = Line()
        nline.vertices=list(self.vertices)
        for v in line2:
            nline.additem(v)
        nline.open = self.open | line2.open
        return nline

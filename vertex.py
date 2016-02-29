import re
import sys

FERMIONS = ["t","b"]

def pparse(p):
    lp=re.split("[+-]",p)
    for mom in [x for x in lp if x!='']:
        p=p.replace(mom,mom+",")
    lp=p.split(",")
    return [x for x in lp if x!='']
           

class Vertex:
    def __init__(self,element):
        try:
            self.momenta=element.find("momenta").text.split(",")
            self.type=element.find("type").text
            self.types=element.find("type").text.split(",")
            self.fields=element.find("fields").text.split(",")
            for i in range(0,len(self.fields)):
                if int(self.fields[i])<0:
                    self.fields[i]="ext"+str(-int(self.fields[i]))
        except:
            print "Error while defining vertex object"
    def writenextprop(self,file,line=1):
        if self.types[1]! in FERMIONS:
            print "No fermion coming out of this vertex ! Something is wrong."
        else:
            file.write("i_*(")
            lp=pparse(self.momenta[0])
            for p in lp:
                file.write("g_("+str(line)+","+p+")+")
            file.write("mt)*D("+self.momenta[0]+",mt)*d_(col"+self.fields[0]+",col"+str(int(self.fields[0])-1)+")")
    def contains(self,f):
        f in self.fields
    def output(self,file,line=1):
        if self.type=="tbar,t,g":
            file.write("i_*g*g_("+str(line)+",mu"+self.fields[2]+")*T(b"+self.fields[2]+",col"+self.fields[0]+",col"+self.fields[1]+")")
        elif self.type=="tbar,t,H":
            file.write("i_*Y*d_(col"+self.fields[0]+",col"+self.fields[1]+")")
        elif self.type=="H,H,H":
            file.write("i_*h3")
        elif self.type=="H,H,H,H":
            file.write("i_*h4")
        elif self.type=="g,g,g":
            file.write("(-g3*f(b"+self.fields[0]+",b"+self.fields[1]+",b"+self.fields[2]+")*(0")
            for i in range(0,3):
                j=(i+1)%3
                k=(i+2)%3
                p1=self.momenta[i]
                p2=self.momenta[j]
                lp1=re.split("[+-]",p1) #get a list of all momenta combined in leg i
                lp2=re.split("[+-]",p2) #get a list of all momenta combined in leg j
                lp1[:]=[x for x in lp1 if x!='']
                lp2[:]=[x for x in lp2 if x!='']
                #add the index k to each individual momentum and then p-k
                for mom in lp1:
                    if p1!="0":
                        p1=p1.replace(mom,mom+"(mu"+self.fields[k]+")")
                for mom in lp2:
                    if p2!="0":
                        p2=p2.replace(mom,mom+"(mu"+self.fields[k]+")")
                p="("+p1+"-("+p2+"))"
                file.write("+d_(mu"+self.fields[i]+",mu"+self.fields[j]+")*"+p)
            file.write("))")
        elif self.type=="g,g,g,g":
            i=0
            j=1
            k=2
            l=3
            file.write("(-i_)*g^2*(")
            file.write("f(b"+self.fields[i]+",b"+self.fields[j]+",bdummy)*f(b"+self.fields[k]+",b"+self.fields[l]+",bdummy)*(d_(mu"+self.fields[i]+",mu"+self.fields[k]+")*d_(mu"+self.fields[j]+",mu"+self.fields[l]+")-d_(mu"+self.fields[i]+",mu"+self.fields[l]+")*d_(mu"+self.fields[j]+",mu"+self.fields[k]+"))")
            file.write("+f(b"+self.fields[i]+",b"+self.fields[k]+",bdummy)*f(b"+self.fields[j]+",b"+self.fields[l]+",bdummy)*(d_(mu"+self.fields[i]+",mu"+self.fields[j]+")*d_(mu"+self.fields[k]+",mu"+self.fields[l]+")-d_(mu"+self.fields[i]+",mu"+self.fields[l]+")*d_(mu"+self.fields[j]+",mu"+self.fields[k]+"))")
            file.write("+f(b"+self.fields[i]+",b"+self.fields[l]+",bdummy)*f(b"+self.fields[j]+",b"+self.fields[k]+",bdummy)*(d_(mu"+self.fields[i]+",mu"+self.fields[j]+")*d_(mu"+self.fields[k]+",mu"+self.fields[l]+")-d_(mu"+self.fields[i]+",mu"+self.fields[k]+")*d_(mu"+self.fields[j]+",mu"+self.fields[l]+"))")
            file.write(")")
        else:
            print "ERROR: Unknown vertex type"
            print self.type

#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from vertex import *


graphs=XML(default_loader("grafs",parse))
diagrams=graphs.find("diagrams")

fermionvertices = ["tbar,t,H","tbar,t,g", "bbar,b,g"]:

for diagram in diagrams.getchildren():
    number=diagram.find("id").text
    filename="diagram"+str(number)+".frm"
    file=open(filename,"w+")
    file.write("format mathematica;\n")
    file.write("CFunction i,g,Y,h3,h4,D,mt,mH,gt,g3,g4;\n")#This could use an automation as well
    file.write("Tensor Tr(cyclic),T,Tp,f(antisymmetric),ff(rcyclic),Delta(symmetric);\n")
    file.write("Function TM,TT;\n")
    file.write("Symbols a,nf,NF,NA,cF,cA,[cF-cA/6],pt2,Dim;\n")
    file.write("Dimension NA;\n")
    file.write("AutoDeclare Index j,b;\n")
    file.write("Dimension NF;\n")
    file.write("AutoDeclare Indices i,col;\n")
    file.write("Dimension Dim;\n")
    file.write("AutoDeclare Vector p,k,q;\n")
    file.write("AutoDeclare Indices mu;\n")
    file.write("Dimension NF;\n")
    file.write("Off statistics;\n")

    file.write("Local Diagram = 1/NA*Delta(bext1,bext3)*(")    
    file.write("\n")
    NOvertices=diagram.find("vertices").getchildren()
    propagators=diagram.find("propagators").getchildren()
    prefactor=diagram.find("signsym").text
    np=int(diagram.find("defdata").find("incoming").text)
    nq=int(diagram.find("defdata").find("outgoing").text)

    vertices=[]
    fermionlines=[]
    nfvertices=[]

    #Initialize vertices objects, put them in a list
    for v in NOvertices:
        vertices.append(Vertex(v))


    #Sort vertices between fermionic and nonfermionic and create fermion lines
    for v in vertices:
        if v.type in fermionvertices
            if len(fermionlines)==0: #If there are no lines yet, create one
                fermionlines=[line()]
                fermionlines[0].addv(v)
            else: #If there exist lines
                found=False
                matches = []
                for line in fermionlines: 
                    if v in line:
                        found=True
                        matches.append(line)
                if found:
                    mergedline=line().addv(v)
                    for line in matches:
                        mergedline=mergedline+line
                        print len(fermionlines)#FOR TEST
                        fermionlines.remove(line)
                        print len(fermionlines)#FOR TEST
                    fermionlines.append(mergedline)
                if not found:
                    #print "This is a new line !"
                    fermionlines.append(line().addv(v))
        else:
            nfvertices.append(v)    

    file.write(prefactor)

    count=0
    for line in fermionlines:
        for v in line:
            file.write("*")
            v.output(file,count)
            file.write("*")
            v.writenextprop(file,count)
        count=count+1
    for v in nfvertices:
       file.write("*")
       v.output(file)

    for p in propagators:

        if p.find("field").text=="g":
            i=2*int(p.find("id").text)
            file.write("*(-i_)*D("+p.find("momentum").text+",0)*d_(mu"+str(i)+",mu"+str(i-1)+")*d_(b"+str(i)+",b"+str(i-1)+")")
        elif p.find("field").text=="H":
            file.write("*i_*D("+p.find("momentum").text+",mH)")


    file.write(");\n")
    for i in range(1,len(fermionlines)+1):
        file.write("Tracen,"+str(i)+";\n")
    file.write("#call SUn\n")
    file.write("id a=1/2;\n")
    file.write("id pt2 = 2*(p1.q1)*(p2.q1)/(p1.p2);\n")
    file.write("id pt2^-1 = (p1.p2)/(2*(p1.q1)*(p2.q1));\n")
    file.write("id mH=0;\n")
    file.write("id p1.p1=0;\n")
    file.write("id p2.p2=0;\n")
    file.write("id q1.q1=0;\n")
    file.write("id Delta(bext1?,bext3?)=d_(bext1,bext3);\n")
    file.write(".sort\n")
    file.write("Print ;\n")
    file.write(".end")


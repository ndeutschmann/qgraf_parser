#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from vertex import *
from line import*

graphs=XML(default_loader("grafs",parse))
diagrams=graphs.find("diagrams")

fermionvertices = ["tbar,t,H","tbar,t,g","tbar,t,g,H","tbar,t,g,g","tbar,t,g,g,H"]
for diagram in diagrams.getchildren():
    number=diagram.find("id").text
    print ""
    print ""
    print "Starting diagram number "+number
    filename="diagram"+str(number)+".frm"
    file=open(filename,"w+")
    file.write("format mathematica;\n")
    file.write("CFunction i,g,Y,h3,h4,v,Ctg,mt,s,mH,Denom;\n")#This could use an automation as well
    file.write("Tensor Tr(cyclic),T,Tp,f(antisymmetric),ff(rcyclic),Delta(symmetric);\n")
    file.write("Function TM,TT;\n")
    file.write("Symbols a,nf,NF,NA,cF,cA,[cF-cA/6],Dim;\n")
    file.write("Dimension NA;\n")
    file.write("AutoDeclare Index j,b;\n")
    file.write("Dimension NF;\n")
    file.write("AutoDeclare Indices i,col;\n")
    file.write("Dimension Dim;\n")
    file.write("AutoDeclare Vector p,k,q;\n")
    file.write("AutoDeclare Indices mu;\n")
    file.write("Dimension NF;\n")
    file.write("Off statistics;\n")

    file.write("Local Diagram = (p1.p2*d_(muext1,muext3)-p1(muext3)*p2(muext1))*d_(bext1,bext3)*(")
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
        if v.type in fermionvertices:
            if len(fermionlines)==0: #If there are no lines yet, create one
                fermionlines=[Line()]
                fermionlines[0].additem(v)
            else: #If there exist lines
                found=False
                matches = []
                for line in fermionlines:
                    if v in line:
                        found=True
                        matches.append(line)
                if found:
                    mergedline=Line()
                    mergedline.additem(v)
                    for line in matches:
                        mergedline=mergedline+line
                        print "BEFORE REMOVAL "+str(len(fermionlines))#FOR TEST
                        fermionlines.remove(line)
                        print "AFTER REMOVAL "+str(len(fermionlines))#FOR TEST
                    fermionlines.append(mergedline)
                if not found:
                    nl = Line()
                    nl.additem(v)
                    fermionlines.append(nl)
        else:
            nfvertices.append(v)

    file.write(prefactor)

    count=0

    for line in fermionlines:
        print "Is the line open ? "+str(line.open)
        if line.open:
            print "opening the line"
            line[0].openline(file,count)
        else:
            print "not doing anything: the line is not open"
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
            file.write("*(-i_)*Denom({},0)*d_(mu{},mu{})*d_(b{},b{})".format(p.find("momentum").text,str(i),str(i-1),str(i),str(i-1)))
        elif p.find("field").text=="H":
            file.write("*i_*Denom({},mH)".format(p.find("momentum").text))


    file.write(");\n")
    for i in range(0,len(fermionlines)):
        file.write("Tracen,"+str(i)+";\n")
    file.write("#call SUn\n")
    file.write("id a=1/2;\n")
    file.write("id p1.p1=0;\n")
    file.write("id p2.p2=0;\n")
    file.write("id q1.q1=s;\n")
    file.write(".sort\n")
    file.write("Print ;\n")
    file.write(".end")

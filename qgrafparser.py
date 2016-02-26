#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from vertex import *



graphs=XML(default_loader("grafs",parse))
diagrams=graphs.find("diagrams")


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
        if v.type in ["tbar,t,H","tbar,t,g"]:
            #print "I found a fermion vertex: "+v.type
            #print str(v.fields)
            if len(fermionlines)==0: #If there are no lines yet, create one
                fermionlines=[[v]] 
                #print "Created a fermion line"
            else: #If there exist lines
                sv=set([str(int(v.fields[0])-1),str(int(v.fields[1])+1)]) # Make a set of fermions connected to this vertex (2i is the antifermion connected to fermion 2i-1)
                found=False
                matches = []
                for line in fermionlines: 
                    for vl in line:
                        if bool(set(vl.fields)&sv): #If non zero intersection it's our line
                            found=True
                            matches.append(line)
                            break
                if found:
                    #print "This matches "+str(len(matches))+"lines"
                    mergedline = [v]
                    for line in matches:
                        #print "one line contains"
                        #for v in line:
                            #print str(v.fields)
                        mergedline=mergedline+line
                        #print "mergedline contains"
                        #for v in mergedline:
                            #print str(v.fields)
                        fermionlines.remove(line)
                    fermionlines.append(mergedline)
                if not found:
                    #print "This is a new line !"
                    fermionlines.append([v])
        else:
            nfvertices.append(v)    

    file.write(prefactor)

    count=0
    #print "There are "+str(len(fermionlines))+"lines"
    for line in fermionlines:
        #print "Line "+str(count)
        #for v in line:
            #print str(v.fields)
        count=count+1
        nv=len(line)
        v=line[0]
        line.remove(v)
        i=0
        while(i<nv):
            file.write("*")
            #print "vertext number "+str(v.fields)
            v.output(file,count)
            file.write("*")
            v.writenextprop(file,count)
            i=i+1          
            for vv in line:
                if int(vv.fields[1])+1==int(v.fields[0]):
                    v=vv
                    line.remove(vv)
                    break
                
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
#    file.write("Local A1 = (d_(muext1,muext3) - p2(muext1)*p1(muext3)/(p1.p2))*Diagram;\n")
    file.write("Local A9 = (d_(muext1,muext3) - 2*p2.q1*q1(muext1)*p1(muext3)/(pt2*p1.p2) - 2*p1.q1*q1(muext3)*p2(muext1)/(pt2*p1.p2) + 2*q1(muext1)*q1(muext3)/pt2 )*Diagram;\n")
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
    file.write("Print A9;\n")
    file.write(".end")


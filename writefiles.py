import shelve
##filename = open("Pictures\\interfile1.tx","w")
##filename.close()


##filename2 = open("SubFiles\\transfile2.tx","w")
##filename2.close()


##filename2 = shelve.open("C:\\SheetMetal Work\\TOBESHEETMETAL.cd","r")

try:
    filename2 = shelve.open("C:\\SheetMetal Work\\squaretocylindertest.cd")

    valuekey = filename2.keys()
##    accept = filename2['format']
    valuedict2 = filename2['input']
##    print filename2.keys()
    print valuedict2
##    print type(valuedict)
##    filename2.close()
    print valuekey
except KeyError:
    print "Could no Open file. file may be corrupt or damaged"

##except Exception,message:
##    print "Unknown File"
raw_input("Enter your name")

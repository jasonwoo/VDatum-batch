#Convert LAS files using command line VDatum version 3.3
#Jason  - April 25, 2014
##Sample VDatum cmd:
#java -jar vdatum.jar ihorz:nad83:utm:m:10 ivert:navd88:m:height ohorz:ihorz overt:mhw:m:height -nodata -file:las:las:e:\\vdatum_batch_proc\or_test_file_subset.las;e:\\vdatum_batch_proc\result\
#Assumes an input LAS file in NAD83 UTM meters 

import os,popen2,time,glob

####### Variables to edit ################
vdatumpath = 'C:\\vdatum33' # Path to the VDatum command line jar file
invdatum = 'nad83' #Input vertical datum
outvdatum = 'mhw'  #Output vertical datum
utmzone = 18 #UTM zone / northern UTM zone shall be 1 to 60, southern UTM zone shall be -1 to -60
##########################################

start = time.time() # Start the timer

lasf = glob.glob('*.las')

laspath = os.getcwd()

if not os.path.isdir(''+outvdatum+'_output'):
    os.makedirs(''+outvdatum+'_output')

for infile in lasf:
            
    os.chdir(vdatumpath)
    vconvert='java -jar vdatum.jar ihorz:nad83:utm:m:%s ivert:%s:m:height ohorz:ihorz overt:%s:m:height -nodata -file:las:las:%s\\%s;%s\\%s_output'%(utmzone,invdatum,outvdatum,laspath,infile,laspath,outvdatum)
    popen2.popen4(vconvert)

    print '\nConverted '+infile+' from '+invdatum+' to '+outvdatum+' with VDatum...'

    
print '\n\nProcessing completed in: %s' % ((time.time() - start)/60),'minutes'

del start

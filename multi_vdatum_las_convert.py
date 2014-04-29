#Convert LAS files using command line VDatum version 3.3 - multi-threaded version
#JasonW  - April 25, 2014
##Sample VDatum cmd:
#java -jar vdatum.jar ihorz:nad83:utm:m:10 ivert:navd88:m:height ohorz:ihorz overt:mhw:m:height -nodata -file:las:las:e:\\vdatum_batch_proc\or_test_file_subset.las;e:\\vdatum_batch_proc\result\
#
#Assumes an input LAS file in NAD83 UTM meters 

import os,time,glob,Queue,threading

####### Variables to edit ###############################
vdatumpath = 'C:\\vdatum33' #Path to the VDatum jar file
invdatum = 'nad83' #Input vertical datum
outvdatum = 'mhw'  #Output vertical datum
utmzone = 18 #UTM zone / northern UTM zone shall be 1 to 60, southern UTM zone shall be -1 to -60
numProc = 6 #Number of processes to spawn
#########################################################

start = time.time() # Start the timer

if not os.path.isdir(''+outvdatum+'_output'):
    os.makedirs(''+outvdatum+'_output')

lasf = glob.glob('*.las')

laspath = os.getcwd()

#multi-threading snippet tweezed from sellars    
queue = Queue.Queue()

class ThreadJobs(threading.Thread):
    
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            # get job from queue
            myJob = self.queue.get()
            infile = myJob
            os.chdir(vdatumpath)           
            vconvert = r'java -jar vdatum.jar ihorz:nad83:utm:m:%s ivert:%s:m:height ohorz:ihorz overt:%s:m:height -nodata -file:las:las:%s\\%s;%s\\%s_output'%(utmzone,invdatum,outvdatum,laspath,infile,laspath,outvdatum)#VDatum Conversion
            os.system(vconvert)

            # signal queue job is done
            self.queue.task_done()

def main():
    # spawn a pool of workers, and pass them queue instance
    for i in range(numProc):
        t = ThreadJobs(queue)
        t.setDaemon(True)
        t.start()
    # populate queue with jobs
    for infile in lasf:
        queue.put(infile)
    # wait on the queue until everything has been processed
    queue.join()
    return 'Done'

main()
     
print '\n\nProcessing completed in: %s' % ((time.time() - start)/60),'minutes'

del start

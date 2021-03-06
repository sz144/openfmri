#!/usr/bin/env python
""" run_copy_stripped.py - copy skull-stripped images from freesurfer dirs
"""

## Copyright 2011, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import os,sys

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

if len(sys.argv)>1:
    dataset=sys.argv[1]
else:
    usage()
    
if len(sys.argv)>2:
    basedir=sys.argv[2]
    if not os.path.exists(basedir):
        print 'basedir %s does not exist!'%basedir
        sys.exit(1)
else:
    basedir='/corral-repl/utexas/poldracklab/openfmri/staged/'
 
if len(sys.argv)>3:
    subdir=sys.argv[3]
    if not os.path.exists(subdir):
        print 'subdir %s does not exist!'%subdir
        sys.exit(1)
else:
    subdir='/corral-repl/utexas/poldracklab/openfmri/subdir/'
 

outfile=open('run_copy_stripped_%s.sh'%dataset,'w')


dsdir=os.path.join(basedir,dataset)
for root,dirs,files in os.walk(dsdir):
    for f in files:
        if f.rfind('highres001.nii.gz')>-1 and root.find(dataset)>-1:
            f_split=root.split('/')
            outfile.write('mri_convert --out_orientation LAS %s/%s_%s/mri/brainmask.mgz --reslice_like %s/highres001.nii.gz  %s/highres001_brain.nii\n'%(subdir,f_split[-3],f_split[-2],root,root))
            outfile.write('gzip %s/highres001_brain.nii\n'%root)
            outfile.write('fslmaths %s/highres001_brain.nii.gz -thr 1 -bin %s/highres001_brain_mask.nii.gz\n'%(root,root))

outfile.close()

            
print 'now launch using:'
print 'sh run_copy_stripped_%s.sh'%dataset




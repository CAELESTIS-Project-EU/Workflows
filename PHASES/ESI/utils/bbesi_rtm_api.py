# -*- coding: utf-8 -*-
"""
@author: Santiago Montagud Pérez de Lis
ESI Group
DoE

#
#------------------------------------------------------------------------------
"""
#
#from builtins import str
import sys
import os
import logging
log = logging.getLogger()
import re
import subprocess
import itertools
import time

re_newkey = re.compile('^[\w|\s]{6}\/')

class Visual_API():
    def __init__(self, metaData={}):
        metaData1 = {
            'Name': 'ESI RTM filling'}

    def LaunchMacro(self, MacroName):
        """Modifies the property value in the include file"""
        ModPermFile = os.path.join(self.SourceFilesPath, MacroName)
        Modify_vdb(self,self.solverVEPath, ModPermFile)
        print('Macro ' + MacroName + ' has been executed')
                
    def solveStep(self, runInBackground=False):

        OUTPUT_PATH=os.path.normpath(self.outputFile)

        #This code uses the terminal to launch the simulation
        if self.simtype=='RTM':

            print("RTM SOLVER")
            #print("modified np to the end")
                
            cmd = ''
            cmd += '"' + self.solverPath + '"'
            cmd += ' -rtm -userf -compiler ' + '"'
            cmd +=  self.vsPath + '"'
            cmd += ' -rtm -skippre -prefix '
            cmd += '"' + r'{}'.format(self.inputFile) + '"'
            if (self.mpidir):
                cmd += ' -mpidir ' + str(self.mpidir)
            cmd += r" > "
            cmd += '"' + OUTPUT_PATH + '" -np ' + str(self.np)
            
            try:
                ret_code = subprocess.call(cmd, shell=True)
            except subprocess.CalledProcessError as e:
                print("Error while running {}: {}".format(linesToWrite, str(e)))
                # If the command failed, e.output contains the standard output (if any)
                print("Error Output:", e.output)
                # e.stderr contains the standard error (if any)
                print("Standard Error:", e.stderr)
                raise Exception(f"Execution failed: {e}")
            print("RTM FILLING SOLVER OK")

        if self.simtype=='CURING':
            print("RTM CURING SOLVER")
            #print("modified np to the end")
            cmd = ''
            cmd += '"' + self.solverPath + '"'
            cmd += ' -rtm -userf -compiler ' + '"'
            cmd +=  self.vsPath + '"'
            cmd += ' -rtm -skippre -prefix '
            cmd += '"' + r'{}'.format(self.inputFile) + '"'
            if (self.mpidir):
                cmd += ' -mpidir ' + str(self.mpidir)
            cmd += r" > "
            cmd += '"' + OUTPUT_PATH + '" -np ' + str(self.np)
            
            try:
                ret_code = subprocess.call(cmd, shell=True)
                if ret_code != 0:
                        raise Exception("Solver return exit code" + str(ret_code))
            except subprocess.CalledProcessError as e:
                print("Error while running {}: {}".format(linesToWrite, str(e)))
                # If the command failed, e.output contains the standard output (if any)
                print("Error Output:", e.output)
                # e.stderr contains the standard error (if any)
                print("Standard Error:", e.stderr)
                raise Exception(f"Execution failed: {e}")
            print("RTM CURING SOLVER OK")
                
        if self.simtype=='DISTORTION':
            print("DISTORTION SOLVER")

            # Specify the path to your .bat file
            bat_file_path = self.BatFilePath
            #print(bat_file_path)
            print('running pam distortion')
            current_dir = os.getcwd()
            #print(current_dir)
            directory_bat_path = os.path.dirname(bat_file_path)
            os.chdir(directory_bat_path)
            machine = self.machine

            if machine == 'BORLAP020':
                with open(bat_file_path,'w+') as BATF:
                    linesToWrite = '@echo off' + '\n'
                    linesToWrite = linesToWrite + 'start "Tail output file" "' + self.DistortionsolverWinTailPath + '" "' + self.outputFile + '" \n'
                    linesToWrite = linesToWrite + 'call "' + self.solverPath + '" -fp 2 -np 1 "' + self.inputFile + '"   > "' + self.outputFile +  '" 2>&1 \n'
                    linesToWrite = linesToWrite + '@echo off' + '\n'
                    BATF.write(linesToWrite)
                    BATF.close()
                #Use subprocess to run the .bat file
                try:                
                    result_launch = subprocess.run(bat_file_path)
                    print("Standard Output:", result_launch.stdout)
                except subprocess.CalledProcessError as e:
                    print("Error while running {}: {}".format(bat_file_path, str(e)))
                    # If the command failed, e.output contains the standard output (if any)
                    print("Error Output:", e.output)
                    # e.stderr contains the standard error (if any)
                    print("Standard Error:", e.stderr)
            else:
                try:
                    
                    if self.mpidir:
                        mpi_flags = " -mpidir=" + self.mpidir + " "
                    else:
                        mpi_flags = ""

                    linesToWrite = self.solverPath + " " + self.inputFile + mpi_flags + "-np " + str(self.np) + " > " + self.outputFile +  ' 2>&1'
                    print("DISTORTION launch command : ")
                    print(linesToWrite)
                    ret_code = subprocess.call(linesToWrite, shell=True)
                    if ret_code != 0:
                        raise Exception("Solver return exit code" + str(ret_code))
                except subprocess.CalledProcessError as e:
                    print("Error while running {}: {}".format(linesToWrite, str(e)))
                    # If the command failed, e.output contains the standard output (if any)
                    print("Error Output:", e.output)
                    # e.stderr contains the standard error (if any)
                    print("Standard Error:", e.stderr)
                    raise Exception(f"Execution failed: {e}")
            os.chdir(current_dir)
            
            return True

    def isSolved(self):
        """
        Check whether solve has completed.

        :return: Returns true or false depending whether solve has completed when executed in background.
        :rtype: bool
        """

        if self.solverStatus==0:
            return False
        elif self.solverStatus==1:
            lastoutline = tail(os.path.normpath(self.outputFile))
        elif self.solverStatus==2:
            return True
        else:
            return False

#%% RTM IO functions
def tail(filepath):
    with open(filepath, "rb") as f:
        first = f.readline()      # Read the first line.
        f.seek(-2, 2)             # Jump to the second last byte.
        while f.read(1) != b"\n": # Until EOL is found...
            try:
                f.seek(-2, 1)     # ...jump back the read byte plus one more.
            except IOError:
                f.seek(-1, 1)
                if f.tell() == 0:
                    break
        last = f.readline()       # Read last line.
    return last

def Modify_vdb(self,LaunchVEPath, ficout_py): #NumRun, Fc, c1, name_base, LaunchVEPath):
    # import subprocess
    # To modify the parameters by using a macro, Visual Environment must be called
    ACTIVECONF=r'Trade:All'
    
    if self.simtype=='DISTORTION':
            
        ACTIVEAPP=r'VisualDISTORTION'
    else:
        ACTIVEAPP=r'VisualRTM'
        
    DISPLAYMODE=r' -nodisplay'

    if self.display == 1:
        cmd = ''
        cmd += '"' + LaunchVEPath + '"'
        cmd += ' -activeconfig ' + ACTIVECONF
        cmd += ' -activeapp ' + ACTIVEAPP
        cmd += ' -sessionrun '
        cmd += '"' + ficout_py + '"'

    else:
        cmd = ''
        cmd += '"' + LaunchVEPath + '"'
        cmd += ' -activeconfig ' + ACTIVECONF
        cmd += ' -activeapp ' + ACTIVEAPP
        cmd += DISPLAYMODE
        cmd += ' -sessionrun '
        cmd += '"' + ficout_py + '"'
        cmd += ' -exit '
    
    #print("Visual command is : ", cmd)    

    def run(*popenargs, **kwargs):
        input = kwargs.pop("input", None)
        check = kwargs.pop("handle", False)

        if input is not None:
            if 'stdin' in kwargs:
                raise ValueError('stdin and input arguments may not both be used.')
            kwargs['stdin'] = subprocess.PIPE

        process = subprocess.Popen(*popenargs, **kwargs)
        try:
            stdout, stderr = process.communicate(input)
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        if check and retcode:
            raise subprocess.CalledProcessError(
                retcode, process.args, output=stdout, stderr=stderr)
        return retcode, stdout, stderr

    returncode = 0
    proc = run(cmd,\
              stdout=subprocess.PIPE,\
              stderr=subprocess.PIPE,\
#              timeout=600,\
#              check=True,\
              shell=True, universal_newlines=True)
#returncode = proc.returncode





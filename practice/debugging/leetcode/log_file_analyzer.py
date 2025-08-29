"""
Given a list of logs like:

INFO: job_123 started
ERROR: job_123 failed
INFO: job_456 started
INFO: job_789 started
ERROR: job_789 failed
Write a Python function that returns the set of job IDs that failed.

"""

# Solution Idea:
"""
Read in the beginning of the line for "Error".
    each line = entry in list
    then check for 'job_NUM' later on in the line, then strip the 'job_' and insert 
    into map of 1 to many, FAIL:[123, 345, 456...]
"""

import os

def lf_analyze(log_file):
    errors = []
    with open(log_file, 'r')as file:
        for line in file:
            #print(line)
            if 'E' in line:
                temp = line.split('job_')
                job_id= temp[1].split(' ')
                print(job_id[0])
                errors.append(job_id[0])
    return errors

def v2_lf_analyse(log_file):
    errors = []
    with open(log_file, 'r')as file:
        for line in file:
            line  = line.strip()
            print(line.split())
            if line and line.startswith("ERROR:"):
                temp = line.split('job_')
                job_id= temp[1].split(' ')
                print(job_id[0])
                errors.append(job_id[0])
    return errors

def set_lf_analyze(log_file):
    errors = set()
    with open(log_file, 'r')as file:
        for line in file:
            #print(line)
            if 'E' in line:
                temp = line.split('job_')
                job_id= temp[1].split(' ')
                print(job_id[0])
                errors.add(job_id[0])
    return errors    

if __name__ == "__main__":
    log_file = os.path.join(os.getcwd(),"log_file.log")
    job_errors = lf_analyze(log_file)
    set_job_errors = set_lf_analyze(log_file)
    v2_job_errors = v2_lf_analyse(log_file)
    print(f"Simple List based collection of errors:\n {job_errors}\n")
    print(f"Simple List based collection of errors with improved read:\n {v2_job_errors}\n")
    print(f"Simple Set based collection of errors:\n {set_job_errors}\n")
    
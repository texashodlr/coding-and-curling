# Job Scheduler

"""
You are given a list of jobs, each with a job ID and its runtime in seconds. Assume all jobs start at the same time.

Write a function that returns the job ID of the job that finishes first.
jobs = [("job_a", 12), ("job_b", 5), ("job_c", 20), ("job_d", 7)]
"job_b"

Thoughts:
    We're basically given a list and need to find the smallest time so jobs[0][1] etc
    Traverse the list and then get the lowest item 
"""


#print(jobs[0][1])

def job_scheduler(jobs):
    start = jobs[0]
    for j in jobs:
        temp = j
        if temp[1] < start[1]:
            start = temp
    return start[0]

def job_scheduler_v2(jobs):
    if not jobs:
        raise ValueError("jobs list is empty")
    return min(jobs, key=lambda x: x[1])[0]

def fastest_jobs(jobs):
    if not jobs: return[]
    m = min(t for _, t in jobs)
    print(m)
    return [j for j, t in jobs if t == m]

if __name__ == '__main__':
    jobs = [("job_a", 12), ("job_b", 5), ("job_c", 20), ("job_d", 7)]
    print(job_scheduler(jobs))
    print(job_scheduler_v2(jobs))
    print(fastest_jobs(jobs))
    
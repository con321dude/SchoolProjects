# helpful libraries: (thanks to the amazing TA) *cough* gimme good grade plz *cough*
# PS: You are actually a really cool and fun TA, (not just saying that cuz your the one grading this)... might be a little crazy at times cuz ur Colombian like me, but that just adds to the fun. Hopefully u read this and thx for all the help :)
import pandas as pd
import numpy as np


class Process:  # define class of process to be used
    def __init__(self, name, bursts):
        self.name = name
        self.bursts = bursts

        self.Ttr = 0  # turnaround time
        self.tCPU = 0  # total time
        self.Tw = 0  # waiting time
        self.tIO = 0  # time spent in IO
        self.Tr = 0  # response time
        self.mfqLoc = 1

        self.fReady = False  # flags to state which state the process is currently in
        self.fRunning = False
        self.fIO = False
        self.fVisited = False

        self.index = 0  # counter to see what place we are at, if even -> cpu burst, if odd -> io burst


def FCFS():  # First Come First Serve function
    # initialize all the processes with their values at the beginning of each function:
    p1 = Process("p1", [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4])
    p2 = Process("p2", [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8])
    p3 = Process("p3", [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6])
    p4 = Process("p4", [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3])
    p5 = Process("p5", [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4])
    p6 = Process("p6", [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8])
    p7 = Process("p7", [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10])
    p8 = Process("p8", [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6])

    processes = [p1, p2, p3, p4, p5, p6, p7, p8]  # list of all processes

    time = 0
    cpuTime = 0
    cpuUtilization = 0

    rQueue = []
    wQueue = []
    completedProcesses = 0
    time = 0
    cpuruntime = 0
    used = 0
    Ttravg = 0
    Travg = 0
    Twavg = 0
    tCPUavg = 0
    tIOavg = 0
    for p in processes:  # create ready queue with all processes
        rQueue.append(p)

    for p in processes:  # calculate total process completion time
        for count, burstTime in enumerate(p.bursts):  # looking at cpu bursts only
            if count % 2 == 0:
                p.tCPU += burstTime
                cpuTime += burstTime
            count += 1  # to get every other value

    # while not done with every process?
#     done if amount of completed processes == total amount of processes
    while completedProcesses < len(processes):

        if len(rQueue) > 0:  # when choosing next process to run,
            # first check ready queue... if empty then update waiting queue,
            # if waiting queue is empty, then exit

            # set current process to first process in the ready queue
            runningProcess = rQueue[0]
            rQueue.remove(rQueue[0])  # remove it from the ready queue because it is now running

            runningProcess.fVisited = True
            runningProcess.fReady = False
            runningProcess.fRunning = True
            # while still active on that burst
            while runningProcess.bursts[runningProcess.index] > 0:
                print("\nReady Queue at time:", time, " \n")
                for p in rQueue:  # decrease all ready q values and increase all ready process waiting times
                    p.Tw += 1
                    print(p.name, ":", p.bursts, "\n", "        Tw =", p.Tw)

                    if p.fVisited == False:
                        p.Tr += 1
                print("Currently Running: ", runningProcess.name, ":",
                      runningProcess.bursts, "time: ", time)  # output current running process

                # change current remaining burst time
                runningProcess.bursts[runningProcess.index] -= 1
                time += 1
                cpuruntime += 1

                if len(wQueue) > 0:  # if there are items in waiting queue:
                    print("Waiting Queue at time:", time, " \n")
                    for p in wQueue:  # decrease all waiting q values
                        print(p.name, ":", p.bursts, "\n")
                        p.bursts[p.index] -= 1
                        p.tIO += 1  # increase IO time of the process that is waiting
                        if p.bursts[p.index] == 0:  # if p is done waiting
                            p.index += 1  # change index of runningProcess

                            rQueue.append(p)  # move from waiting to ready (first add it to ready)
                            wQueue.remove(p)

            # done with this process: calculate the values at this time because this is when you finished p
            if runningProcess.index == len(runningProcess.bursts)-1:
                runningProcess.fRunning = False
                runningProcess.fTerminated = True
                completedProcesses += 1
                runningProcess.Ttr = time

            else:  # send to waiting
                runningProcess.index += 1
                runningProcess.fRunning = False
                runningProcess.fWaiting = True  # current process is now waiting
                wQueue.append(runningProcess)

        else:  # nothing in ready Queue
            if runningProcess.fRunning == False and len(rQueue) == 0:
                if len(wQueue) > 0 and len(rQueue) == 0:
                    while len(rQueue) == 0:
                        print("\nWaiting Queue at time:", time, " \n")
                        for p in wQueue:  # decrease all waiting q values
                            print(p.name, ":", p.bursts, "\n")
                            p.bursts[p.index] -= 1

                            if p.bursts[p.index] == 0:
                                p.index += 1  # change index of runningProcess
                                rQueue.append(p)
                                wQueue.remove(p)
                            print("Time ", time, wQueue)
                        time += 1

    print("FCFS Results:\n")
    for p in processes:
        print(p.name, "     Ttr =", p.Ttr, "        tCPU =", p.tCPU,
              "        Tw =", p.Tw, "        tIO =", p.tIO, "        Tr =", p.Tr)
        Ttravg = p.Ttr + Ttravg
        Twavg = p.Tw + Twavg
        tCPUavg = p.tCPU + tCPUavg
        tIOavg = p.tIO + tIOavg
        Travg = p.Tr + Travg

    Ttravg = Ttravg/len(processes)
    Twavg = Twavg/len(processes)
    tCPUavg = tCPUavg/len(processes)
    tIOavg = tIOavg/len(processes)
    Travg = Travg/len(processes)

    cpuUtilization = 100*(cpuruntime / time)
    print("\nAvg values:  Ttr avg:",  Ttravg, "     Tw avg:", Twavg,
          "     Tr avg:", Travg, "     tCPU avg:", tCPUavg, "     tIO avg:", tIOavg, "      cpuUtilization:", cpuUtilization, "%", "      cpuruntime:", cpuruntime, "      totalruntime:", time)


def sortReady(rQueue):
    lst = []
    ind = []
    for p in rQueue:
        lst.append(p.bursts[p.index])
        ind.append(p.name)
    sortedQ = pd.DataFrame(lst, index=ind, columns=['burst'])
    sortedQ = sortedQ.sort_values(['burst'])
    sortedQ = sortedQ.reset_index()
    print(sortedQ)
    treadQ = []
    indexc = 0
    for i in range(len(sortedQ)):
        for j in range(len(rQueue)):

            if sortedQ.iloc[i, 0] == rQueue[j].name:
                treadQ.append(rQueue[j])

    return(treadQ)


def SJF():  # First Come First Serve function with a sorting when something is added to ready queue

    p1 = Process("p1", [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4])
    p2 = Process("p2", [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8])
    p3 = Process("p3", [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6])
    p4 = Process("p4", [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3])
    p5 = Process("p5", [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4])
    p6 = Process("p6", [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8])
    p7 = Process("p7", [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10])
    p8 = Process("p8", [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6])

    processes = [p1, p2, p3, p4, p5, p6, p7, p8]  # list of all processes

    time = 0
    cpuTime = 0
    cpuUtilization = 0

    rQueue = []
    wQueue = []
    completedProcesses = 0
    time = 0
    cpuruntime = 0
    idle = 0
    used = 0
    Ttravg = 0
    Travg = 0
    Twavg = 0
    tCPUavg = 0
    tIOavg = 0
    for p in processes:  # create ready queue with all processes
        rQueue.append(p)

    for p in processes:  # calculate total process completion time
        for count, burstTime in enumerate(p.bursts):  # looking at cpu bursts only
            if count % 2 == 0:
                p.tCPU += burstTime
                cpuTime += burstTime
            count += 1  # to get every other value
    rQueue = sortReady(rQueue)

    while completedProcesses < len(processes):

        if len(rQueue) > 0:  # when choosing next process to run,
            # first check ready queue... if empty then update waiting queue,
            # if waiting queue is empty, then exit

            # set current process to first process in the ready queue
            rQueue = sortReady(rQueue)
            runningProcess = rQueue[0]
            rQueue.remove(rQueue[0])  # remove it from the ready queue because it is now running

            runningProcess.fVisited = True
            runningProcess.fReady = False
            runningProcess.fRunning = True
            # while still active on that burst
            while runningProcess.bursts[runningProcess.index] > 0:
                print("\nReady Queue at time:", time, " \n")
                for p in rQueue:  # decrease all ready q values and increase all ready process waiting times
                    p.Tw += 1
                    print(p.name, ":", p.bursts, "\n", "        Tw =", p.Tw)

                    if p.fVisited == False:
                        p.Tr += 1
                print("Currently Running: ", runningProcess.name, ":",
                      runningProcess.bursts, "time: ", time)  # output current running process

                # change current remaining burst time
                runningProcess.bursts[runningProcess.index] -= 1
                time += 1
                cpuruntime += 1
                if len(wQueue) > 0:  # if there are items in waiting queue:
                    print("Waiting Queue at time:", time, " \n")
                    for p in wQueue:  # decrease all waiting q values
                        print(p.name, ":", p.bursts, "\n")
                        p.bursts[p.index] -= 1
                        p.tIO += 1  # increase IO time of the process that is waiting
                        if p.bursts[p.index] == 0:  # if p is done waiting
                            p.index += 1  # change index of runningProcess

                            rQueue.append(p)  # move from waiting to ready (first add it to ready)
                            wQueue.remove(p)

            # done with this process: calculate the values at this time because this is when you finished p
            if runningProcess.index == len(runningProcess.bursts)-1:
                runningProcess.fRunning = False
                runningProcess.fTerminated = True
                completedProcesses += 1
                runningProcess.Ttr = time
                # runningProcess.Tw = runningProcess.Ttr - runningProcess.tCPU - runningProcess.tIO

            else:  # send to waiting
                runningProcess.index += 1
                runningProcess.fRunning = False
                runningProcess.fWaiting = True  # current process is now waiting
                wQueue.append(runningProcess)

        else:  # nothing in ready Queue
            if runningProcess.fRunning == False and len(rQueue) == 0:
                if len(wQueue) > 0 and len(rQueue) == 0:
                    while len(rQueue) == 0:
                        print("\nWaiting Queue at time:", time, " \n")
                        for p in wQueue:  # decrease all waiting q values
                            print(p.name, ":", p.bursts, "\n")
                            p.bursts[p.index] -= 1

                            if p.bursts[p.index] == 0:
                                p.index += 1  # change index of runningProcess
                                rQueue.append(p)
                                wQueue.remove(p)
                            print("Time ", time, wQueue)
                        time += 1

    print("SJF Results:\n")
    for p in processes:
        print(p.name, "     Ttr =", p.Ttr, "        tCPU =", p.tCPU,
              "        Tw =", p.Tw, "        tIO =", p.tIO, "        Tr =", p.Tr)
        Ttravg = p.Ttr + Ttravg
        Twavg = p.Tw + Twavg
        tCPUavg = p.tCPU + tCPUavg
        tIOavg = p.tIO + tIOavg
        Travg = p.Tr + Travg

    Ttravg = Ttravg/len(processes)
    Twavg = Twavg/len(processes)
    tCPUavg = tCPUavg/len(processes)
    tIOavg = tIOavg/len(processes)
    Travg = Travg/len(processes)

    cpuUtilization = 100*(cpuruntime) / time
    print("\nAvg values:  Ttr avg:",  Ttravg, "     Tw avg:", Twavg,
          "     Tr avg:", Travg, "     tCPU avg:", tCPUavg, "     tIO avg:", tIOavg, "      cpuUtilization:", cpuUtilization, "%", "      cpuruntime:", cpuruntime, "      totalruntime:", time)


def MFQ():  # MFQ function

    p1 = Process("p1", [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4])
    p2 = Process("p2", [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8])
    p3 = Process("p3", [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6])
    p4 = Process("p4", [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3])
    p5 = Process("p5", [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4])
    p6 = Process("p6", [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8])
    p7 = Process("p7", [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10])
    p8 = Process("p8", [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6])

    processes = [p1, p2, p3, p4, p5, p6, p7, p8]  # list of all processes

    time = 0
    cpuTime = 0
    cpuUtilization = 0

    rQueue = []
    wQueue = []
    completedProcesses = 0
    time = 0
    cpuruntime = 0
    idle = 0
    used = 0
    Ttravg = 0
    Travg = 0
    Twavg = 0
    tCPUavg = 0
    tIOavg = 0
    tq = 5

    for p in processes:  # create ready queue with all processes
        rQueue.append(p)

    for p in processes:  # calculate total process completion time
        for count, burstTime in enumerate(p.bursts):  # looking at cpu bursts only
            if count % 2 == 0:
                p.tCPU += burstTime
                cpuTime += burstTime
            count += 1  # to get every other value

    # while not done with every process?
#     done if amount of completed processes == total amount of processes
    while completedProcesses < len(processes):

        if len(rQueue) > 0:  # when choosing next process to run,
            # first check ready queue... if empty then update waiting queue,
            # if waiting queue is empty, then exit

            # set current process to first process in the ready queue
            runningProcess = rQueue[0]
            rQueue.remove(rQueue[0])  # remove it from the ready queue because it is now running

            runningProcess.fVisited = True
            runningProcess.fReady = False
            runningProcess.fRunning = True
            # runningProcess.mfqLoc = 1

            if runningProcess.mfqLoc == 1:  # first Queue
                tq = 5
            elif runningProcess.mfqLoc == 2:  # second queue
                tq = 10
            elif runningProcess.mfqLoc > 2:  # third queue
                tq = 100
            # while still active on that burst

            y = min(tq, runningProcess.bursts[runningProcess.index])

            for i in range(y):  # run the amount of times

                print("\nReady Queue at time:", time, " \n")
                for p in rQueue:  # decrease all ready q values and increase all ready process waiting times
                    p.Tw += 1
                    print(p.name, ":", p.bursts, "\n", "        Tw =", p.Tw)

                    if p.fVisited == False:
                        p.Tr += 1

                if len(wQueue) > 0:  # if there are items in waiting queue output waiting queue
                    print("\nWaiting Queue at time:", time, " \n")
                    for p in wQueue:  # decrease all waiting q values
                        print(p.name, ":", p.bursts, "\n")
                        p.bursts[p.index] -= 1

                        p.tIO += 1  # increase IO time of the process that is waiting
                        if p.bursts[p.index] == 0:  # if p is done waiting
                            p.index += 1  # change index of waiting queue Process
                            # move from waiting to ready (first add it to ready)
                            rQueue.append(p)
                            wQueue.remove(p)

                print("\nCurrently Running: ", runningProcess.name, ":",
                      runningProcess.bursts, "time: ", time, "  This process is in queue:", runningProcess.mfqLoc)  # output current running process

                # change current remaining burst time
                runningProcess.bursts[runningProcess.index] -= 1
                time += 1
                cpuruntime += 1

                tq -= 1

                runningProcess.mfqLoc += 1
                tq = 0

            # done with this process: calculate the values at this time because this is when you finished p
            if runningProcess.index == len(runningProcess.bursts)-1:
                runningProcess.fRunning = False
                runningProcess.fTerminated = True
                completedProcesses += 1
                runningProcess.Ttr = time
                # runningProcess.Tw = runningProcess.Ttr - runningProcess.tCPU - runningProcess.tIO

            elif runningProcess.bursts[runningProcess.index] == 0:  # Done with it, send to waiting
                runningProcess.index += 1  # look at IO burst instead of cpu
                runningProcess.fRunning = False
                runningProcess.fWaiting = True  # current process is now waiting
                runningProcess.mfqLoc = 1
                wQueue.append(runningProcess)
            else:  # not done yet, send back to ready...
                runningProcess.fRunning = False
                runningProcess.fReady = True
                rQueue.append(runningProcess)

        else:  # nothing in ready Queue
            if runningProcess.fRunning == False and len(rQueue) == 0:
                if len(wQueue) > 0 and len(rQueue) == 0:
                    while len(rQueue) == 0:
                        print("\nWaiting Queue at time:", time, " \n")
                        for p in wQueue:  # decrease all waiting q values
                            print(p.name, ":", p.bursts, "\n")
                            p.bursts[p.index] -= 1

                            if p.bursts[p.index] == 0:
                                p.index += 1  # change index of runningProcess
                                rQueue.append(p)
                                wQueue.remove(p)
                            print("Time ", time, wQueue)
                        time += 1

    print("MFQ:\n")
    for p in processes:
        print(p.name, "     Ttr =", p.Ttr, "        tCPU =", p.tCPU,
              "        Tw =", p.Tw, "        tIO =", p.tIO, "        Tr =", p.Tr)
        Ttravg = p.Ttr + Ttravg
        Twavg = p.Tw + Twavg
        tCPUavg = p.tCPU + tCPUavg
        tIOavg = p.tIO + tIOavg
        Travg = p.Tr + Travg

    Ttravg = Ttravg/len(processes)
    Twavg = Twavg/len(processes)
    tCPUavg = tCPUavg/len(processes)
    tIOavg = tIOavg/len(processes)
    Travg = Travg/len(processes)

    cpuUtilization = 100*cpuruntime / time

    print("\nAvg values:  Ttr avg:",  Ttravg, "     Tw avg:", Twavg,
          "     Tr avg:", Travg, "     tCPU avg:", tCPUavg, "     tIO avg:", tIOavg, "      cpuUtilization:", cpuUtilization, "%", "      cpuruntime:", cpuruntime, "      totalruntime:", time)


def sortReady(rQueue):
    lst = []
    ind = []
    for p in rQueue:  # sort ready queue based on their current burst values... using a temp panda DataFrame
        lst.append(p.bursts[p.index])
        ind.append(p.name)
    sortedQ = pd.DataFrame(lst, index=ind, columns=['burst'])
    sortedQ = sortedQ.sort_values(['burst'])
    sortedQ = sortedQ.reset_index()
    print(sortedQ)
    treadQ = []
    indexc = 0
    for i in range(len(sortedQ)):
        for j in range(len(rQueue)):
            if sortedQ.iloc[i, 0] == rQueue[j].name:
                treadQ.append(rQueue[j])
    return(treadQ)


print(" What do you want to run? \n")
runagain = 0
x = 0


def runprocesses(runagain, x):
    if runagain == 0:
        x = int(input("1. FCFS      2. SJF      3. MFQ     4. Exit\n"))
        if x == 1:
            FCFS()
        if x == 2:
            SJF()
        if x == 3:
            MFQ()
        elif x == 4:
            runagain += 1
        runprocesses(runagain, x)
    else:
        return


runprocesses(runagain, x)

#This algorithm only works for pipe networks identical with the shape of the one in example 2.11.
#Any one of the K and Q values can be changed as needed.
#Negative Q values at the corners mean water is exiting the system at the point.
#Positive Q values at the corners mean water is entering the system at the point.
#You can enter the Q and K values from the console after executing the code, or if you prefer set the values from the source code.

#Variable that tells the algorithm when to stop, if the correction is smaller than this value in both loops.
#You can manually set this value to your liking.
StopWhen = 0.1

#Defining the correction variables.
#They can be initialized to anything larger than StopWhen
CorrectionValue1 = 255
CorrectionValue2 = 255

#Variables to keep track of which corner or pipe the input is for.
CornerInput = 0
PipeInput = 0
CornerA = 0
CornerB = 0
CornerC = 0
CornerD = 0

while CornerInput < 4:

    if CornerInput == 0:
        try:
            CornerA = int(input("Enter flow at point A: "))
            CornerInput = CornerInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    elif CornerInput == 1:
        try:
            CornerB = int(input("Enter flow at point B: "))
            CornerInput = CornerInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    elif CornerInput == 2:
        try:
            CornerC = int(input("Enter flow at point C: "))
            CornerInput = CornerInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    else:
        try:
            CornerD = int(input("Enter flow at point D: "))
            CornerInput = CornerInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    #Check to see if continuity is satisfied.
    if (CornerA + CornerB + CornerC + CornerD != 0) and (CornerInput >= 4):
        print("Continuity is not satisfied.")
        CornerInput = 0

while PipeInput < 5:
    if PipeInput == 0:
        try:
            KPipeAB = int(input("Enter K value for pipe AB: "))
            PipeInput = PipeInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    elif PipeInput == 1:
        try:
            KPipeBC = int(input("Enter K value for pipe BC: "))
            PipeInput = PipeInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    elif PipeInput == 2:
        try:
            KPipeAC = int(input("Enter K value for pipe AC: "))
            PipeInput = PipeInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    elif PipeInput == 3:
        try:
            KPipeCD = int(input("Enter K value for pipe CD: "))
            PipeInput = PipeInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

    else:
        try:
            KPipeAD = int(input("Enter K value for pipe AD: "))
            PipeInput = PipeInput + 1
        except ValueError:
            print("Invalid input. Please enter a number: ")

#Creating lists and defining variables.
CornerFlowList = [CornerA, CornerB, CornerC, CornerD]
KList = [KPipeAB, KPipeBC, KPipeAC, KPipeCD, KPipeAD]
PipeAB = 0
PipeBC = 0
PipeAC = 0
PipeCD = 0
PipeAD = 0
PipeFlowList = [PipeAB, PipeBC, PipeAC, PipeCD, PipeAD]

#This variable tells the code for which loop the flow in AC is clockwise, or positive.
ClockwiseFlowAC = 0

#My algorithm first starts by selecting a corner with inflow, which has an outflow corner on its diagonal.
#For example, if we were to select B, then we would have to check if D is an outflow.
#This is because I designed it to first distribute the inflow to its neighbours, and then the flow reaches the last corner.
#Therefore, if I didn't add this check, and the only outflow corner was a neighbour to the selected inflow corner, the algorithm would fail.
#If the inflows are not aligned with an outflow at all, the first loop fails, and I save this to a variable.
#This is because I will have to use a different algorithm to assume flow in the pipes.
StartIndex = 0
FirstLoopFailed = False
for corner in CornerFlowList:
    if StartIndex == 2:
        FirstLoopFailed = True
        break
    if (CornerFlowList[StartIndex] * CornerFlowList[StartIndex + 2] < 0):
        if CornerFlowList[StartIndex] > 0:
            break
        else:
            StartIndex = StartIndex + 2
            break
    else:    
        StartIndex = StartIndex + 1

#To summarize, this algorithm picks the first inflow corner saved in the cornerflowlist.
#Then it checks if there is a neighbouring outflow corner that has a lesser absolute value than the initial corner.
#If so, it sends the minimum required flow there, and then sends the rest directly towards the other outflow corner, from both inflow corners.
#Otherwise, it sends the entirety of the flow in the initial corner, to an outflow corner, and then distributes the other inflow corner's flow as needed.
if (StartIndex == 2) and FirstLoopFailed:
    StartIndex = 0
    if CornerFlowList[StartIndex] > 0:

        if CornerA > abs(CornerB):
            CornerA = CornerA + CornerB
            PipeAB = abs(CornerB)
            PipeAD = -1 * CornerA
            CornerD = CornerD + CornerA
            CornerA = 0
            PipeCD = abs(CornerD)
            CornerC = CornerC + CornerD

        elif CornerA > abs(CornerD):
            CornerA = CornerD + CornerA
            PipeAD = CornerD
            PipeAB = CornerA
            CornerB = CornerB + CornerA
            PipeBC = CornerB
            CornerC = CornerC + CornerB

        else:
            PipeAB = CornerA
            CornerB = CornerB + CornerA
            PipeBC = CornerB
            PipeCD = -1 * CornerD


    elif CornerB > 0:

        if CornerB > abs(CornerA):
            CornerB = CornerB + CornerA
            PipeAB = CornerA
            PipeBC = CornerB
            PipeCD = -1 * CornerD

        elif CornerB > abs(CornerC):
            CornerB = CornerB + CornerC
            PipeBC = -1 * CornerC
            PipeAB = -1 * CornerB
            PipeAD = CornerD

        else:
            PipeBC = -1 * CornerB
            CornerA = CornerA + CornerB
            PipeAD = -1 * CornerA
            PipeCD = CornerC

#Set as an impossible number so the next check definitely fails, as the assumption has been made already.
    StartIndex = 9

#After selecting a starting point, the code diverges for every possible starting index, while assuming flows.
#Negative flow for a pipe means it is going counter-clockwise in its cycle.
#Positive flow for a pipe means it is going clockwise in its cycle.
#For starting points B and D, the algorithm checks if the neighbouring corners are both inflows.
#If they are inflows, it splits the flow equally between them. 
#Following this step, the neighbour corner with the greater flow value will push half of it through the diagonal pipe, and the other half to the outflow corner.
#The neighbouring corner that recieved the flow from the diagonal pipe will push forward all of its flow to the outflow corner.
#If one, or both, neighbouring corners are outflow corners, the algorithm will pick one outflow corner to provide minimum flow required.
#It will push forward the rest of the flow into the other neighbouring corner.
#The corner that recieved the larger flow, will push half of the flow it has left through the diagonal, and the other half directly to the final outflow corner.
#The corner that recieved the minimum flow, will only push forward the flow it recieved through the diagonal pipe.
if StartIndex == 1:

    if (CornerA >= 0) and (CornerC >= 0):
        PipeAB = -1 * (CornerB / 2)
        PipeBC = (CornerB / 2)
        CornerA = CornerA + (CornerB / 2)
        CornerC = CornerC + (CornerB / 2)

        if CornerA > CornerC:
            PipeAC = CornerA / 2
            ClockwiseFlowAC = 1
            PipeAD = -1 * (CornerA / 2)
            PipeCD = CornerC + (CornerA / 2)

        elif CornerA < CornerC:
            PipeAC = CornerC / 2
            ClockwiseFlowAC = 2
            PipeAD = -1 * (CornerA + (CornerC / 2))
            PipeCD = CornerC / 2

        else:
            PipeAD = -1 * (CornerA)
            PipeCD = CornerC

    elif (abs(CornerA) < abs(CornerC)):
        PipeAB = CornerA
        PipeBC = CornerB + CornerA
        CornerA = 0
        CornerC = CornerC + PipeBC

        PipeAC = CornerC / 2
        ClockwiseFlowAC = 2
        PipeAD = -1 * (CornerC / 2)
        PipeCD = CornerC / 2

    elif (abs(CornerC) < abs(CornerA)):
        PipeBC = -1 * CornerC
        PipeAB = -1 * (CornerB + CornerC)
        CornerA = CornerA + CornerB + CornerC
        CornerC = 0

        PipeAC = CornerA / 2
        ClockwiseFlowAC = 1
        PipeAD = -1 * (CornerA / 2)
        PipeCD = CornerA / 2

elif StartIndex == 3:

    if (CornerA >= 0) and (CornerC >= 0):
        PipeAD = CornerD / 2
        PipeCD = -1 * (CornerD / 2)
        CornerA = CornerA + (CornerD / 2)
        CornerC = CornerC + (CornerD / 2)

        if CornerA > CornerC:
            PipeAC = CornerA / 2
            ClockwiseFlowAC = 1
            PipeAB = CornerA/2
            PipeBC = -1 * (CornerC + (CornerA / 2))

        elif CornerA < CornerC:
            PipeAC = CornerC / 2
            ClockwiseFlowAC = 2
            PipeAB = CornerA + (CornerC / 2)
            PipeBC = -1 * (CornerC / 2)

        else:
            PipeAB = CornerA
            PipeBC = -1 * CornerC

    elif (abs(CornerA) < abs(CornerC)):
        PipeAD = -1 * CornerA
        CornerD = CornerD + CornerA
        PipeCD = -1 * CornerD 

        CornerC = CornerD + CornerC
        PipeAC = CornerC / 2
        ClockwiseFlowAC = 2
        PipeBC = -1 * (CornerC / 2) 
        PipeAB = (CornerC / 2)

    elif abs(CornerC) < abs(CornerA):
        PipeCD = CornerC
        CornerD = CornerD + CornerC
        PipeAD = CornerD

        CornerA = CornerA + CornerD
        PipeAC = CornerA / 2
        ClockwiseFlowAC = 1
        PipeAB = CornerA / 2
        PipeBC = -1 * (CornerA / 2)

elif StartIndex == 0:

    if (CornerB >= 0) and (CornerD >= 0):
        PipeBC = CornerB
        PipeAC = CornerA
        ClockwiseFlowAC = 1
        PipeCD = -1 * CornerD

    elif(CornerB * CornerD < 0) and (CornerB >= 0):
        PipeAD = -1 * CornerA
        CornerD = CornerD + CornerA
        PipeCD = CornerD * -1
        PipeBC = CornerB

    elif (CornerB * CornerD < 0) and (CornerD >= 0):
        PipeAB = CornerA
        CornerB = CornerB + CornerA 
        PipeCD = -1 * CornerD 
        PipeBC = CornerB

    else:
        PipeAB = abs(CornerB)
        PipeAC = abs(CornerC)
        ClockwiseFlowAC = 1
        PipeAD = CornerD

elif StartIndex == 2:

    if (CornerB >= 0) and (CornerD >= 0):
        PipeAB = -1 * CornerB
        PipeAC = CornerC
        ClockwiseFlowAC = 2
        PipeAD = CornerD

    elif(CornerB * CornerD < 0) and (CornerB >= 0):

        CornerD = CornerD + CornerC
        PipeCD = CornerC
        PipeAB = -1 * CornerB
        PipeAD = CornerD

    elif (CornerB * CornerD < 0) and (CornerD >= 0):
        PipeBC = -1 * CornerC 
        CornerB = CornerB + CornerC
        PipeAB = -1 * CornerB
        PipeAD = CornerD

    else:
        PipeBC = CornerB
        PipeAC = abs(CornerA)
        ClockwiseFlowAC = 2
        PipeCD = abs(CornerD)

#Assumed flow in pipes
print("Pipe AB assumption: " + str(PipeAB))
print("Pipe BC assumption: " + str(PipeBC))
print("Pipe AC assumption: " + str(PipeAC))
print("Pipe AC is positive for loop " + str(ClockwiseFlowAC))
print("Pipe CD assumption: " + str(PipeCD))
print("Pipe AD assumption: " + str(PipeAD))

while (abs(CorrectionValue1) > StopWhen) and (abs(CorrectionValue2) > StopWhen):

    if ClockwiseFlowAC == 1:
        CorrectionValue1 = -1 * (KPipeAD * PipeAD * abs(PipeAD) + KPipeCD * PipeCD * abs(PipeCD) + KPipeAC * PipeAC * PipeAC) / (2 * KPipeAD * abs(PipeAD) + 2 * KPipeCD * abs(PipeCD) + 2 *KPipeAC * PipeAC)

        CorrectionValue2 = -1 * (KPipeAB * PipeAB * abs(PipeAB) + KPipeBC * PipeBX * abs(PipeBC) - KPipeAC * PipeAC * PipeAC) / (2 * KPipeAB * abs(PipeAB) + 2 * KPipeBC * abs(PipeBC) + 2 *KPipeAC * PipeAC)

        PipeAD = PipeAD + CorrectionValue1 
        PipeCD = PipeCD + CorrectionValue1 
        PipeAC = PipeAC + CorrectionValue1- CorrectionValue2 
        PipeAB = PipeAB + CorrectionValue2 
        PipeBC = PipeBC + CorrectionValue2 


    if ClockwiseFlowAC == 2:
        CorrectionValue1 = -1 * (KPipeAD * PipeAD * abs(PipeAD) + KPipeCD * PipeCD * abs(PipeCD) - KPipeAC * PipeAC * PipeAC) / (2 * KPipeAD * abs(PipeAD) + 2 * KPipeCD * abs(PipeCD) + 2 *KPipeAC * PipeAC)

        CorrectionValue2 =-1 * (KPipeAB * PipeAB * abs(PipeAB) + KPipeBC * PipeBC * abs(PipeBC) + KPipeAC * PipeAC * PipeAC) / (2 * KPipeAB * abs(PipeAB) + 2 * KPipeBC * abs(PipeBC) + 2 *KPipeAC * PipeAC)

        PipeAD = PipeAD + CorrectionValue1 
        PipeCD = PipeCD + CorrectionValue1 
        PipeAC = PipeAC - CorrectionValue1 + CorrectionValue2 
        PipeAB = PipeAB + CorrectionValue2 
        PipeBC = PipeBC + CorrectionValue2

    print(CorrectionValue1)
    print(CorrectionValue2)
print("Pipe AB assumption: " + str(PipeAB))
print("Pipe BC assumption: " + str(PipeBC))
print("Pipe AC assumption: " + str(PipeAC))
print("Pipe AC is positive for loop " + str(ClockwiseFlowAC))
print("Pipe CD assumption: " + str(PipeCD))
print("Pipe AD assumption: " + str(PipeAD))
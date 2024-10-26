# This algorithm only works for pipe networks identical with the shape of the one in example 2.11.
# Any one of the K and Q values can be changed as needed.
# Negative Q values at the corners mean water is exiting the system at the point.
# Positive Q values at the corners mean water is entering the system at the point.
# You can enter the Q and K values from the console after executing the code, or if you prefer set the values from the source code.

# Variable that tells the algorithm when to stop, if the correction is smaller than this value in both loops.
# You can manually set this value to your liking.
StopWhen = 0.1

# Variable that limits the amount of times new correction values can be calculated. 
# 10 is enough since even in tens of thousands of unique conditions, about 4% needs more iterations.
iteration_limit = 10

# Defining the correction variables.
# They can be initialized to anything larger than StopWhen.
# Other than that their initial values are arbitrary.
CorrectionValue1 = 255
CorrectionValue2 = 255

# Variables to keep track of which corner or pipe the input is for.
CornerInput = 0
PipeInput = 0
CornerA = 0
CornerB = 0
CornerC = 0
CornerD = 0

# Corner Input Loop.
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

    # Check to see if continuity is satisfied.
    if (CornerA + CornerB + CornerC + CornerD != 0) and (CornerInput >= 4):
        print("Continuity is not satisfied.")
        CornerInput = 0

# Pipe Input Loop.
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

# Creating lists and defining variables.
CornerFlowList = [CornerA, CornerB, CornerC, CornerD]
PipeAB = 0
PipeBC = 0
PipeAC = 0
PipeCD = 0
PipeAD = 0

# This variable tells the code for which loop's clockwise direction AC is positive.
ClockwiseFlowAC = 0

# My algorithm first searches the input for 2 corners with 0 flow.
# This is because my main algorithm can cause zero division errors, since one loop can contain completely 0 flow pipes.
# To avoid this, I check for the two zero case, and if its true, I direct the input to a seperate algorithm I made for this specific condition.
StartIndex = 0
FirstLoopFailed = False
ZeroCounter = 0

for corner in CornerFlowList:
    if corner == 0:
        ZeroCounter = ZeroCounter + 1

if ZeroCounter < 2:

    # I assume that there is a "main" inflow corner, and a "main" outflow corner.
    # With this assumption, I come to the conclusion that there is only two types of systems.
    # One where the main inflow corner and the main outflow corner, are on the opposite diagonal ends, which I'll refer to as type 1.
    # The other one being that the main inflow and main outflow corners are neighbours, which I'll refer to as type 2.
    # I check to see which type it is by going through CornerFlowList.
    # If the flow is type 1, then either in the first or second index, their multiplication with the corner on the diagonal will give a negative integer.
    # If the flow is type 2 however, the loop will move on the the third corner, index 2, in which case we can say that the check for type 1 failed, and it is type 2.
    # I check the type like this, because I will write different if else statements for the types.
    for corner in CornerFlowList:

        # The flow is type 2.
        if StartIndex == 2:
            FirstLoopFailed = True
            break
        
        # The flow is type 1.
        if (CornerFlowList[StartIndex] * CornerFlowList[StartIndex + 2] < 0):
            
            # If this is true, the main inflow corner is on the top of the diagonal.
            if CornerFlowList[StartIndex] > 0:
                break
            
            # Else, the main inflow corner is on the bottom of the diagonal.
            else:
                StartIndex = StartIndex + 2
                break

        else:    
            StartIndex = StartIndex + 1

    # Starting the algorithm for type 2 flow.
    if FirstLoopFailed:

        # If Corner A is the main inflow.
        if CornerA >= 0:
            PipeAB = CornerA / 2
            PipeAD = -1 * (CornerA / 2)
            PipeCD = CornerC / 2
            PipeBC = -1 * (CornerC / 2)
            CornerB = CornerB + (CornerA / 2) + (CornerC / 2)
            CornerD = CornerD + (CornerA / 2) + (CornerC / 2)

            if CornerB > CornerD:
                PipeBC = PipeBC + CornerB
                PipeCD = PipeCD + CornerB
            
            elif CornerB < CornerD:
                PipeAD = PipeAD + CornerD
                PipeAB = PipeAB + CornerD
                
                
        # If Corner B is the main inflow.
        elif CornerB >= 0:

            PipeAB = -1 * (CornerB / 2)
            PipeBC = CornerB / 2
            PipeAD = CornerD / 2
            PipeCD = -1 * (CornerD / 2)
            CornerA = CornerA + (CornerB / 2) + (CornerD / 2)
            CornerC = CornerC + (CornerB / 2) + (CornerD / 2)

            if CornerC > CornerA:
                PipeAC = CornerC
                ClockwiseFlowAC = 2

            elif CornerC < CornerA:
                PipeAC = CornerA
                ClockwiseFlowAC = 1

            elif CornerC == 0:
                PipeAC = 1
                ClockwiseFlowAC = 1
                PipeBC = PipeBC - 1
                PipeAB = PipeAB - 1

        # Setting StartIndex to an impossible value, so the following code doesn't execute.
        StartIndex = 9

        
    # Corner B is the main inflow corner.
    if StartIndex == 1:

        # Neighbouring corners of the main inflow corner are non-negative.
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

        # The neighbouring corners of the main inflow corner could be negative.   
        else:
            PipeAB = -1 * (CornerB / 2)
            CornerA = CornerA + (CornerB / 2)
            PipeBC = CornerB / 2
            CornerC = CornerC + (CornerB / 2)

            if (CornerA > 0) and (CornerC <= 0):

                if CornerC < 0:
                    PipeAC = abs(CornerC)
                    ClockwiseFlowAC = 1
                    CornerA = CornerA + CornerC
                    PipeAD = -1 * CornerA

                elif CornerC == 0:
                    PipeAC = CornerA / 2
                    ClockwiseFlowAC = 1
                    PipeAD = -1* (CornerA / 2)
                    PipeCD = CornerA / 2

            elif (CornerA <= 0) and (CornerC > 0):
                
                if CornerA < 0:
                    PipeAC = abs(CornerA)
                    ClockwiseFlowAC = 2
                    CornerC = CornerC + CornerA
                    PipeCD = CornerC

                elif CornerA == 0:
                    PipeAC = CornerC / 2
                    ClockwiseFlowAC = 2
                    PipeAD = -1 * (CornerC / 2)
                    PipeCD = CornerC / 2
            
            elif (CornerA > 0) and (CornerC > 0):

                if CornerA > CornerC:
                    PipeAC = CornerA/2
                    ClockwiseFlowAC = 1
                    CornerC = CornerC + (CornerA / 2)
                    PipeAD = -1*(CornerA/2)
                    PipeCD = CornerC
                
                elif CornerA < CornerC:
                    PipeAC = CornerC/2
                    ClockwiseFlowAC = 2
                    CornerA = CornerA + (CornerC/2)
                    PipeCD = CornerC / 2
                    PipeAD = -1 * CornerA
                
                elif CornerA == CornerC:
                    PipeCD = CornerC
                    PipeAD = -1*CornerA

    # Corner D is the main inflow corner.
    elif StartIndex == 3:

        # Neighbouring corners of the main inflow corner are non-negative.
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

        # The neighbouring corners of the main inflow corner could be negative.   
        else:
            PipeAD = CornerD / 2
            PipeCD = -1 * (CornerD / 2)
            CornerA = CornerA + (CornerD / 2)
            CornerC = CornerC + (CornerD / 2)

            if (CornerA > 0) and (CornerC <= 0):

                if CornerC < 0:
                    PipeAC = abs(CornerC)
                    ClockwiseFlowAC = 1
                    CornerA = CornerA + CornerC
                    PipeAB = CornerA

                elif CornerC == 0:
                    PipeAC = CornerA / 2
                    ClockwiseFlowAC = 1
                    PipeAB = CornerA / 2
                    PipeBC = -1*(CornerA)
            
            elif (CornerA <= 0) and (CornerC > 0):

                if CornerA < 0:
                    PipeAC = abs(CornerA)
                    ClockwiseFlowAC = 2
                    CornerC = CornerC + CornerA
                    PipeBC = -1 * CornerC
                
                elif CornerA == 0:
                    PipeAC = CornerC / 2
                    ClockwiseFlowAC = 2
                    PipeAB = CornerC / 2
                    PipeBC = -1*(CornerC / 2)

            elif (CornerA > 0) and (CornerC > 0):
            
                if CornerA > CornerC:
                    PipeAC = CornerA / 2
                    ClockwiseFlowAC = 1
                    CornerC = CornerC + (CornerA / 2)
                    PipeAB = CornerA / 2
                    PipeBC = -1 * CornerC
                
                elif CornerA < CornerC:
                    PipeAC = CornerC / 2
                    ClockwiseFlowAC = 2
                    CornerA = CornerA + (CornerC/2)
                    PipeBC = -1*(CornerC/2)
                    PipeAB = CornerA
                
                elif CornerA == CornerC:
                    PipeAB = CornerA
                    PipeBC = -1*CornerC

    # Corner A is the main inflow corner.
    elif StartIndex == 0:
        PipeAB = CornerA / 3
        PipeAC = CornerA / 3
        ClockwiseFlowAC = 1
        PipeAD = -1 * (CornerA / 3)
        CornerB = CornerB + (CornerA/3)
        CornerC = CornerC + (CornerA/3)
        CornerD = CornerD + (CornerA/3)

        # Neighbouring corners of the main inflow corner are non-negative.
        if (CornerB >= 0) and (CornerD >= 0):
            PipeBC = CornerB
            PipeCD = -1 * CornerD

        # The neighbouring corners of the main inflow corner could be negative.   
        elif(CornerB * CornerD < 0) and (CornerB >= 0):
            PipeBC = CornerB
            CornerC = CornerC + CornerB
            PipeCD = CornerC

        elif (CornerB * CornerD < 0) and (CornerD >= 0):
            PipeCD = -1 * CornerD
            CornerC = CornerC + CornerD
            PipeBC = -1 * CornerC

    # Corner C is the main inflow corner.
    elif StartIndex == 2:
        PipeBC = -1 * (CornerC / 3)
        PipeAC = CornerC/3
        ClockwiseFlowAC = 2
        PipeCD = CornerC / 3
        CornerA = CornerA + (CornerC /3)
        CornerB = CornerB + (CornerC/3)
        CornerD = CornerD + (CornerC/3)

        # Neighbouring corners of the main inflow corner are non-negative.
        if (CornerB >= 0) and (CornerD >= 0):
            PipeAB = -1 * CornerB
            PipeAD = CornerD

        # The neighbouring corners of the main inflow corner could be negative.   
        elif(CornerB * CornerD < 0) and (CornerB >= 0):
            PipeAB = -1 * CornerB
            CornerA = CornerA + CornerB
            PipeAD = -1 * CornerA

        elif (CornerB * CornerD < 0) and (CornerD >= 0):
            PipeAD = CornerD
            CornerA = CornerA + CornerD
            PipeAB = CornerA

# There are two zero corners in the system.
else:
    if CornerA > 0:

        if CornerB < 0:
            PipeAC = CornerA
            ClockwiseFlowAC = 1
            PipeBC = CornerB

        elif CornerC < 0:
            PipeAC = CornerA 
            ClockwiseFlowAC = 1
        
        else:
            PipeAC = CornerA
            ClockwiseFlowAC = 1
            PipeCD = CornerA
    
    elif CornerB > 0:

        if CornerA < 0:
            PipeBC = CornerB
            PipeAC = CornerB
            ClockwiseFlowAC = 2
        
        elif CornerC < 0:
            PipeAB = CornerC 
            PipeAC = CornerB
            ClockwiseFlowAC = 1
        
        else:
            PipeAB = CornerD
            PipeAD = CornerD

    elif CornerC > 0:

        if CornerA < 0:
            PipeAC = CornerC
            ClockwiseFlowAC = 2
        
        elif CornerB < 0:
            PipeAC = CornerC
            ClockwiseFlowAC = 2
            PipeAB = CornerC

        else:
            PipeAC = CornerC
            ClockwiseFlowAC = 2
            PipeAD = CornerD

    else:

        if CornerA < 0:
            PipeCD = CornerA
            PipeAC = CornerD
            ClockwiseFlowAC = 2

        elif CornerB < 0:
            PipeAD = CornerD
            PipeAB = CornerD
        
        else:
            PipeAD = CornerD
            PipeAC = CornerD
            ClockwiseFlowAC = 1

# Assumed flow in pipes.
print("Pipe AB assumption: " + str(PipeAB))
print("Pipe BC assumption: " + str(PipeBC))
print("Pipe AC assumption: " + str(PipeAC))
print("Pipe AC is positive for loop " + str(ClockwiseFlowAC))
print("Pipe CD assumption: " + str(PipeCD))
print("Pipe AD assumption: " + str(PipeAD))

# Initialize the iteration counter.
iteration_counter = 0

# Calculate correction values until both values are smaller than the set tolerance.
while (abs(CorrectionValue1) > StopWhen) and (abs(CorrectionValue2) > StopWhen):

    # Stop if iteration limit is reached.
    if iteration_counter == iteration_limit:
        break

    # Correction value formula and addition, if the sign of the flow in AC is set according to loop 1.
    if ClockwiseFlowAC == 1:
        CorrectionValue1 = -1 * (KPipeAD * PipeAD * abs(PipeAD) + KPipeCD * PipeCD * abs(PipeCD) + KPipeAC * PipeAC * PipeAC) / (2 * KPipeAD * abs(PipeAD) + 2 * KPipeCD * abs(PipeCD) + 2 *KPipeAC * PipeAC)

        CorrectionValue2 = -1 * (KPipeAB * PipeAB * abs(PipeAB) + KPipeBC * PipeBC * abs(PipeBC) - KPipeAC * PipeAC * PipeAC) / (2 * KPipeAB * abs(PipeAB) + 2 * KPipeBC * abs(PipeBC) + 2 *KPipeAC * PipeAC)

        PipeAD = PipeAD + CorrectionValue1 
        PipeCD = PipeCD + CorrectionValue1 
        PipeAC = PipeAC + CorrectionValue1- CorrectionValue2 
        PipeAB = PipeAB + CorrectionValue2 
        PipeBC = PipeBC + CorrectionValue2 

    # Correction value formula and addition, if the sign of the flow in AC is set according to loop 2.
    elif ClockwiseFlowAC == 2:
        CorrectionValue1 = -1 * (KPipeAD * PipeAD * abs(PipeAD) + KPipeCD * PipeCD * abs(PipeCD) - KPipeAC * PipeAC * PipeAC) / (2 * KPipeAD * abs(PipeAD) + 2 * KPipeCD * abs(PipeCD) + 2 *KPipeAC * PipeAC)

        CorrectionValue2 =-1 * (KPipeAB * PipeAB * abs(PipeAB) + KPipeBC * PipeBC * abs(PipeBC) + KPipeAC * PipeAC * PipeAC) / (2 * KPipeAB * abs(PipeAB) + 2 * KPipeBC * abs(PipeBC) + 2 *KPipeAC * PipeAC)

        PipeAD = PipeAD + CorrectionValue1 
        PipeCD = PipeCD + CorrectionValue1 
        PipeAC = PipeAC - CorrectionValue1 + CorrectionValue2 
        PipeAB = PipeAB + CorrectionValue2 
        PipeBC = PipeBC + CorrectionValue2
    
    # Correction value formula and addition, if the sign of the flow in AC is not set, or the assumed flow in AC is 0.
    else:
        CorrectionValue1 = -1 * (KPipeAD * PipeAD * abs(PipeAD) + KPipeCD * PipeCD * abs(PipeCD) - KPipeAC * PipeAC * PipeAC) / (2 * KPipeAD * abs(PipeAD) + 2 * KPipeCD * abs(PipeCD) + 2 *KPipeAC * PipeAC)

        CorrectionValue2 =-1 * (KPipeAB * PipeAB * abs(PipeAB) + KPipeBC * PipeBC * abs(PipeBC) + KPipeAC * PipeAC * PipeAC) / (2 * KPipeAB * abs(PipeAB) + 2 * KPipeBC * abs(PipeBC) + 2 *KPipeAC * PipeAC)

        PipeAD = PipeAD + CorrectionValue1 
        PipeCD = PipeCD + CorrectionValue1 
        PipeAC = PipeAC - CorrectionValue1 + CorrectionValue2 
        PipeAB = PipeAB + CorrectionValue2 
        PipeBC = PipeBC + CorrectionValue2
        ClockwiseFlowAC = 2

    print(CorrectionValue1)
    print(CorrectionValue2)
    iteration_counter = iteration_counter + 1

# Final Results.
print("Pipe AB after correction: " + str(PipeAB))
print("Pipe BC after correction: " + str(PipeBC))
print("Pipe AC after correction: " + str(PipeAC))
print("Pipe AC's sign with respect to loop " + str(ClockwiseFlowAC))
print("Pipe CD after correction: " + str(PipeCD))
print("Pipe AD after correction: " + str(PipeAD))

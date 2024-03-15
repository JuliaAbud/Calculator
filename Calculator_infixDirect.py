#__________________________________________________________________________________________
#-----------------------------------------------------------
# Julia Abud
# juliarabud@gmail.com
# 14 Mar 2024
#-----------------------------------------------------------
# Description: Simple calculator that keeps the infix expession always
# Python 3.9
#__________________________________________________________________________________________


import re

class CalculatorInfixDirect:

    debug = True
    splitSymbols = "-+*/^()"
    eStr = ""
    eList=None
    result = 0

    def __init__(self):
        print("""\
 _____       _            _       _             
/  __ \     | |          | |     | |            
| /  \/ __ _| | ___ _   _| | __ _| |_ ___  _ __ 
| |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|
| \__/\ (_| | | (__| |_| | | (_| | || (_) | |   
 \____/\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
                              Infix expression (Direct)
                    """)
        self.PrintInstructions();
         
    def PrintInstructions(self):
        print("""\
        This Calculator can process operations with + - * / ^ ( ) and will respect their priority 
        It accepts integers, floats and negative numbers
        'test' : Will do a unit test using "files/tests.txt
        'exit' : Will exit this calculator and let you choose again
        _______________________________________________________
        This calculator will process directly from the infix expression without reorganizing. 
        Advantages: To keep it infix makes it is easier to see the steps that were followed in a human-way.
        Disadvanatge: Slower algorithm compared to using postfix as it needs to read the expression multiple times (once per operator)
        _______________________________________________________
                    """)
        
        print("example:")
        self.Calculate("3+3^2*4(-2.5+9/3)")
        self.GetInput()

    def GetInput(self):
        expression = input("Enter expression:")
        if(expression!="exit"):
            if (expression=="test"):
                self.UnitTest("files/tests.txt")
            else:
                self.Calculate(expression)
            self.GetInput()

    def Calculate(self, e): 
        self.eStr = e
        print('Infix expression: ', self.eStr )
        self.eList= self.__SplitExpression(self.eStr)
        if(self.__TestValidExpression(self.eStr)):
            self.__CalculateExpression()
            print ("Solution: "+str(self.result)+"\n")

    def __TestValidExpression(self,exprStr):      
        # Has any character that is not our symbols .(dot) and digits
        invalidSymbols = re.findall("[^"+self.splitSymbols+".0-9]",exprStr)
        if len(invalidSymbols)>0 : 
            print("There is at least one invalid character in the expression. Please check.")
            return False
        # Has same amount of right and left parentheses
        if len(re.findall("[(]",exprStr)) != len(re.findall("[)]",exprStr)): 
            print("There is not an equal amount of right and left parentheses. Please check.")
            return False
        return True

    def __SplitExpression(self,e):
        #split with lookbehind and lookahead, they match to a position not to characters
        e_parts = re.split("(?<=["+self.splitSymbols+"])|(?=["+self.splitSymbols+"])",e)

        #the split could return emty slots in the frst and last position, remove them if needed
        if(e_parts[0]==''):
            del(e_parts[0])
        if(e_parts[-1]==''):
            del(e_parts[-1])

        # Detect negative numbers
        for x in range(len(e_parts)-1,0,-1):
            if e_parts[x] == '-':
                combine=False
                if(x-1<0): combine = True
                elif re.match("[-+*/^(]",e_parts[x-1]): combine = True
                if combine: 
                    e_parts[x] = e_parts[x]+e_parts[x+1]
                    del e_parts[x+1]

        # Make float what can be float
        for index, item in enumerate(e_parts):
            try:
                e_parts[index] = float(item)
            except:
                pass
        return e_parts

    def __CalculateSimpleExpression(self,e):
        if len(e)==3:
            if e[1]=="+":
                self.result = e[0]+e[2]
            elif e[1]=="-":
                self.result = e[0]-e[2]
            elif e[1]=="*":
                self.result =  e[0]*e[2]
            elif e[1]=="/":
                try: 
                    self.result =  e[0]/e[2]
                except: 
                    self.result = None
                    print("Error: Zero Division")
            elif e[1]=="^":
                self.result =  pow(e[0],e[2])
            return self.result

    def __CalculateExpression(self):

        if self.debug: print(self.eList)

        # Priority 0 : ( ) resets the highest operator
        # Priority 1 : + -
        # Priority 2 : * /
        # Priority 3 : ^
        priority = 0
        endPthsIdx = startPthsIdx = 0
        operatorIdx = None

        for x in range(len(self.eList)):
            if self.eList[x]=='(':
                startPthsIdx = x
                priority = 0
            elif self.eList[x]==')':
                endPthsIdx = x
                break
            elif (self.eList[x]=='+' or self.eList[x]=='-') and (priority<1):
                operatorIdx = x
                priority=1
            elif (self.eList[x]=='*' or self.eList[x]=='/') and (priority<2):
                operatorIdx = x
                priority=2
            elif self.eList[x]=='^' and (priority<3):
                operatorIdx = x
                priority=3

        # Clean parenthesis containing juts a number and Apply simple operations
        if(endPthsIdx-startPthsIdx == 2):
            multiply = False
            # If the parenthesis if preceded by another number
            if(startPthsIdx>0):
                if type(self.eList[startPthsIdx-1]) is float: 
                    self.eList[startPthsIdx] = '*'
                    multiply = True

            del self.eList[endPthsIdx]
            if not multiply: del self.eList[startPthsIdx]

        elif(operatorIdx!=None):
            result = self.__CalculateSimpleExpression(self.eList[operatorIdx-1:operatorIdx+2])
            self.eList[operatorIdx-1]=result
            del self.eList[operatorIdx:operatorIdx+2]
        
        if(len(self.eList)==1):
            self.result = self.eList[0]
        else:
            self.__CalculateExpression()


    def UnitTest(self, file):
        print('-------------------------')
        print('-------UNIT TEST---------')
        print('-------------------------')
        testFile = open(file, "r")
        for line in testFile:
            equation = line
            print('Tested equation: ', equation)
            equation = equation.replace(" ", "")
            expression = equation.partition(":")[0]
            self.Calculate(expression)
            print('-------------------------')
        testFile.close()


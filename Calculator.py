#__________________________________________________________________________________________
#-----------------------------------------------------------
# Julia Abud
# juliarabud@gmail.com
# 14 Mar 2024
#-----------------------------------------------------------
# Description: Simple calculator
#__________________________________________________________________________________________


import re

class Calculator:

    debug = True
    splitSymbols = "-+*/^()"
    eStr = ""
    eList=None
    result = 0

    def __init__(self, expression=""):
        if (len(expression)>0):
            self.Calculate(expression)

    def Calculate(self, e): 
        self.eStr = e
        print('Infix expression: ', self.eStr )
        self.eList= self.__SplitExpression()
        if(self.__TestValidExpression()):
            self.__CalculateExpression()
            print ("Solution: "+str(self.result))

    def __TestValidExpression(self):      
        # Has any character that is not our symbols .(dot) and digits
        invalidSymbols = re.findall("[^"+self.splitSymbols+".0-9]",self.eStr)
        if len(invalidSymbols)>0 : 
            print("There is at least one invalid character in the expression. Please check.")
            return False
        # Has same amount of right and left parentheses
        if len(re.findall("[(]",self.eStr)) != len(re.findall("[)]",self.eStr)): 
            print("There is not an equal amount of right and left parentheses. Please check.")
            return False
        return True

    def __SplitExpression(self):
        #split with lookbehind and lookahead, they match to a position not to characters
        e_parts = re.split("(?<=["+self.splitSymbols+"])|(?=["+self.splitSymbols+"])",self.eStr)
        #the split could return empty slots in the first and last position, remove them if needed
        if(e_parts[0]==''):
            del(e_parts[0])
        if(e_parts[-1]==''):
            del(e_parts[-1])
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
                self.result =  e[0]/e[2]
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

        if(endPthsIdx-startPthsIdx == 2):
            self.eList[startPthsIdx] = self.eList[startPthsIdx+1]
            del self.eList[startPthsIdx+1:endPthsIdx+1]
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



def main():
    c = Calculator()
    c.Calculate("5+3*(4-6/(3))")
    c.UnitTest("files/tests.txt")

if __name__ == "__main__":
    main()
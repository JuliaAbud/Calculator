#__________________________________________________________________________________________
#-----------------------------------------------------------
# Julia Abud
# juliarabud@gmail.com
# 15 Mar 2024
#-----------------------------------------------------------
# Description: Simple calculator using postfix Expression
# Python 3.9
#__________________________________________________________________________________________


import re

class CalculatorPostfix:

    debug = True
    splitSymbols = "-+*/^()"
    eStr = ""
    eList=None
    result = 0

    def __init__(self):
        self.IntroText();
         
    def IntroText(self):
        print("""\
 _____       _            _       _             
/  __ \     | |          | |     | |            
| /  \/ __ _| | ___ _   _| | __ _| |_ ___  _ __ 
| |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|
| \__/\ (_| | | (__| |_| | | (_| | || (_) | |   
 \____/\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
                                Postfix expression
        """)
        print("""\
        This Calculator can process operations with + - * / ^ ( ) and will respect their priority 
        It accepts integers, floats and negative numbers
        'test' : Will do a unit test using "files/tests.txt"
        'exit' : Will exit this calculator and let you choose again
        _______________________________________________________
        This calculator will transform an infix expression to postfix to be able to process. 
        Advantages: to calculate from postfix it is efficient. 
        It will only run once through our expression 
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
            self.ePostFix = self.__InfixToPostfix(self.eList)
            self.result = self.__CalculatePostfixExpression(self.ePostFix)
            print ("Solution: "+str(self.result)+"\n")

    def __TestValidExpression(self,exprStr):      
        # Does it has any character that is not our symbols .(dot) and digits
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

        # The split could return empty slots in the first and last position, remove them if needed
        if(e_parts[0]==''): del(e_parts[0])
        if(e_parts[-1]==''): del(e_parts[-1])

        # Detect negative numbers and number preceding parenthesis
        for x in range(len(e_parts)-1,0,-1):
            #Negative numbers, we combine contents of both indexes
            if e_parts[x] == '-':
                combine=False
                if(x-1<0): combine = True
                elif re.match("[-+*/^(]",e_parts[x-1]): combine = True
                if combine: 
                    e_parts[x] = e_parts[x]+e_parts[x+1]
                    del e_parts[x+1]
            #Number preceding parenthesis, we need to push a *
            if e_parts[x] == '(':
                e_parts.insert(x,'*')

        # Make float what can be float
        for index, item in enumerate(e_parts):
            try:
                e_parts[index] = float(item)
            except:
                pass

        if self.debug: print("Split expression: "+str(e_parts))
        return e_parts

    def __InfixToPostfix(self,eList):
        infix = eList
        postfix = []
        stack = []
        priority = { '(': 0, '+': 1 , '-': 1, '*': 2, '/': 2, '^': 3}

        for x in range(len(infix)):
            v = infix[x]
            #check if it is an operator
            if re.match("[-+*/^]", str(v)) and (type(v) is not float):
                while stack and (priority.get(v) < priority.get(stack[-1]) or 
                                 (priority.get(v) == priority.get(stack[-1]) and v == '^')):
                    postfix.append(stack.pop())
                stack.append(v)
            elif v == '(': 
                stack.append(v)
            elif v == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            #what is left is for it to be an operand
            else:
                postfix.append(v)
        while stack:
            postfix.append(stack.pop())

        if self.debug: print("Postfix expression: "+ str(postfix))
        return postfix

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

    def __CalculatePostfixExpression(self,e):
        if self.debug: print(e)
        postfix = e
        stack = []
        for x in range(len(postfix)):
            v = postfix[x]
            if type(v) is float: 
                stack.append(v)
            else:
                operand1 = stack.pop()
                operand2 = stack.pop()
                result = self.__CalculateSimpleExpression([operand2, v, operand1])
                stack.append(result)
            if self.debug: print(stack)
        if(len(stack)==1):
            return stack[0]

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



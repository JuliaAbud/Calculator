#__________________________________________________________________________________________
#-----------------------------------------------------------
# Julia Abud
# juliarabud@gmail.com
# 15 Mar 2024
#-----------------------------------------------------------
# Description: Allows to choose between our two calculators
# Python 3.9
#__________________________________________________________________________________________

import Calculator_infixDirect as Cin
import Calculator_postfix as Cpost

def InputTypeCalculator():
    cType = input("What type of calculator process you wanna use (infix/postfix):")
    if (cType=="infix"):
        Cin.CalculatorInfixDirect()
    if (cType=="postfix"):
        Cpost.CalculatorPostfix()
    InputTypeCalculator()

def main():
    InputTypeCalculator()

if __name__ == "__main__":
    main()
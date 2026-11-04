# added comment for iteration one

# import statements
import re;
import operator;
import time;
from typing import final;

# start of program
# DISCLAIMER: All veriable names are in camelCase since I learned Java as my first programming language
# I will use underscores in the future


# main class
# calculator class
@final
class TrashCalculator:
    AMOUNT_OF_INSTANCES = 0;

    # initialize an instance variable equation to store the user's equation in constructor
    def __init__(self):
        try:
            if (TrashCalculator.AMOUNT_OF_INSTANCES == 1):
                raise ManyInstancesException();

            TrashCalculator.AMOUNT_OF_INSTANCES += 1;

            self.equation = "";
        except ManyInstancesException as e:
            print(e);

    def __init_subclass__(cls, **kwargs):
        raise TypeError(f"Class '{cls.__name__}' can not inherit from class 'TrashCalculator'");

    # gets the user's input
    def getUserInput(self):
        return input();

    # rules for a valid equation
    def rules(self):
        print("Rules:\n1. No parenthesis/brackets (calculator no support)\n2. Asterisk (*) only for multiplication" \
            "\n3. ^, *, /, +, - are exponents, multiplication, division, addition, and substraction\n" \
            "   a) Decimal exponents can represent roots (taking principle root)\n" \
            "4. Resulting answer can not be over the float limit of numbers\n   a) About 2^1024 or about 1.7 x 10^308\n" \
            "Special operators: // (integer division), % (modulo)");

    # calculates the result of 2 numbers and its operation
    def calculate(self, numOne, numTwo, operator):
        return operator(numOne, numTwo);

    # performs equation's operations using operator precedence rules
    def doOperation(self, equation):

        if (equation[0] == "+"):
            equation = equation[:0] + "" + equation[1:];

        if (equation[0] == "*" or equation[0] == "/" or equation[0] == "^" or equation[0] == "%"):
            raise InvalidEquationException();

        # decides what operators are going to get evaluated during the current loop
        operandNumber = 1;

        # these two patterns detect and extract all numbers, positive, negative, and decimals
        negativeNumberPattern = r'(?<![\d.])-\d+(?:\.\d+)?|\d+(?:\.\d+)?';
        positiveNumberPattern = r'\b\d+\.\d+|\b\d+\b|\b\.\d+\b\d+';

        # combines the two patterns above
        combinedNumberPattern = f"{negativeNumberPattern}|{positiveNumberPattern}";

        equationNumbers = re.findall(combinedNumberPattern, equation);

        # removes all numbers from the inputted equation string
        # leaves behind all other operators
        equation = re.sub(combinedNumberPattern, " ", equation);

        equationOperations = re.findall(r'//|\+|\-|\^|\*|/|%', equation);

        # checks if any numbers were put into the equation
        if (len(equationNumbers) == 0):
            raise InvalidEquationException();

        # checks if enough numbers were put into the equation
        # # of numbers should be one more than # of operators
        if (len(equationNumbers) == len(equationOperations)):
            raise InvalidEquationException();

        operationOne = None;
        operationTwo = None;
        operationThree = None;
        operationFour = None;

        # repeats the evaluation process until a single number is left in the 'equationNumbers' list
        while (len(equationNumbers) != 1):

            # positions to loop through the list with operators
            startingPoint = 0;
            endingPoint = len(equationOperations);
            increment = 1;

            # 'operandNumber' decides what operations are going to be performed in current loop
            # structured to follow operator precedence rules
            if (operandNumber == 1):
                operationOne = "^";
                startingPoint = len(equationOperations) - 1;
                endingPoint  = -1;
                increment = -1;
            elif (operandNumber == 2):
                operationOne = "*";
                operationTwo = "/";
                operationThree = "//";
                operationFour = "%";
            elif (operandNumber == 3):
                operationOne = "+";
                operationTwo = "-";

            intermediateAnswer = 0;
            equationEvaluated = False;

            # checks to see if any current operators are in the operators list
            # if so, evaluate numbers 1 behind and after that position with the operator in that position
            for iterator in range (startingPoint, endingPoint, increment):
                
                if (str(equationOperations[iterator]) == operationOne):
                    equationEvaluated = True;

                    numberOne = float(equationNumbers[iterator]);
                    numberTwo = float(equationNumbers[iterator + 1]);

                    if (operationOne == "^"):

                        isAnswerNegative = False;
                        signChanging = 1.0;

                        if (numberOne < 0):
                            isAnswerNegative = True;

                        if (isAnswerNegative):
                            signChanging = -1.0;
                            numberOne = abs(numberOne);
                        
                        intermediateAnswer = signChanging * self.calculate(numberOne, numberTwo, operator.pow);
                    if (operationOne == "*"):
                        intermediateAnswer = self.calculate(numberOne, numberTwo, operator.mul);
                    if (operationOne == "+"):
                        intermediateAnswer = self.calculate(numberOne, numberTwo, operator.add);


                if (equationOperations[iterator] == operationTwo):
                    equationEvaluated = True;

                    numberOne = float(equationNumbers[iterator]);
                    numberTwo = float(equationNumbers[iterator + 1]);

                    if (operationTwo == "/"):
                        intermediateAnswer = self.calculate(numberOne, numberTwo, operator.truediv);
                    if (operationTwo == "-"):
                        intermediateAnswer = self.calculate(numberOne, numberTwo, operator.sub);

                if (equationOperations[iterator] == operationThree):
                    equationEvaluated = True;

                    numberOne = float(equationNumbers[iterator]);
                    numberTwo = float(equationNumbers[iterator + 1]);

                    if (operationThree == "//"):
                        intermediateAnswer = self.calculate(numberOne, numberTwo, operator.floordiv);

                if (equationOperations[iterator] == operationFour):
                    equationEvaluated = True;

                    numberOne = float(equationNumbers[iterator]);
                    numberTwo = float(equationNumbers[iterator + 1]);

                    if (operationFour == "%"):
                        intermediateAnswer = self.calculate(numberOne, numberTwo, operator.mod);
                
                if (equationEvaluated):
                    equationNumbers[iterator] = intermediateAnswer;

                    del equationNumbers[iterator + 1];
                    del equationOperations[iterator];

                    # breaks from 'for' loop and iterates equation again using same operators
                    # since current equation got evaluated
                    break;

            # switches operators to new types if all the current highest precedence operators got evaluated
            if (not equationEvaluated):
                operandNumber += 1;

        # returns single final answer after equation has been evaluated as a whole
        return str(equationNumbers[0]);

    # checks if user equation follows all rules listed
    def validateEquation(self, equation):

        # checks if equation has 2 or more periods next to eachother (e.g. 2..5, 2...5)
        # if it does, that's not a number so throw an exception
        if (bool(re.search(r'(\.)(\1)+', equation))):
            raise InvalidEquationException();

        # checks for any invalid symbols other than the ones mentioned in rules
        # also checks for any letters
        # also checks for any substraction symbol in between two other symbols
        # throws InvalidEquation exception if any of the above are present
        anyInvalidSymbol = r'[^\w\-+/*^%\.]';
        consecutiveInvalid = r'(?!//[^/]|//(?!\S))[/*^%\.]{2,}';
        consecutiveInvalidForSubstraction = r'[-+/*^%\.]{3,}';
        consecutiveInvalidForAddition = r'\+[\/\*%\^]';

        combinedInvalidPattern = f"{anyInvalidSymbol}|{consecutiveInvalid}|{consecutiveInvalidForSubstraction}|{consecutiveInvalidForAddition}";

        if (re.compile(combinedInvalidPattern).search(equation)):
            raise InvalidEquationException();

    # simplifies equation for multiple ++ or +- or -- before verifying equation validity
    # also simplifies whitespace and other operators
    def simplifyInitialEquation(self, equation):

        # gets rid of any whitespace
        equation = re.sub(r"\s+", "", equation);

        # simplifies double minuses to a plus
        equation = re.sub(r"-{2,}", lambda m: "+" * (len(m.group(0)) // 2) + "-" * (len(m.group(0)) % 2), equation);

        # simplifies long lines of pluses into a single plus
        equation = re.sub(r"\++", "+", equation);

        # simplifies plus-minuses into a singe minus
        equation = equation.replace("+-", "-");

        # converts another way to write exponents into the symbol calculator uses
        equation = equation.replace("**", "^");

        # simplifies operator-plus into the lone operator
        # (e.g /+ -> *, *+ -> *)
        equation = re.sub(r"([\/\*\^%])\+", r"\1", equation);

        # converts number-decimal into floats by adding a 0 after the decimal point
        # (e.g. 1. -> 1.0, 5. -> 5.0)
        equation = re.sub(r"(\d+)\.(?!\d|\.)", r"\1.0", equation);
        
        self.validateEquation(equation);

        equationAnswer = self.doOperation(equation);

        return equationAnswer;

    # main process to evaluate the equation and returns an answer
    def startEvaluatingEquation(self):

        equationAnswer = float(self.simplifyInitialEquation(self.equation));
        equationAnswer = round(equationAnswer, 10);

        return equationAnswer;

    # entry point of the main program
    # gets an equation and starts using other methods to evaluate the equation
    # afterwards, prints the final answer
    # main exception handling
    def start(self):

        exitProgram = False;

        while (not exitProgram):
            print("Enter an equation (type 'exit' to leave the program)");
            self.rules();

            validEquation = False;

            while (not validEquation):
                try:
                    userEquation = self.getUserInput();

                    if (re.sub(r'\s+', "", userEquation).lower() == "exit"):
                        exitProgram = True;

                        break;
                    
                    self.equation = userEquation;

                    answer = self.startEvaluatingEquation();

                    print("Answer: " + str(answer));

                    validEquation = True;

                    # waits 4 seconds before asking for another equation
                    # so user can see the answer
                    time.sleep(4);
                
                except InvalidEquationException:
                    print("Invalid equation\n");

                    time.sleep(3);

                    print("Reenter another equation following the rules:");
                    self.rules();
                
                except ZeroDivisionError:
                    print("The equation divides a number by zero (0)\n");

                    time.sleep(3);

                    print("Enter a new equation");

                except OverflowError:
                    print("The equation yields a result too big of a number for the program to store\n");

                    time.sleep(4);

                    print("Enter a new equation");

        print("Exited program");

# custom exception classes

# limit class instantiation to 1 cuz why not :p
@final
class ManyInstancesException(Exception):
    def __init__(self):
        self.msg = "Can not instantiate two or more instances of this class";

    def __str__(self):
        return f"{self.msg}";

# represents an invalid equation
@final
class InvalidEquationException(Exception):
    def __init__(self):
        self.msg = "Equation invalid";

    def __str__(self):
        return f"{self.msg}";

calc = TrashCalculator();

calc.start();
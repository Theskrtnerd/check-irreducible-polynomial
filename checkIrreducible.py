import math
from sympy import *

###Tools

#Function to print out the solution if f(x) is irreducible
def printSolution(coeffs_list, constant, j, criterion, new_coeffs_list):
  print(f"You've inputed the function f(x)={generateFunctionString(coeffs_list)}")
  if constant != 0:
    if constant > 0:
      print(f"We'll subtitute x by x+{constant}. Thus, the function will become f(x+{constant})={generateFunctionString(coeffs_list,f'(x+{constant})')}={generateFunctionString(getNewCoefficientsList(coeffs_list,constant))}")
    else:
      print(f"We'll subtitute x by x{constant}. Thus, the function will become f(x{constant})={generateFunctionString(coeffs_list,f'(x{constant})')}={generateFunctionString(getNewCoefficientsList(coeffs_list,constant))}")
  
  if j == 1:
    print(f"We'll subtitute x by 1/x. Thus, the function will become x^{len(coeffs_list)-1}*f(1/x)={generateFunctionString(list(reversed(getNewCoefficientsList(coeffs_list,constant))))}")
  
  if criterion[0] == "Eisenstein":
    print(f"We'll apply the Eisenstein's criterion, and for p={criterion[1]}, the function satisfies the conditions. Hence, the function's indeed irreducible")
  
  elif criterion[0] == "Perron":
    print(f"We'll apply the Perron's criterion, and therefore, the function's irreducible")
  
  elif criterion[0] == "Cohn":
    print(f"We'll apply the Cohn's criterion. For b = {criterion[1]}, the function f({criterion[1]}) will be equal to {replaceFunctionX(criterion[1],new_coeffs_list)}, which is a prime number. Hence, the function's irreducible")

#Wiki about Newton Binomial Formula: "https://en.wikipedia.org/wiki/Binomial_theorem"
#Newton Binomial Formula to expand a_i(x+k)^n
def newtonBinomialExpansion(coeff_ai,constant_k,degree_n):
  coeffs_list=[]
  for i in range(0,degree_n+1):
    coeffs_list.append(coeff_ai*math.comb(degree_n,i)*(constant_k**i))
  return coeffs_list

#Get the new coefficients list for the function f(x+k)
def getNewCoefficientsList(coeffs_list, constant_k):
  degree_n = len(coeffs_list)-1
  new_coeffs_list = [0 for i in range(len(coeffs_list))]
  for i in range(degree_n,-1,-1):
    bruh = [0 for j in range(i)]+ newtonBinomialExpansion(coeffs_list[i],constant_k,degree_n-i)
    new_coeffs_list = [sum(value) for value in zip(new_coeffs_list, bruh)]

  return(new_coeffs_list)

#Subtitute x by a into the function f(x), and return f(a)
def replaceFunctionX(a, coeffs_list):
  sum = 0
  for i in range(len(coeffs_list)):
    sum = sum + coeffs_list[i]*a**(len(coeffs_list)-1-i)
  return sum

#Generate the string to display the polynomial from the coefficients list
def generateFunctionString(coeffs_list, var_string="x"):
  string = ""
  n = len(coeffs_list)
  for i in range(n):
    if coeffs_list[i] != 0:
      if i == n-1:
        bruh = f"{coeffs_list[i]}"
      elif i == n-2:
        if coeffs_list[i] == 1:
          bruh = f"{var_string}"
        elif coeffs_list[i] == -1:
          bruh = "-{var_string}"
        else:
          bruh = f"{coeffs_list[i]}{var_string}"
      else:
        if coeffs_list[i] == 1:
          bruh = f"{var_string}^{n-1-i}"
        elif coeffs_list[i] == -1:
          bruh = f"-{var_string}^{n-1-i}"
        else:
          bruh = f"{coeffs_list[i]}{var_string}^{n-1-i}"    
      if coeffs_list[i] > 0 and i != 0:
        symbol="+"
      else:
        symbol=""
      string = string + symbol + bruh
  return string



### List of criterions

#Wiki about Eisenstein's criterion: "https://en.wikipedia.org/wiki/Eisenstein%27s_criterion"
#Check the Eisenstein's criterion with a prime number p
def checkEisensteinCriterionWithP(coeffs_list, prime_p):
  for i in range(len(coeffs_list)):
    if i == 0:
      if coeffs_list[0] % prime_p == 0:
        return False
    elif i == (len(coeffs_list)-1):
      if coeffs_list[i] % prime_p != 0 or coeffs_list[i] % (prime_p**2) == 0:
        return False
    else:
      if coeffs_list[i] % prime_p != 0:
        return False
  return True

#Eisenstein's criterion
def eisensteinCriterion(coeffs_list):
  list_of_primes_p = primefactors(math.gcd(*coeffs_list[1:]))
  for prime_p in list_of_primes_p:
    if checkEisensteinCriterionWithP(coeffs_list,prime_p) ==  True:
      return prime_p
  return False

#Wiki about Perron's criterion: "https://en.wikipedia.org/wiki/Perron%27s_irreducibility_criterion"
#Perron's criterion
def perronCriterion(coeffs_list):
  if coeffs_list[0] != 1:
    return False
  sum = 1
  for i in range(2,len(coeffs_list)):
    sum += abs(coeffs_list[i])
  if abs(coeffs_list[1]) > sum:
    return True
  return False

#Work in progress :))
#Osada's criterion
def osadaCriterion(coeffs_list):
  pass

#Wiki about Cohn's criterion: "https://en.wikipedia.org/wiki/Cohn%27s_irreducibility_criterion"
#Cohn's criterion
def cohnCriterion(coeffs_list):
  for i in range(len(coeffs_list)):
    if coeffs_list[i] < 0:
      return False
  t = max(coeffs_list) + 1
  for i in range(t, t+10):
    if isprime(replaceFunctionX(i, coeffs_list)) == True:
      return i
  return False


def checkIrreducible(coeffs_list):
  for constant_k in range(0,1000):
    for i in [1,-1]:
      for j in [0,1]:
        new_coeffs_list = getNewCoefficientsList(coeffs_list,i*constant_k)
        if j == 1 and new_coeffs_list[-1] != 0:
          new_coeffs_list.reverse()
        if eisensteinCriterion(new_coeffs_list) != False:
          printSolution(coeffs_list, i*constant_k, j, ["Eisenstein",eisensteinCriterion(new_coeffs_list)], new_coeffs_list)
          return True
        if perronCriterion(new_coeffs_list):
          printSolution(coeffs_list, i*constant_k, j, ["Perron"], new_coeffs_list)
          return True
        if constant_k >= 0 and constant_k <= 100:
          if cohnCriterion(new_coeffs_list) != False:
            printSolution(coeffs_list, i*constant_k, j, ["Cohn", cohnCriterion(new_coeffs_list)], new_coeffs_list)
            return True
  return False
  
  
  
      
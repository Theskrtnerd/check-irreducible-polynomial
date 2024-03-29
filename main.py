from checkIrreducible import checkIrreducible

def main():
  print("This is a python script to check whether your polynomial is irreducible or not\nThis script uses different criterions like Eisenstein's criterion, Perron's criterion, and Cohn's criterion. This will only use several criterions to check, and might not be correct\nBut if a polynomial is indeed irreducible, this script will show you the solution to prove that the polynomial is irreducible using one of the criterions\nPlease enter the coefficients of your polynomial (enter '2 -3 1' if your polynomial is 2x^2-3x+1)")
  coefficients = [int(i) for i in input().split()]
  if checkIrreducible(coefficients) == False:
    print(f"This function's reducible")

if __name__ == '__main__':
  main()
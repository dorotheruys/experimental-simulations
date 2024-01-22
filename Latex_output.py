import pandas as pd

df = pd.read_excel("Testmatrix.xlsx")

latex_code = df.to_latex(index=True)

with open('testmatrix.tex', 'w') as f:
    f.write(latex_code)
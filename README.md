# SolarGazer: A Simple Panel Regressions Wrapper for Latex Tables in Python

## Description

solargazer is an extremely simple library designed to offer additional functionalities relative to stargazer for Latex table generation in Python. The library is compatible with the PanelOLS class from statsmodels for clean tables in Latex. 

IMPORTANT: Follow this Colab tutorial notebook for the easiest setup guide: https://colab.research.google.com/drive/1tshfY-2al7asU7pTFvFFg1n4NSvLXtZg?usp=sharing

## Installation

Installation is extremely simple using pip. If you are using this to make regression tabels, you will need to have linearmodels installed. Open your terminal or command prompt and run:

```bash
pip install linearmodels
```

Then you can install solargazer using: 
```bash
pip install solargazer
``` 

To run the tables in Latex, you will also need to include this in your preamble:
```latex
\usepackage{amssymb}
\usepackage{threeparttable}
\usepackage{booktabs}
```

## Use

There is only one simple function. 

```python
from solargazer.solargazer import SolarGazer
SolarGazer().make_table(model_list,model_names, groupings = group_dict)
``` 

The function takes three parameters.
1. *model_list*: a list of your fitted PanelOLS models. This is post-processing, etc.
2. *model_names*: a list of strings which are the names you want for the columns in your regressions.
3. *grouping*: an optional dictionary to add groupings at the top of the regression table, if you want to make clear that several of the regressions are of the same type. If you don't provide a dictionary here, there will be no additional title at the top, just the model names. 

So a full example might be:
```python
SolarGazer().make_table([model1, model2, model3],['model 1','model 2','model 3'], groupings = {'Republican':[model1, model2],'Democratic':[model3]})
```

The library will output a LateX string that you can directly transfer to your file. 
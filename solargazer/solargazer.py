import pandas as pd

class SolarGazer:
    def __init__(self):
        pass
    def format_coefficient(self, row):
        """Format coefficient string with standard errors and significance stars."""
        star = '*' * int(row['pvalue'] < 0.1) + '*' * int(row['pvalue'] < 0.05) + '*' * int(row['pvalue'] < 0.01)
        return f"""{row['parameter']:.3f}$^{{{star}}}$ ({row['std_error']:.3f})""" 
    
    def get_coefs(self, model, model_name, drop_fe_rows = False):
        tmp = pd.DataFrame(model.params).join(pd.DataFrame(model.pvalues)).join(pd.DataFrame(model.std_errors))
        tmp.loc[:,model_name] = tmp.apply(self.format_coefficient, axis = 1)
        tmp.at['Time FE',model_name] = model._time_effect
        tmp.at['Entity FE',model_name] = model._entity_effect
        tmp.at['Standard Errors',model_name] = model._cov_type
        tmp.at['R-Squared',model_name] = round(model.rsquared, 3)
        tmp.at['Number of Observations',model_name] = model.nobs
        tmp[model_name] = tmp[model_name].replace(False, '').replace(True, '\checkmark')
        if drop_fe_rows:
            tmp = tmp[~tmp.index.str.contains('\.')]
        return tmp[model_name]
    
    def create_merged_table(self, models, model_names, drop_fe_rows = False):
        final = pd.DataFrame()
        for model, name in zip(models, model_names):
            curr = self.get_coefs(model, name, drop_fe_rows=drop_fe_rows)
            final = pd.merge(final, curr, left_index = True, right_index = True, how = 'outer')
        return final

    def generate_regression_table(self, df, model_labels, groupings=None):
        """
        Generates LaTeX code for a regression table with optional grouping of models.
        
        Parameters:
        - df: pandas DataFrame containing the regression results.
        - model_labels: List of column names in df to use as model labels in the table.
        - groupings: Optional dictionary where keys are group names and values are lists of model labels.
        """
        
        # Start of the table
        latex_str = "\\begin{threeparttable}\n" \
                    "\\begin{tabular}{l" + "c" * len(model_labels) + "}\n" \
                    "\\toprule\n"
        
        # Define the column spans for the group headers
        col_spans = []
        current_col = 2  # start after the row labels
        
        # Table column headers
        if groupings:
            # Create headers and calculate column spans for each group
            for group_name, labels in groupings.items():
                cols = len(labels)
                col_spans.append((current_col, current_col + cols - 1))
                current_col += cols
                latex_str += f"& \multicolumn{{{cols}}}{{c}}{{{group_name}}} "
            latex_str += "\\\\\n"
            
            # Sub-header lines for each group
            for span in col_spans:
                latex_str += "\\cmidrule(lr){" + f"{span[0]}-{span[1]}" + "}"
            latex_str += "\n"
            
            # Column labels for each group
            for label in model_labels:
                latex_str += f"& {label} "
            latex_str += "\\\\\n"
        else:
            for label in model_labels:
                latex_str += f"& {label} "
            latex_str += "\\\\\n"
        
        latex_str += "\\midrule\n"  # Add a line after the column headers

        # Table body
        for index, row in df.iterrows():
            if index not in ['Time FE', 'Entity FE', 'Standard Errors', 'R-Squared', 'Number of Observations']:
                # Split the coefficient and standard error
                row_data = [value if '(' not in value else value.split(' (') for value in row[model_labels]]
                coeffs = [item[0] if isinstance(item, list) else item for item in row_data]
                ses = [('(' + item[1] if isinstance(item, list) else '') for item in row_data]
                latex_str += f"{index} & " + " & ".join(coeffs) + "\\\\\n"
                latex_str += f"& " + " & ".join(ses) + "\\\\\n"
        
        # Line separator before the footer
        latex_str += "\\midrule\n"
        
        # Footer section for FE, SE, R-squared, and Observations
        footer_items = ['Time FE', 'Entity FE', 'R-Squared', 'Number of Observations']
        for item in footer_items:
            if item in df.index:
                row_data = " & ".join(str(df.loc[item, label]) for label in model_labels)
                latex_str += f"{item} & {row_data} \\\\\n"

        # Standard Errors row
        if 'Standard Errors' in df.index:
            se_data = " & ".join(str(df.loc['Standard Errors', label]) for label in model_labels)
            latex_str += f"Standard Errors & {se_data} \\\\\n"
        
        # End of the table
        latex_str += "\\bottomrule\n" \
                    "\\end{tabular}\n" \
                    "\\begin{tablenotes}\n" \
                    "\\small\n" \
                    "\\item Note: Standard errors in parentheses. * p$<$0.05, ** p$<$0.01, *** p$<$0.001.\n" \
                    "\\end{tablenotes}\n" \
                    "\\end{threeparttable}\n"
        
        return latex_str

    def make_table(self, model_list, model_names, groupings = None, drop_fe_rows = False):
        df = self.create_merged_table(model_list, model_names, drop_fe_rows = drop_fe_rows)
        df.fillna('', inplace=True)
        latex = self.generate_regression_table(df, model_names, groupings)
        print(latex)
import re
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.font_manager as font_manager

def extract_variables_and_values(file_path):
    # Lists to store mu_star and sigma values
    mu_star_values = []
    sigma_values = []
    
    # Regular expression pattern to match variable names and their associated values
    #variable_pattern = r'([a-zA-Z_]+)\s*:\s*\[([\d\s.]+)\]'
    variable_pattern = r'([a-zA-Z_]+)\s*:\s*\[([\d\s.eE+-]+)\]'
    
    # Open the file and extract variable names and values using regular expression
    with open(file_path, 'r') as file:
        content = file.read()
        matches = re.findall(variable_pattern, content)
        # Process each match and extract variable name and values
        for match in matches:
            variable_name = match[0]
            values = match[1].split()
            float_values = [float(value) for value in values]
            # Separate mu_star and sigma values based on variable name
            if variable_name == 'mu_star':
                mu_star_values.extend(float_values)
            elif variable_name == 'sigma':
                sigma_values.extend(float_values)

    min_value = min(mu_star_values)
    max_value = max(mu_star_values)
    mu_star_values_normalized = [(x - min_value) / (max_value - min_value) for x in mu_star_values]
    
    return mu_star_values, sigma_values, mu_star_values_normalized

# Path to the results.txt file
file_path = 'results.txt'

# Extract mu_star and sigma values from the results.txt file
mu_star, sigma, mu_star_normalized = extract_variables_and_values(file_path)

# Define a list of markers and lavels for the plot
markers = ['s', 'v', '^', '<', '>',
           'o', '1', 'D', '3', 'o', 'D', 'd',
           '8', '2', 'p', '*', 'h', '*',
           'X', 'x', '+']
labels  = ['$E_{11}$', '$E_{22}$', '$v_{12}$', '$v_{23}$', '$G_{12}$',
           '$X_{T}$', '$f_{XT}$', '$X_{C}$', '$f_{XC}$', '$Y_{T}$', '$Y_{C}$', '$S_{L}$',
           '$G_{XT}$', '$f_{GT}$', '$G_{XC}$', '$G_{Ic}$', '$G_{YC}$', '$G_{IIc}$',
           '$T_{I}$', '$T_{II}$', '$\eta_{BK}$']
#
# Plot figure
#
plt.figure(figsize=(8,4))
#cm = 1/2.54  # centimeters in inches
#plt.figure(figsize=(16*cm, 5*cm))
plt.bar(labels, mu_star_normalized)
#plt.bar(labels, mu_star, yerr=errors)


# Customize the plot if needed
plt.ylabel('$\mu^*$')
plt.tight_layout()
plt.savefig('p16r20_bar.png', format='png', dpi=1200)
plt.show()




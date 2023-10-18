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
        print(matches)
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
    
    return mu_star_values, sigma_values

# Path to the results.txt file
file_path = 'results.txt'

# Extract mu_star and sigma values from the results.txt file
mu_star, sigma = extract_variables_and_values(file_path)

# Define a list of markers and lavels for the plot
markers = ['s', 'v', '^', '<', '>',
           'o', '1', 'D', '3', 'o', 'D', 'd',
           '8', '2', 'p', '*', 'h', '*',
           'X', 'x', '+']
labels  = ['$E_{11}$', '$E_{22}$', '$v_{12}$', '$v_{23}$', '$G_{12}$',
           '$X_{T}$', '$f_{XT}$', '$X_{C}$', '$f_{XC}$', '$Y_{T}$', '$Y_{C}$', '$S_{L}$',
           '$G_{XT}$', '$f_{GT}$', '$G_{XC}$', '$G_{Ic}$', '$G_{YC}$', '$G_{IIc}$',
           '$T_{I}$', '$T_{II}$', '$\eta_{BK}$']

print(len(mu_star), len(sigma))
#
# Plot figure
#
plt.figure(figsize=(8,4))
#cm = 1/2.54  # centimeters in inches
#plt.figure(figsize=(16*cm, 5*cm))
for i in range(len(mu_star)):
    if labels[i] == '$G_{Ic}$' or labels[i] == '$Y_{T}$' or labels[i] == '$Y_{C}$':
        plt.plot(mu_star[i], sigma[i], marker=markers[i % len(markers)], markersize=9, linestyle = 'None', label=labels[i], markerfacecolor='none')
    else:
        plt.plot(mu_star[i], sigma[i], marker=markers[i % len(markers)], markersize=9, linestyle = 'None', label=labels[i])
    
# Draw lines to split quadrants
plt.plot([-max(mu_star)*0.05, max(mu_star)*1.05],[max(sigma)/2.,max(sigma)/2.], linewidth=1, linestyle= '--', color='grey' )
plt.plot([max(mu_star)/2,max(mu_star)/2],[-max(sigma)*0.05,max(sigma)*1.05], linewidth=1, linestyle= '--', color='grey' )

# Customize the plot if needed
plt.xlabel('$\mu^*$')
plt.ylabel('$\sigma$')
plt.title('$p=16$, $r=20$')
plt.xlim([-max(mu_star)*0.05,max(mu_star)*1.05])
plt.ylim([-max(sigma)*0.05,max(sigma)*1.05])
#plt.grid(True)
plt.legend(ncol=2, loc='center right', bbox_to_anchor=(1.45, 0.5))
plt.tight_layout()
plt.savefig('p16r20.png', format='png', dpi=1200)
plt.show()




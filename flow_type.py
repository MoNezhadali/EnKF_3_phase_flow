import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the function to determine the flow regime
def Flow_type(NFr, CL, L1, L2, L3, L4):
    """Function to Determine the Flow regime by the Method of Beggs and Brill"""
    # flow_type 1 - Segregated flow
    if (((CL < 0.01) and (NFr < L1)) or ((CL >= 0.01) and (NFr < L2))):
        return 1  # Segregated Flow
    
    # flow_type 2 - Transition flow
    if ((CL >= 0.01) and (L2 < NFr) and (NFr <= L3)):
        return 2  # Transition Flow
    
    # flow_type 3 - Intermittent flow
    if ((((0.01 <= CL) and (CL < 0.4)) and ((L3 < NFr) and (NFr < L1))) or ((CL >= 0.4) and (L3 < NFr) and (NFr <= L4))):
        return 3  # Intermittent Flow
    
    # flow_type 4 - Distributed flow
    if (((CL < 0.4) and (NFr >= L1)) or ((CL >= 0.4) and (NFr > L4))):
        return 4  # Distributed Flow
    
    return 0  # Undefined Flow

# Read the Excel file
file_path = './flow_results.xlsx'
df = pd.read_excel(file_path)

# Extract NFr and CL values
example_NFr = df['NFr'].values
example_CL = df['CL'].values

# Define the range for NFr and CL
NFr_values = np.logspace(-2, 2, 1000)  # Log scale from 0.01 to 100
CL_values = np.linspace(0.01, 1, 1000)  # Linear scale from 0.01 to 1

# Create a grid to hold the flow types
flow_map = np.zeros((len(CL_values), len(NFr_values)))

# Calculate the flow type for each combination of NFr and CL
for i, CL in enumerate(CL_values):
    L1 = 316 * CL ** 0.302
    L2 = 0.0009252 * CL ** (-2.4684)
    L3 = 0.1 * CL ** (-1.4516)
    L4 = 0.5 * CL ** (-6.738)
    
    for j, NFr in enumerate(NFr_values):
        flow_map[i, j] = Flow_type(NFr, CL, L1, L2, L3, L4)

# Plot the flow regime map
plt.figure(figsize=(10, 6))
contour = plt.contourf(NFr_values, CL_values, flow_map, levels=[0, 1, 2, 3, 4, 5], cmap='viridis', alpha=0.7)
cbar = plt.colorbar(contour, ticks=[1, 2, 3, 4])
cbar.ax.set_yticklabels(['Segregated Flow', 'Transition Flow', 'Intermittent Flow', 'Distributed Flow'])

plt.yscale('log')
plt.xscale('log')
plt.xlabel('NFr')
plt.ylabel('CL')
plt.title('Flow Regime Map')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Add example points to the plot
# plt.scatter(example_NFr, example_CL, color='black', marker='x')
# for i, txt in enumerate(range(len(example_NFr))):
#     plt.annotate('', (example_NFr[i], example_CL[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.show()

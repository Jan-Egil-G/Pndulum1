import matplotlib.pyplot as plt

# Define the data
cpu_small_mean = [0.00013831980198016715, 0.0001538386138614157]
cpu_small_std = [3.505606372586156e-05, 0.0000565350757852686]
gpu_small_mean = [0.018939956435643644, 0.0012419752475247407, 0.0015166386138614164, 0.0012400247524752886]
gpu_small_std = [0.1798107446044838, 0.0006087049893677482, 0.0012219723052485478, 0.0006022506077050028]
gpu_large_mean = [0.001822654455445829, 0.001807039603960553, 0.0014082039603960674, 0.0194971851485149]
gpu_large_std = [0.001595737439463353, 0.0017419757967364474, 0.0005968471983549903, 0.18319744352593748]
cpu_large_mean = [ 0.00021334554455452423, 0.00023512079207898667, 0.0002053435643562952, 0.00021246138613860392]
cpu_large_std = [4.197075058854175e-05, 4.69912338992378e-05, 2.3505009746124436e-05, 3.3263460344163515e-05]



# Create the bar plot
fig, ax = plt.subplots()
x = ['Sample1', 'Mean1', 'Sample2', 'Mean2', 'Sample3', 'Mean3', 'Sample4', 'Mean4','Sample5', 'Mean5', 'Sample6', 'Mean6','Sample7', 'Mean7', 'Sample8', 'Mean8','Sample9', 'Mean9', 'Sample10', 'Mean10','Sample11', 'Mean11', 'Sample12', 'Mean12','Sample', 'Mean', 'Sample', 'Mean','Sample', 'Mean', 'Sample', 'Mean','Sample', 'Mean', 'Sample', 'Mean','Sample', 'Mean', 'Sample', 'Mean','Sample', 'Mean', 'Sample', 'Mean','Sample', 'Mean', 'Sample', 'Mean','Sample', 'Mean', 'Sample', 'Mean',]
ax.barh(x[:2], cpu_small_mean, yerr=cpu_small_std, label='CPU Small Model')
ax.barh(x[2:6], gpu_small_mean, yerr=gpu_small_std, label='GPU Small Model')
ax.barh(x[10:14], gpu_large_mean, yerr=gpu_large_std, label='GPU Large Model')
ax.barh(x[6:10], cpu_large_mean, yerr=cpu_large_std, label='CPU Large Model')

# Add labels and legend
ax.set_xlabel('Sample,Mean')
# ax.set_ylabel('Mean')
ax.legend()

# Show the plot
plt.show()

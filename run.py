import pandas as pd
import numpy as np
import os
import glob
from glob import glob
import shutil
import csv

data_path = os.getenv('DATA_PATH','/data')
inputs_path = os.path.join(data_path, 'inputs')
parameters_path = os.path.join(inputs_path, 'parameters')
outputs_path = os.path.join(data_path, 'outputs')
if not os.path.exists(outputs_path):
    os.mkdir(outputs_path)
parameter_outputs_path = os.path.join(outputs_path, 'parameters')
parameter_outputs_path_ = outputs_path + '/' + 'parameters'
if not os.path.exists(parameter_outputs_path):
    os.mkdir(parameter_outputs_path_)

# Look to see if a parameter file has been added
parameter_file = glob(parameters_path + "/*.csv", recursive = True)
print('parameter_file:', parameter_file)

# Read environment variables
rainfall_total = int(os.getenv('TOTAL_DEPTH'))
duration = int(os.getenv('DURATION'))

unit_profile = np.array([0.017627993, 0.027784045, 0.041248418, 0.064500665, 0.100127555, 0.145482534, 0.20645758,
                         0.145482534, 0.100127555, 0.064500665, 0.041248418, 0.027784045, 0.017627993])

rainfall_times = np.linspace(start=0, stop=duration*3600, num=len(unit_profile))

unit_total = sum((unit_profile + np.append(unit_profile[1:], [0])) / 2 *
                 (np.append(rainfall_times[1:], rainfall_times[[-1]]+1)-rainfall_times))

rainfall_data = pd.DataFrame(list(unit_profile*rainfall_total/unit_total/1000) + [0, 0],
                        list(rainfall_times) + [duration*3600+1, duration*3600+2])

rainfall1 = pd.DataFrame(list(unit_profile*rainfall_total/unit_total/1000) + [0, 0])
rainfall2 = pd.DataFrame(list(rainfall_times) + [duration*3600+1, duration*3600+2])

rainfall = pd.concat([rainfall1, rainfall2], axis=1)
rainfall = rainfall.reset_index(drop=True)
print('rainfall:',rainfall)

rainfall.to_csv(os.path.join(outputs_path, 'rainfall_data.csv'), encoding='utf-8', index=False, header=True,float_format='%.6f')

with open(os.path.join(outputs_path,'rainfall_data.txt'),'a') as f:
    print('* * *', file = f)
    print('* * * rainfall ***', file = f)
    print('* * *', file = f)
    print(len(unit_profile), file = f)
    print('* * *', file = f)
    print(rainfall_data.to_string(header=False), file=f)
f.close()

# Move the amended parameter file to the outputs folder
if len(parameter_file) == 1 :
    file_path = os.path.splitext(parameter_file[0])
    print('Filepath:',file_path)
    filename=file_path[0].split("/")
    print('Filename:',filename[-1])

    src = parameter_file[0]
    print('src:',src)
    dst = os.path.join(parameter_outputs_path,filename[-1] + '.csv')
    print('dst,dst')
    shutil.copy(src,dst)

    # Print all of the input parameters to an excel sheet to be read in later
    with open(os.path.join(dst), 'a') as f:
        f.write('TOTAL_DEPTH,%s\n' %rainfall_total)
        f.write('DURATION,%s\n' %duration)

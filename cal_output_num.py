import os

dir_path = 'SynthTextData/results_bin2'
count = 0
for dir_1 in os.listdir(dir_path):
    for dir_2 in os.listdir('{}/{}'.format(dir_path, dir_1)):
        count += len(os.listdir('{}/{}/{}'.format(dir_path, dir_1, dir_2)))
print(count)

import shutil
import os
from datetime import datetime


def increment_and_save():
    # Define the file path
    file_path = "./LogDir/counter.txt"

    # Open the file and read the integer
    with open(file_path, "r") as file:
        counter = int(file.read())

    # Increment the integer
    counter += 1

    # Open the file and write the new integer
    with open(file_path, "w") as file:
        file.write(str(counter))

    # Return the new integer
    return counter


def delete_content():
    # Define the directory path
    directory = "./LogDir/norm/"

    # Get all the files in the directory
    files = os.listdir(directory)

    # Delete the files
    for file in files:
        file_path = os.path.join(directory, file)
        os.remove(file_path)

def saver():
    xx=increment_and_save()
    # Get the current date and format it
    today = datetime.today().strftime('%Y-%m-%d')

    dateAndNum=today+"_"+str(xx)

    # Define the source and destination directories
    src_dir = "./LogDir/Logs/"
    dst_dir = f"./Old/{dateAndNum}/"

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Get all the files in the source directory
    files = os.listdir(src_dir)

    # Keep track of the number of files moved
    count = 0

    # Move the files
    for file in files:
        count += 1
        src_file = os.path.join(src_dir, file)
        dst_file = os.path.join(dst_dir, file)
        shutil.move(src_file, dst_file)

def combine(lastlog):
    runningNo = 0
    with open('Logdir/prenorm/Log_0.csv', 'w') as f1:
        f1.write("v1 sin,v1 cos, v2 sin,v2 cos,pos, dt-v1 (dgr pr sec), dt-v2, dt-pos (pct pr sec), act1 (raw), act2, lbl v1 (0-360), v2 lbl,  pos lbl\n")
    f1.close()
    for i in range(0, lastlog+1):
        print(i, "lognr")
        print(runningNo, "runningNo")
        with open('Logdir/Logs/Log_%s.csv' % i, 'r') as f:
            with open('Logdir/prenorm/Log_0.csv', 'a') as f1:
                for j,line in enumerate(f):
                    if j == 0:
                        continue
                    runningNo += 1
                    f1.write(line)

    f1.close()
    f.close()


def MakeTestSet(startline, stopline):
    # Define the source and destination directories
    src_dir = "./LogDir/norm/"
    dst_dir = "./LogDir/testset/"

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # filenms
    file = "Log_0.csv"
    targetFile = "Log_0.csv"


    # open norm csv file
    with open(src_dir + file, 'r') as f:
        # read the file from startline to stopline
        lines = f.readlines()[startline:stopline]
        # open testset csv file
        with open(dst_dir + targetFile, 'w') as f1:
            # write the lines to the testset csv file
            f1.writelines(lines)
        f1.close()
    f.close()

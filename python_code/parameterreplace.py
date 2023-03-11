import fileinput, sys, os
x =input("enter text to be searched : ")
y =input("enter text to be replaced : ")
directory = input("enter directory : ")
def replaceAll(file, findexp, replaceexp):
    for line in fileinput.input(file, inplace=1):
        if findexp in line:
            line = line.replace(findexp, replaceexp)
        sys.stdout.write(line)

if __name__ == '__main__':
    files = os.listdir(directory)
    for file in files:
        newfile = os.path.join(directory, file)
        replaceAll(newfile,x,y )
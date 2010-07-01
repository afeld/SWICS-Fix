import csv
import os.path
import sys

UNKNOWN_VAL = "-9999.900"

def main():
    for filename in sys.argv[1:]:
        print filename
        if os.path.isfile(filename):
            #fileReader = open('ACE_SWICS_Data_2h_2001.1.txt')

            splitRows = []
            # read the entire file into memory using the csv module
            for row in open('ACE_SWICS_Data_2h_2001.1.txt').readlines():
                splitRows.append(row.split())

            cleanRows = cleanData(splitRows)
            
            writer = csv.writer(open(filename + "-clean.csv", "wb"))
            writer.writerows(splitRows)

            #writer = open(filename + "-clean.csv", "wb")
            #for row in cleanRows:
            #    writer.write(",".join(row) + "\n")
            print "Done."
                


def cleanData(splitRows):
    # loop through rows
    for i in range(len(splitRows)):
        atBeginning = i == 0
        splitRow = splitRows[i]
        
        # loop through columns
        for j in range(len(splitRow)):
            if splitRow[j] == UNKNOWN_VAL:
                # this value is missing: find next real value in column
                
                # loop through following cells in column
                nextVal = None
                k = None
                for k in range(i+1, len(splitRows)):
                    atEnd = k == (len(splitRows) - 1)                    

                    currentVal = splitRows[k][j]
                    if currentVal != UNKNOWN_VAL:
                        # found a real value
                        nextVal = float(currentVal)
                        break
                    elif atEnd: # and not a real value
                        nextVal = prevVal

                prevVal = None
                try:
                    prevVal = float(splitRows[i-1][j])
                except ValueError:
                    # it's the first row
                    prevVal = nextVal
                except IndexError:
                    # it's the first row
                    prevVal = nextVal
                    
                numGaps = k - i + 1
                slope = (nextVal - prevVal) / numGaps

                for l in range(i, i+numGaps):
                    splitRows[l][j] = "%.3f" % (prevVal + slope)
                    prevVal += slope
    return splitRows


if __name__ == "__main__":
    main()

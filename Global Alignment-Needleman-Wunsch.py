import sys
import csv

def getMatrix(gap,s1Size,s2Size):
    
	matrix = []
 	#m = |S1| + 1, #𝑛 = |S2| + 1
	for i in range(len(s1Size) + 1):
     
		helperMatrix = []
  
		for j in range(len(s2Size) + 1):
      
			helperMatrix.append(0)
   
		matrix.append(helperMatrix)

	# Initializing the first row and first column with the gap values
			
			#Initialization Step 
			#F_0,j = d * j
			#F_i,0 = d * i
   
	for j in range(1,len(s2Size) + 1):
     
		matrix[0][j] = gap * j
  
	for i in range(1,len(s1Size) + 1):
     
		matrix[i][0] = gap * i
  
	return matrix

#fill a matrix with zeros
def initializeBackTrackingMatrix(s1Size,s2Size):

	backTrackingMatrix = []
 
	for i in range(len(s1Size) + 1):
     
		helperMatrix = []
  
		for j in range(len(s2Size) + 1):
      
			helperMatrix.append('0')
   
		backTrackingMatrix.append(helperMatrix)


	#fill the first column and row of the matrix
	for j in range(1,len(s2Size) + 1):
     
		backTrackingMatrix[0][j] = "left"
  
	for i in range(1,len(s1Size)+1):
     
		backTrackingMatrix[i][0] = "upper"
  
	backTrackingMatrix[0][0] = "first cell"
 
	return backTrackingMatrix

#Scoring matrix helper 
def getScore(S1,S2):
		if S1 == S2:
			return match #1
		else:
			return mismatch#-1


# this function puts all the scores that need to be aligned scores inside a matrix 
def getAligned(S1,S2,score):

	matrix = getMatrix(gap,S1,S2) #call and assign
 
	backTrack = initializeBackTrackingMatrix(S1,S2) #calls function 

	for i in range(1,len(S1) + 1):
    
		for j in range(1,len(S2) + 1):
      
			# get the max score 
   
			leftCell = matrix[i][j-1] + gap # adds gap penalty 
			upperCell = matrix[i-1][j] + gap # adds gap penalty 								
			diagonalCell = matrix[i-1][j-1] + getScore(S1[i-1],S2[j-1]) # Scoring matrix
   
			matrix[i][j] = max(leftCell,upperCell,diagonalCell) # get the max score
   
			#fill in the backtrack matrix
   
			if matrix[i][j] == leftCell:
       
				backTrack[i][j] = "left"
    
			elif matrix[i][j] == upperCell:
       
				backTrack[i][j] = "upper"
    
			else:
       
				backTrack[i][j] = "diagonal"
    
	return matrix,backTrack


def needlemanWunsch(S1,S2,backTrack,matrix):
    
	i = len(S1)
	j = len(S2)

	s1List = []
	s2List = []
	
 	#gets and add to lists

	while(j > 0 or i > 0): 
     
     	#S1[i-1] == S2[j-1]
		if backTrack[i][j] == "diagonal": 

			s1List.append(S1[i-1])
			s2List.append(S2[j-1])
			i -= 1
			j -= 1
   
		elif backTrack[i][j] == "left": 
      
			s1List.append('-') #add gap
			s2List.append(S2[j-1])
			j -= 1
   
		elif backTrack[i][j] == "upper":
      
			s1List.append(S1[i-1])
			s2List.append('-') #add gap
			i -= 1
   
		elif backTrack[i][j] == "first cell":
      
			break #we reach the [0,0]

	return s1List,s2List

###################################################################################

match = 1 #Reward on a match
mismatch = -1 #Penalty on a mismatch
gap = -2 #Gap penalty

S1 = ""
S2 = ""

'''
MOODLE 
'''

def main():
    
    #read the csv file to take the sequences and assign them to a variable (S1 & S2)
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                if not row[0].startswith("sequence"):
                    S1 = row[0]
                    S2 = row[1]
                    # print()
                    # calls
                    score = getScore(S1,S2)
                    matrix,backTrack = getAligned(S1, S2, score)
                    s1List,s2List = needlemanWunsch(S1, S2, backTrack, matrix, )
                    sequence_1 = ''.join(s1List[::-1])
                    sequence_2 = ''.join(s2List[::-1])
                    finalScore = matrix[-1][-1]
                    print(sequence_1, sequence_2, finalScore)
main()


'''
TEST FUERA DE MOODLE (COMENTAR EL MAIN PARA USAR)
'''

# S1 = "GATTACA"
# S2 = "GTCGACGCA"

# score = getScore(S1,S2)
# matrix,backTrack = getAligned(S1, S2, score)
# s1List,s2List = needlemanWunsch(S1, S2, backTrack, matrix, )
# sequence_1 = ''.join(s1List[::-1])
# sequence_2 = ''.join(s2List[::-1])
# finalScore = matrix[-1][-1]
# print(sequence_1, sequence_2, finalScore)


'''
Global Alignment App

https://bioboot.github.io/bimm143_W20/class-material/nw/
'''
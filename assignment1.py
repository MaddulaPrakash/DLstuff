# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BGFnoZ2Xehs-FBXsJJ_bMUH7rxont4Mv
"""
#unzip assignment data folder
!unzip Assignment1_data.zip

#1 Gets the unique words vocab
def get_unique_words(file_name, unique_set):
  with open('/content/Assignment1_data/'+file_name, encoding = "utf8",
            errors='ignore') as f:
    text = f.read()

    words = text.lower()
    words = text.split()
    words = [word.strip('.,!;()[]') for word in words]
    words = [word.replace("'s", '') for word in words]
    for word in words:
      if word not in unique_set:
        unique_set[word] = [0] * 21
        unique_set[word][int(file_name.replace('.txt',''))] = 1
      else:
        unique_set[word][int(file_name.replace('.txt',''))] += 1
    return unique_set

#iterate through assignment directory for files and get unique words and store
#them in unique set
import os
unique_set = {}
for i in os.listdir('/content/Assignment1_data/'):
  unique_set = get_unique_words(i, unique_set)



#1 Matrix A : M = 1242, N = 20

mat = [[0 for _ in range(len(os.listdir('/content/Assignment1_data/'))+1)] for 
       _ in range(len(unique_set))]

i = 0
for x in unique_set:
  mat[i][0] = x
  mat[i][1:] = unique_set[x]
  i += 1

mat

mat[0][1:] = unique_set['Bond']

#2 heat map
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
A = np.array(mat)

B = A[:,1:]
B = B.astype(float)
sum = np.sum(B,axis=1)
word_count = {}
for count,i in enumerate(list(A[:,0])):
  word_count[i] = sum[count] 
word_countword_freq = pd.DataFrame(word_count.items(),
                                   columns=['word','frequency']).sort_values(by='frequency',ascending=False)
fig, axes = plt.subplots(3,1,figsize=(8,20))
sns.barplot(ax=axes[0],x='frequency',y='word',data=word_countword_freq.head(30))

#duplicate copy of unique word set which we can use to determine term frequency 
unique_set_copy = unique_set.copy()
unique_set_copy

#3 to calculate TF IDF score, we proceed by calculating term frequency and 
#inverse doc frequency seperately and multiply them to get TF-IDF score
def termfreq(document, mat):

    #read doc
    count = 0
    with open('/content/Assignment1_data/'+ document, encoding = "utf8",
              errors='ignore') as f:
      read_words = f.read()
      count = len(read_words)
      #iterate unique list and update array with doc number 
      for word in unique_set_copy:
        unique_set_copy[word][int(document.replace('.txt','')) -1] = unique_set_copy[word][int(document.replace('.txt',''))-1] / count
    
    return unique_set_copy

for i in os.listdir('/content/Assignment1_data/'):
  tf = termfreq(i, mat)

column_list = []
for col in range(len(mat)):
    column_list.append(mat[col][0])

#calculate inverse doc frequency using log(number of doc/number of doc that contain word)
def inverse_doc_freq():
  inverse_doc = 0
  for i in os.listdir('/content/Assignment1_data/'): 
      with open('/content/Assignment1_data/'+ i, encoding = "utf8", errors='ignore') as f:
        read_inverse_doc_words = f.read()
        for word in column_list:
          if word in read_inverse_doc_words :
            inverse_doc += 1
  return np.log(20/inverse_doc)

#calculating TF-IDF score 
tf_idf_mat = [[0 for _ in range(len(os.listdir('/content/Assignment1_data/'))+1)] for _ in range(len(unique_set_copy))]

i = 0
for x in unique_set_copy:
  tf_idf_mat[i][0] = x
  tf_idf_mat[i][1:] = unique_set[x]
  i += 1

idf = inverse_doc_freq()
tf_idf_mat = [[0 for _ in range(len(tf_idf_mat[0]))] for _ in range(len(tf_idf_mat))]
for i in range(len(tf_idf_mat)):
  for j in range(1, len(tf_idf_mat[0])):
    tf_idf_mat[i][j] = tf_idf_mat[i][j] * idf

#TF-IDF Score
tf_idf_mat 

#4 cosine similarity
import math
import string
import sys

# reading the text file .This functio will return a  list of the lines of text in the file.
def read_file(filename):
	
	try:
		with open(filename, 'r', encoding = "utf8", errors='ignore') as f:
			data = f.read()
		return data
	
	except IOError:
		sys.exit()

# splitting the text lines into words translation table is a global variable
# mapping upper case to lower case and punctuation to spaces
translation_table = str.maketrans(string.punctuation+string.ascii_uppercase,
									" "*len(string.punctuation)+string.ascii_lowercase)
	
# returns a list of the words in the file
def get_words_from_line_list(text):
	
	text = text.translate(translation_table)
	word_list = text.split()
	
	return word_list


# counts frequency of each word returns a dictionary which maps the words to
# their frequency.
def count_frequency(word_list):
	
	D = {}
	
	for new_word in word_list:
		
		if new_word in D:
			D[new_word] = D[new_word] + 1
			
		else:
			D[new_word] = 1
			
	return D

# returns dictionary of (word, frequency)  pairs from the previous dictionary.
def word_frequencies_for_file(filename):
	
	line_list = read_file(filename)
	word_list = get_words_from_line_list(line_list)
	freq_mapping = count_frequency(word_list)

	return freq_mapping


# returns the dot product of two documents
def dotProduct(D1, D2):
	Sum = 0.0
	
	for key in D1:
		
		if key in D2:
			Sum += (D1[key] * D2[key])
			
	return Sum

# returns the angle in radians between document vectors
def vector_angle(D1, D2):
	numerator = dotProduct(D1, D2)
	denominator = math.sqrt(dotProduct(D1, D1)*dotProduct(D2, D2))
	
	return math.acos(numerator / denominator)


def documentSimilarity(filename_1, filename_2):

	sorted_word_list_1 = word_frequencies_for_file(filename_1)
	sorted_word_list_2 = word_frequencies_for_file(filename_2)
	return vector_angle(sorted_word_list_1, sorted_word_list_2)

similar_docs= {}
for i in os.listdir('/content/Assignment1_data/'): 
    similar_docs[i] = documentSimilarity('/content/Assignment1_data/10.txt',
                                         '/content/Assignment1_data/' + i)

for i in range(len(similar_docs)):
  similar_docs[i][i] = np.cos(similar_docs[i][1])

sorted(similar_docs.items(), key=lambda x:x[1])

#4 cosine similarity -- 06.txt, 11.txt, 08.txt are most similar to 10.txt

new_matrix_b

new_matrix_b = [[0 for _ in range(20)] for _ in range(20)]

#5 we can acheive this by intersection of two lists
# traverse the docs by two nested for loops and the read the files and 
#split the words into doci and docj respectively 
# find the intersection and assign to new matrix B
new_matrix_list = []
words = []
for i in range(1, len(new_matrix_b)+1):
  for j in range(1, len(new_matrix_b[0])+1):
    with open('/content/Assignment1_data/'+str(i)+'.txt', encoding = "utf8",
              errors='ignore') as f:
      new_matrix_list = f.read()
      words = new_matrix_list.split()
      doci = set(words)
    with open('/content/Assignment1_data/'+str(j)+'.txt', encoding = "utf8",
              errors='ignore') as f:
      new_matrix_list = f.read()
      words = new_matrix_list.split()
      docj = set(words)

    new_matrix_b[i-1][j-1] = len(doci.intersection(docj))

#5 
new_matrix_b


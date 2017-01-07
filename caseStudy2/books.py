import os
import pandas as pd
import matplotlib.pyplot as plt

def read_book(title_path):
	with open(title_path, 'r') as current_file:
		text = current_file.read()
		text = text.replace('\n', '').replace('\r', '')
	return text

def word_stats(word_counts):
	num_unique = len(word_counts)
	counts = word_counts.values()
	return (num_unique, counts)
	
def count_words(text):
	word_counts = {}
	for word in text.split(' '):
		word_counts[word] = word_counts.get(word, 0) + 1
	return word_counts

book_dir = "/Users/Admin/Desktop/workspaces/workspacePython/usingPythonForResearch/caseStudy2/Books"
stats = pd.DataFrame(columns = ("language", "author", "title", "length", "unique"))
title_num = 1
for language in os.listdir(book_dir):
	for author in os.listdir(book_dir + "/" + language):
		for title in os.listdir(book_dir + "/" + language + "/" + author):
			inputfile = book_dir + "/" + language + "/" + author + "/" + title
			print(inputfile)
			text = read_book(inputfile)
			(num_unique, counts) = word_stats(count_words(text))
			stats.loc[title_num] = language, author.capitalize(), title.replace(".txt", ""), sum(counts), num_unique
			title_num += 1

print(stats.head())
plt.figure(figsize = (10,10))
subset = stats[stats.language == 'English']
print(subset)
plt.loglog(subset.length, subset.unique, 'o', label='English', color = 'crimson')
subset = stats[stats.language == 'French']
plt.loglog(subset.length, subset.unique, 'o', label='French', color = 'forestgreen')
subset = stats[stats.language == 'German']
plt.loglog(subset.length, subset.unique, 'o', label='German', color = 'orange')
subset = stats[stats.language == 'Portuguese']
plt.loglog(subset.length, subset.unique, 'o', label='Portuguese', color = 'blueviolet')
plt.legend()
plt.xlabel('Book length')
plt.ylabel('Number of unique words')
plt.show()
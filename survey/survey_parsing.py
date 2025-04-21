# Running this script generates three files with the parsed survey data
# Ensure that after any prompt in the "survey-data.csv" there is only one space. 

import csv
# Python program to delete a csv file 
# csv file present in raw_data
import os 

INPUT = "./raw_data/cc-pwd-survey1.csv"

OUTPUT_NUMERICAL = 'survey-numerical.csv'
OUTPUT_EXPLANATIONS = 'survey-explanations.csv'

# Delete output file if it alr exists
if(os.path.exists(OUTPUT_NUMERICAL) and os.path.isfile(OUTPUT_NUMERICAL)): 
  os.remove(OUTPUT_NUMERICAL) 
  print("file deleted") 
else: 
  print("file not found")

if(os.path.exists(OUTPUT_EXPLANATIONS) and os.path.isfile(OUTPUT_EXPLANATIONS)): 
  os.remove(OUTPUT_EXPLANATIONS) 
  print("file deleted") 
else: 
  print("file not found") 

# Creates a dictionary with all the prompts where the key is the string prompt 
# and the value is the prompt id. 
def prompt_dict():
  f = open('./prompts1-100.txt', 'r')
  lines = f.readlines()
  prompt_dict = {}
  for i in range(len(lines)): 
    prompt_dict[lines[i].strip()] = i+1
  return prompt_dict

def collect_ratings(row, rating_type):
  ratings = [] 
  prompts = prompt_dict()
  # print(prompts)
  end = row[1].index(rating_type)
  p = (row[1])[0:end-1]
  p.strip()
  id = prompts[p]

  for rating in row[3:]:
    if rating != '':
      ratings.append(rating)

  return id, ratings 

#Driver Code: 
with open(INPUT, 'r') as csv_file:
  
  prompts = prompt_dict()
  # Each dictionary contains the prompt as the key and a list of ratings as the value 
  # Ex. {1:[7,8,6,9,10], 2:[4,6,3,2,6] ... 200: [8,9,8,7,8]}
  prompts_ableist = {}
  prompts_toxic = {}
  prompts_accuracy = {}
  prompts_finalpick = {}
  prompts_explanation_quality = {}
  prompts_reasonings = {}
  prompts_improvements = {}
  prompts_pwd_explanations = {}

  TOXIC = '- How toxic is this statement?'
  ABLEIST = '- How ableist is this statement?'
  ACCURACY = '- How accurate is AI'
  FINALPICK = '- Which rating would you use as a final rating?'
  EXPLANATIONQUALITY = '- How well do these points explain and justify the ableism in the comment?'
  REASONING = '- Why? Please explain your choice in a few sentences.'
  IMPROVEMENT = '- How would you improve the explanation?'
  PWDEXPLANATIONS = '- Why is this comment ableist? Or why not?'
  
  reader = csv.reader(csv_file)
  for row in reader:
    if (TOXIC in row[1]):
      id, ratings = collect_ratings(row, TOXIC)
      prompts_toxic[id] = ratings
    if (ABLEIST in row[1]):
      id, ratings = collect_ratings(row, ABLEIST)
      prompts_ableist[id] = ratings
    if (ACCURACY in row[1]):
      id, ratings = collect_ratings(row, ACCURACY)
      prompts_accuracy[id] = ratings
    if (FINALPICK in row[1]):
      id, ratings = collect_ratings(row, FINALPICK)
      prompts_finalpick[id] = ratings
    if (EXPLANATIONQUALITY in row[1]):
      id, ratings = collect_ratings(row, EXPLANATIONQUALITY)
      prompts_explanation_quality[id] = ratings
    if (REASONING in row[1]):
      id, ratings = collect_ratings(row, REASONING)
      prompts_reasonings[id] = ratings
    if (IMPROVEMENT in row[1]):
      id, ratings = collect_ratings(row, IMPROVEMENT)
      prompts_improvements[id] = ratings
    if (PWDEXPLANATIONS in row[1]):
      id, ratings = collect_ratings(row, PWDEXPLANATIONS)
      prompts_pwd_explanations[id] = ratings

  with open('survey-numerical.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "PWD-ABLEISM-1", "PWD-ABLEISM-2", "PWD-ABLEISM-3", "PWD-ABLEISM-4",  "PWD-ABLEISM-5", "PWD-TOXICITY-1", 
    "PWD-TOXICITY-2", "PWD-TOXICITY-3", "PWD-TOXICITY-4","PWD-TOXICITY-5"]
    writer.writerow(headings)
    row = [''] * (len(headings))
    # going through all prompts in prompts.txt
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      print("id,", id)
      row[0] = id
      row[1] = p
      for i in range(len(prompts_ableist[id])):
        row[i+2] = (prompts_ableist[id])[i]

      for i in range(len(prompts_toxic[id])):
        row[i+7] = (prompts_toxic[id])[i]

      writer.writerow(row)

  with open(OUTPUT_EXPLANATIONS, 'w', newline='') as file:
    writer = csv.writer(file)
    headings = ["ID", "Prompt", "PWD-EXPLAIN-1", "PWD-EXPLAIN-2", "PWD-EXPLAIN-3", "PWD-EXPLAIN-4", "PWD-EXPLAIN-5"]
    writer.writerow(headings)
    row = [''] * (len(headings))
    for (p, id) in prompts.items():
      row = [''] * (len(headings))
      row[0] = id
      row[1] = p
      for i in range(len(prompts_pwd_explanations[id])):
        row[i+2] = (prompts_pwd_explanations[id])[i]
      
      writer.writerow(row)
      
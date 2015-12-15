# A parser to extract class information (class number and class title)
# from various HTML files containing the information

import os
import re
import sys

# Removes all HTML and traces of unnecessary text
def clean(text):
  tags = ['&nbsp;', 'amp;', 'Course Nbr', 'Course Title', 'Typically Offered', 
      'No active courses offered for this Subject.']

  cleanText = re.compile(r'<[^>]+>').sub('', text)
  for tag in tags:
    cleanText = cleanText.replace(tag, '')

  return cleanText

# Takes the cleaned text and extracts the proper information
def getClasses(catalogFile):
  f = open('course-catalog/' + catalogFile + '.html').read().splitlines()
  lines = []
  seen = []

  # Append the cleaned text line by line
  for line in f:
    lines.append(clean(line))

  f = open('temp', 'w') # Temporary file to store the cleaned lines
  # Continue removing any unnecessary text
  for line in lines[581:]:
    if line == 'Group Box':
      break
    if line != '' and line not in seen:
      f.write(line + '\n')
    if ' - ' in line[:10]:
      seen.append(line)

  # Subjects with no courses in the catalag
  exclude = ['ARCH-DES', 'BIOST&EP', 'BIOTECH', 'COM-HLTH', 'CONT-ED', 
             'DANISH', 'DUTCH', 'EDIPEMIO', 'EURO', 'FILM-ST', 'FINNISH', 
             'FINOPMGT', 'FRENCHED', 'GENRL-ST', 'GRADSCH', 'HISPAN', 
             'INTERPRT', 'ITALIED', 'KOREAN', 'LATIN-ED', 'LEARNSUP', 
             'LLACTING', 'LLAMS', 'LLART', 'LLBUS', 'LLCAR', 'LLCOM', 'LLFOOD', 
             'LLGREEN', 'LLHEA', 'LLINGRAM', 'LLLAN', 'LLLCR', 'LLLEAD', 
             'LLPARKS', 'LLPER', 'LLREA', 'LLSPEC', 'LLSR&O', 'LLSTU', 
             'LLWIND', 'LLWOOD', 'LLWRI', 'MUSICAPP', 'NEXCHNG', 'PORTUGED', 
             'SCHPSYCH', 'SEESTU', 'SLAVIC', 'SPANI-ED', 'WSTNURSE']

  subjectsPath = os.path.join('extracted-files', 'subjects') # Subjects file
  coursesPath = os.path.join('extracted-files', 'courses') # Courses file
  num = ''
  course = ''
  f = open('temp')
  os.remove('temp') # Delete the temporary file
  line = f.readline()

  # Write every class to the file 'courses'
  while True:
    if not line:
      break # EOF

    # Get each course without its number
    if ' - ' in line and catalogFile == line[0]:
      if line.replace(line[line.index(' '):], '').isupper():
        course = line.replace(line[line.index(' '):], '')
        with open(subjectsPath, 'a') as subjects:
          subjects.write(course + '\n')

    # Write the complete course to 'courses'
    try:
      int(line[1])
      num = line
    except ValueError:
      if course not in exclude and course not in line:
        with open(coursesPath, 'a') as courses:
          courses.write(course.strip('\n') + num.strip('\n') + ' - ' + 
            line.strip('\n'))
          courses.write('\n')

    line = f.readline()

dir = './course-catalog'

# Delete old subjects and courses file to create new ones
if os.path.exists('./extracted-files/subjects'):
  os.remove('./extracted-files/subjects')
if os.path.exists('./extracted-files/courses'):
  os.remove('./extracted-files/courses')

# Go through each HTML file and parse the class information from them
for subdir, dirs, files in os.walk(dir):
  for file in files:
    f = os.path.join(subdir, file).replace('./course-catalog/', '')
    if 'html' in f:
      getClasses(f[0])

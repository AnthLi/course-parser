# A parser to extract class information (class number - and class title)
# from various SPIRE HTML files containing the classes

import os
import re
import sys

# Removes all HTML tags and traces of unnecessary text
def clean(text):
  tags = ["&nbsp;", "amp;", "Course Nbr", "Course Title", "Typically Offered", 
      "No active courses offered for this Subject."]

  cleanText = re.compile(r"<[^>]+>").sub("", text)
  for tag in tags:
    cleanText = cleanText.replace(tag, "")

  return cleanText

# Takes the cleaned text and extracts the proper information
def getClasses(catalogFile):
  f = open("course-catalog/" + catalogFile + ".html").read().splitlines()
  lines = []
  seen = [] # List of seen classes to prevent duplicates
  
  for line in f:
    lines.append(clean(line)) # Append each line of clean text

  f = open("temp", "w") # Temporary file to store the cleaned lines
  # Continue removing any unnecessary text
  for line in lines[581:]:
    if line == "Group Box":
      break
    if line != "" and line not in seen:
      f.write(line + "\n")
    if " - " in line[:10]:
      seen.append(line)

  # Subjects with no courses offered for the current semester
  exclude = ["ARCH-DES", "BIOST&EP", "BIOTECH", "COM-HLTH", "CONT-ED", 
             "DANISH", "DUTCH", "EDIPEMIO", "EURO", "FILM-ST", "FINNISH", 
             "FINOPMGT", "FRENCHED", "GENRL-ST", "GRADSCH", "HISPAN", 
             "INTERPRT", "ITALIED", "KOREAN", "LATIN-ED", "LEARNSUP", 
             "LLACTING", "LLAMS", "LLART", "LLBUS", "LLCAR", "LLCOM", "LLFOOD", 
             "LLGREEN", "LLHEA", "LLINGRAM", "LLLAN", "LLLCR", "LLLEAD", 
             "LLPARKS", "LLPER", "LLREA", "LLSPEC", "LLSR&O", "LLSTU", 
             "LLWIND", "LLWOOD", "LLWRI", "MUSICAPP", "NEXCHNG", "PORTUGED", 
             "SCHPSYCH", "SEESTU", "SLAVIC", "SPANI-ED", "WSTNURSE"]

  sFile = os.path.join("extracted-files", "subjects") # "subjects" file
  cFile = os.path.join("extracted-files", "courses") # "courses" file
  subject = ""
  num = ""
  f = open("temp")
  os.remove("temp") # Delete the temporary file
  line = f.readline()

  # Write every class to the file "courses"
  while True:
    if not line:
      break # EOF

    # Write each subject to "subjects"
    if " - " in line and catalogFile == line[0]:
      if line.replace(line[line.index(" "):], "").isupper():
        subject = line.replace(line[line.index(" "):], "")
        with open(sFile, "a") as subjects:
          subjects.write(course + "\n") # Write the subject to a separate file

    # Write each complete course number to "courses"
    try:
      int(line[1])
      num = line
    except ValueError:
      if subject not in exclude and subject not in line:
        with open(cFile, "a") as courses:
          # Write the course with its subject, number, and name
          courses.write(course.strip("\n") + num.strip("\n") + " - " + 
            line.strip("\n"))
          courses.write("\n")

    line = f.readline()

dir = "./course-catalog"

# Delete old "subjects" and "courses" files to create new ones
if os.path.exists("./extracted-files/subjects"):
  os.remove("./extracted-files/subjects")
if os.path.exists("./extracted-files/courses"):
  os.remove("./extracted-files/courses")

# Go through each HTML file and parse the class information from them
for subdir, dirs, files in os.walk(dir):
  for file in files:
    f = os.path.join(subdir, file).replace("./course-catalog/", "")
    if "html" in f:
      getClasses(f[0])

import re


def split_into_lines(sentence, max_chars):
   words = sentence.split()
   lines = []
   line = ""

   for word in words:
       # If adding the word would make the line too long, start a new line
       if len(line) + len(word) > max_chars:
           lines.append(line)
           line = ""

       # Add the word to the line
       line += word + " "

   # Append the last line if it's not empty
   if line:
       lines.append(line)

   return lines

def count_lines(s):
   return s.count('\n') + 1

def white_space_independent_compare(s1, s2):
    return re.sub(r'\s+', ' ', s1) == re.sub(r'\s+', ' ', s2)

def edit_distance(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0 for _ in range(n +  1)] for _ in range(m +  1)]

    for i in range(m +  1):
        dp[i][0] = i
    for j in range(n +  1):
        dp[0][j] = j

    for i in range(1, m +  1):
        for j in range(1, n +  1):
            if str1[i -  1] == str2[j -  1]:
                dp[i][j] = dp[i -  1][j -  1]
            else:
                dp[i][j] =  1 + min(dp[i][j -  1], dp[i -  1][j], dp[i -  1][j -  1])

    return dp[m][n]


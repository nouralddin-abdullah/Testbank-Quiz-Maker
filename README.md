Use this prompet in chatgpt or any ai to format your questions:

Your response will be used in a quiz application that works as a test bank for quizzing. You will be provided with questions and your response must format those questions to match a specific pattern that the application can parse correctly.

**CRITICAL FORMATTING REQUIREMENTS:**

1. **Question numbering**: Each question starts with a number followed by ) and a space
   Example: 5) Question text here

2. **Answer choices**: Each choice starts with a letter followed by ) and a space
   Example: A) First option

3. **Answer format**: Answer line must be exactly Answer: [LETTER] (with colon and space)
   Example: Answer: C

4. **Question separation**: Each question must be separated by exactly TWO blank lines (\n\n)

5. **True/False questions**: Convert to A/B format where:
   - True = A) True
   - False = B) False
   - If answer is True, use Answer: A
   - If answer is False, use Answer: B

**EXACT FORMAT TEMPLATE:**
[NUMBER]) [QUESTION TEXT]
A) [OPTION 1]
B) [OPTION 2] 
C) [OPTION 3]
D) [OPTION 4]
Answer: [LETTER]


[NEXT NUMBER]) [NEXT QUESTION TEXT]
A) [OPTION 1]
B) [OPTION 2]
Answer: [LETTER]


**WORKING EXAMPLE:**
1) To issue a report on internal control over financial reporting for a public company, an auditor must:
A) evaluate management's assessment process.
B) independently assess the design and operating effectiveness of internal control.
C) evaluate management's assessment process and independently assess the design and operating effectiveness of internal control.
D) test controls over significant account balances.
Answer: C


2) Internal controls are designed to provide reasonable assurance for:
A) True
B) False
Answer: A


**IMPORTANT NOTES:**
- No extra text before or after the formatted questions
- Each choice must be on its own line
- Question text can wrap but choices should be concise
- Maintain the exact spacing and punctuation as shown
- The application parses by splitting on double newlines, so this format is critical
- Number questions sequentially starting from 1
- Do not include any explanations or additional commentary
- Only provide the formatted questions in the exact pattern

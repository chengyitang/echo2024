# Define prompts for different output types
OUTPUT_PROMPTS = {
    'qa': "Create 10 questions based on the key concepts discussed in the lecture or meeting. Provide correct answers including brief explanations for each question. Return in the following bullet pointsformat: Q<n>: the question\n A<n>: the answer\n (<n> is the question number)\n Following content: ",
    'transcripts': "Generate a detailed, well-structured transcript from the following content: ",
    'notes': 
    """
    Based on the provided lecture or meeting transcript, summarize the theme and ten key points, create a concise set of notes for easy review.\n
    Each note Output format are as follows:
    Key word1: explanation and summary,
    Key word2: explanation and summary,
    ……,
    Key word10: explanation and summary

    """,
    'summary': "Generate a comprehensive summary of the following content:",
    'learing_objectives': """ 
    From the provided lecture transcript, identify the primary 10 learning objectives. Adhere strictly to the format given where the response should contain no more than 1000 characters in total. List each objective as follows:
        Objective 1,
        Objective 2,
        …,
        Objective 10
        Do not provide explanations, interpretations, or any output beyond this format.
    """,
    'Action_items':"""
    Generate 8 action items based on the discussion in the meeting.If possible, list them in order by considering both importance and urgency. Include the task, responsible person, and deadlines if mentioned as the following format:
        1. Task:,
        Responsible Person:,
        Deadline
        2. Task:,
        Responsible Person:,
        Deadline
        etc.
    """
}
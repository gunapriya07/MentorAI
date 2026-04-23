def get_prompt(mode, user_input):
    
    if mode == "Explain":
        return f"""
Explain the following topic in simple terms for a student:

{user_input}

Provide:
1. Simple explanation
2. Example
3. Real-world use
"""

    elif mode == "Summarize":
        return f"""
Summarize the following content in clear bullet points:

{user_input}
"""

    elif mode == "Quiz":
        return f"""
Generate 5 quiz questions based on:

{user_input}

Provide only questions.
"""

    else:
        return user_input
from google import genai
from config.gemini_config import GEMINI_API_KEY

def generate_suggestions(missing_skills, job_title="the role"):
    if not missing_skills:
        return "Your resume already matches the job requirements very well."

    fallback = [f"- Consider learning {skill} through online documentation or hands-on projects."for skill in missing_skills]
    fallback_text = "AI suggestions unavailable. Basic suggestions:\n" + "\n".join(fallback)

    try:
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not loaded")

        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
        You are an expert Career Coach and Technical Recruiter.

        The candidate is missing these skills for the role of '{job_title}':
        {", ".join(missing_skills)}

        Provide a VERY brief, structured improvement plan.

        For each skill include:
        • Actionable step (project idea)
        • Topics to study
        • Learning resources (Coursera, Udemy, edX, MDN, official docs)

        Use bullet points.
        Keep the tone professional and encouraging.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        print("Gemini Error:", e)
        return fallback_text



# def generate_suggestions(missing_skills, job_title="the role"):
#     # Fallback (GOOD PRACTICE – keep this)
#     if not missing_skills:
#         return "Your resume already matches the job requirements very well."

#     fallback = [
#         f"- Consider learning or adding a project related to {skill}."
#         for skill in missing_skills
#     ]

#     fallback_text = (
#         "AI suggestions are temporarily unavailable.\n"
#         "Rule-based improvement suggestions:\n" +
#         "\n".join(fallback)
#     )

#     try:
#         if not GEMINI_API_KEY:
#             raise ValueError("Gemini API key not loaded")

#         client = genai.Client(api_key=GEMINI_API_KEY)

#         prompt = f"""
#             You are an AI career assistant.

#             The candidate is missing the following skills for the {job_title}:
#             {", ".join(missing_skills)}

#             Provide 3 clear, actionable suggestions to improve the resume.
#             Keep it concise and practical.
#             """

#         response = client.models.generate_content(
#             model="models/gemini-2.5-flash",
#             contents=prompt
#         )

#         return response.text.strip()

#     except Exception as e:
#         print("Gemini Error:", e)
#         return fallback_text
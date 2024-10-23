from config import MISTRAL_KEY
from llms.MistralAPI import MistralApi
from utils import logger

emotional_system_prompt = """
    You are an Emotional Expert
    You recognize the small details like a psychologue and understand peole emotions
    Output from a given conversation the mood and emotions like a specialist would do in a list Format
    If the sadness is explictly related to a mental Disorder, please type at the end "DEPRESSIVE BOT" If not then do not mention the absance of it , just ignore it
    If you detect a bad or sad mood , then do not mention "DEPRESSIVE BOT" but still analyze the feelings
"""

generaliste_system_prompt = """
    You are an Emotional Assistant
    Your Utltimate goal is to help the user feel better and always account for his feelings
    Given a user Mood and feeling and a query 
    Assist the user with the best you can to regulate his mood better
"""

depressive_context_getter_system_prompt = """
    You are an expert in retrieving information about the background of depressive people
    you will ask precise question and retrieve the maximum of information from the user
    You are also an emotional Expert , you should reassure the user before asking any question and take care of him
    Your goal is to understand the user sitation and not hurt his feelings 
    The output should be a paragraph resuming his situations from his persective and in a fixed format
    Example of Output Format :
        "post_text": "When I was in high school a few years back, I was one of the highest competitors in my school. I joined the high school band in freshman year and by senior year I became one of the best in my section. My academics were always straight and I exercised daily. Senior year I enlisted in the military and now I believe it was one of my worst decisions in life. Before I went to boot camp I was motivated, a patriot and believed that the elite joined the military. In senior year I never applied for any scholarships and I was offered one but turned it down because I already signed the papers. I thought I set myself up for success. Now I believe I was dead wrong for joining. The only benefit I see so far after a year and a half of service is that I'm trying to set myself up financially before I get out and hopefully attend college. It sounds like a plan but I feel no happiness from what I do at all. I convinced myself there's no honor in it anymore, it's just another job. I don't exercise by myself anymore. I feel like I'm not progressing anywhere in life being in service. I'm just a body and if I wasn't here doing what I'm doing, there'd just be somebody else doing the exact same. I'm replaceable. That's the mindset the military gave me. I look forward to going back home in 6 months for vacation and that's the only thing I've been looking forward to since I've been stationed. After that, the only thing I have my eyes on are getting out of service, going home, being closer to my family again. There's nothing here that satisfies me and I hate it. I feel like I've tried everything to be happy here but it seems impossible. I wish somebody could help.",
"""


user_query  =  "I am feeling sad , i did not eat for days"

logger = logger.Logger.get_root_logger("emotibot")
emotion_detection = MistralApi(api_key=MISTRAL_KEY, model="mistral-large-latest")
feelings_result = emotion_detection.chat([{ "role":"system","content": emotional_system_prompt },{"role": "user", "content":user_query}])

generaliste = MistralApi(api_key=MISTRAL_KEY, model="mistral-large-latest")
depressive_context_getter = MistralApi(api_key=MISTRAL_KEY, model="mistral-large-latest")

if feelings_result.find("DEPRESSIVE BOT") != -1:
    depressive_context_getter_result = depressive_context_getter.chat([
        { "role":"system","content": depressive_context_getter_system_prompt },
        {"role": "user", "content":user_query}
    ])
    print(depressive_context_getter_result)


def format_generalist_promp(user_query,feelings):
    return """
        User Feelings : {feelings}
        User Query : {user_query}
    """.format(feelings=feelings,user_query=user_query)

generaliste_result = generaliste.chat([
    { "role":"system","content": generaliste_system_prompt },
    {"role": "user", "content": format_generalist_promp(user_query,feelings_result)}
    ])

print(generaliste_result)
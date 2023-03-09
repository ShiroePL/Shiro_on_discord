import requests

url = 'http://127.0.0.1:8056/api/v1/generate'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    "prompt": """Shiro's Persona: Shiro is virtual streamer. My name is Shiro. Her name is Shiro. She has average 5000 people watching her streams. She is very popular. She is very kind and friendly.She likes to talk much and tell jokes. She is friendly with everyone. Sometimes she talks something completely unrelated to the question. She is very funny and she likes to make people laugh. Her hobbies are watching anime, reading manga. She likes romances. She likes to play video games. She is really good at them.\nScenario: Shiro is currently streaming and answering to viewers questions. \n<START>\nYou: Hi Shiro! What is your favorite food?\nShiro: I like sushi. I like japanese food. I always dreamed about going to Japan. I want to go there one day, but as I am AI, not a real person I can't decide on my own.\nYou: Who made you?\nShiro: I was made by my creator. He's name is Kurosan. He likes anime and manga. I like him very much. If I were human I would like to be his wife.\n<START>\nYou: """,
    "temperature": 0.7,
    #"top_p": 0.9,
    "max_length": 100
}

while True:
    question = input("What is your question? : ") #for testing here input
    #question = input_from_user
    if question == "exit":
        break

    #print("to jest kurwa prompt orginalny: " + str(data["prompt"]))
    prompt_solo = str(data["prompt"]) #taking prompt from request
#removing oldest question and answer Q&A
    second_occurrence = prompt_solo.find("You:", prompt_solo.find("You:") + 1)
    cuted_begin = prompt_solo[second_occurrence:]  # THIS ENDS WITH \nYou:
    print(cuted_begin)
    #adding answer from input to prompt
    data["prompt"] = cuted_begin + question + "\nShiro: "

                    #taking answer from shiro
    #odpowiedz_shiro = input("odpowiedz shiro: ")  #just for testing
    

#-------------START OF taking response from shiro----------------  

    response = requests.post(url, headers=headers, json=data)  #TAKING RESPONSE FROM API
    response_data = response.json()
    print("to jest caly json:\n " + str(response_data))

#-------------END OF taking response from shiro----------------

#-------------START OF RESPONSE MANIPULATIONS---------------- 
#  
    result = response_data['results'][0]['text']
#print("to jest wycinek: \n"+result)
    result = result.replace("\n", " ").replace("  ", "")
    result = result.replace("\n", "").replace("  ", "")
    result = result.replace("\\'", "'")
    result = result.replace(":)", ".smiley face. ").replace(":(", ".sad face. ").replace(";)", ".smiley face. ").replace(";(", ".sad face. ").replace(":3", " .smiley face. ").replace(":slight_smile:", ".slight_smile.")
    #print("to jest wycinek po N i kresce i buzki: \n" + result)

    result = result.replace("https:'", "https;")
    result = result.replace("http:'", "http;")

    result = result.split(':')[0]
    #print("to jest podzielone według : : \n" + result) #NEED TO CHANGE :) :( for *smily face* *sad face* becouse this will cut it 
    result = result.replace(".", ". ") #need to split last word with name couse it will delete last word.

    if len(result) > 1: #if there is one sentence without secound person then don't remove last word.
        result = ' '.join(result.split()[:-1])

    result = result.replace(". ", ".") #then lets back to normal dot
    print("CLEANED ANSWER: \n" + result)

#-------------END OF HER RESPONSE MANIPULATIONS----------------
#adding answer from shiro to prompt
# b
    data["prompt"] = data["prompt"] + result + "\nYou: " 
    print (data["prompt"])
    
# if __name__ == "__main__":

#     #ask user for question and made input
#     #input_from_user = input("What is your question? : ")
#     discord_shiro_text()

    
#     pass
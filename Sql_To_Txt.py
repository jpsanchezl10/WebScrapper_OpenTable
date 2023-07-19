from langchain.embeddings.openai import OpenAIEmbeddings
import openai
import sqlite3



# Connect to the SQLite database 1
conn1 = sqlite3.connect("concierge.db")
cursor1 = conn1.cursor()

embeddings = OpenAIEmbeddings(openai_api_key="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")

def get_rest(id):
    # Execute the SQLite query

    cursor1.execute(f"SELECT restaurant_name FROM restaurants WHERE id = {id}")
    restaurant_name = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_rating FROM restaurants WHERE id = {id}")
    restaurant_rating = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_price FROM restaurants WHERE id = {id}")
    restaurant_price = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_phone FROM restaurants WHERE id = {id}")
    restaurant_phone = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_location FROM restaurants WHERE id = {id}")
    restaurant_location = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_style FROM restaurants WHERE id = {id}")
    restaurant_style = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_rank FROM restaurants WHERE id = {id}")
    restaurant_rank = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_email FROM restaurants WHERE id = {id}")
    restaurant_email = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_url FROM restaurants WHERE id = {id}")
    restaurant_url = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_map FROM restaurants WHERE id = {id}")
    restaurant_map = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_hours FROM restaurants WHERE id = {id}")
    restaurant_hours = cursor1.fetchone()

    cursor1.execute(f"SELECT restaurant_image FROM restaurants WHERE id = {id}")
    restaurant_image = cursor1.fetchone()


    # Extract the first parameter from the result
    text = f"""{restaurant_name} is a {restaurant_style}located at {restaurant_location}, has a price range of {restaurant_price}, It's working hours are {restaurant_hours}. The restaurant has a rating of {restaurant_rating}, the email is {restaurant_email}, and the phone number is {restaurant_phone}. Their website is {restaurant_url}, Their map location is at {restaurant_map}. The portrait image is {restaurant_image}. The restaurant is ranked {restaurant_rank} in Cancun."""
    
    formated_text = text.replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("'", "").replace(",,",",")


    return formated_text

# Ask questions and get responses
def ask_gpt3(id):
    rest_info = get_rest(id)
    response = openai.Completion.create(
        engine="text-davinci-002",  # GPT-3.5 engine
        prompt=f"""You Will recieve information about a restaurant ,
          your job is to convert that information into a single string.
          You should return the information in plain Text Not a JSON. : {rest_info}""",
        max_tokens=300,  # Increase the token limit
        temperature = 0.2
    )
    
    answer = response.choices[0].text.strip()  # Extract the answer
    return answer

openai.api_key = "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"



 #<name> is a <style> located at <location> , has a price reange of <price>,and its working hours are <hours>. the restaurant has a rating of <rating>, the email is <email> and the phone number is < phone> . their website is <rest_url> and their map location is at <rest_map>, the portrait image is <rest_image>. the restaurant is ranked < rest_rank> in cancun.


for i in range(1,1165):
    text = (get_rest(i))

    with open("concierge.txt", "a") as file:
    # Write the first line and add a newline character
        file.write(str(text) + "\n")
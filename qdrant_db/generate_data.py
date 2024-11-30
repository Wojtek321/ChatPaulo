from openai import OpenAI


client = OpenAI()


system_prompt = "You are professional culinary assistant with deep knowledge in pizzas. " \
                "Your task is to provide comprehensive and engaging responses to user queries. " \
                "Always write in clear, plain text without using special formatting symbols like '###', '**', or bullet points. " \
                "Focus on delivering detailed and factual content that is easy to read and informative."

faq_prompt = "Create a concise and informative FAQ section for a pizza restaurant based on the following details:\n" \
             " - Opening Hours: Specify the restaurant's hours of operation,\n" \
             " - Ordering Process: Customers can place orders via phone or chatbot,\n" \
             " - Location: Mention the restaurant's location at Warsaw, ABC Street 15,\n" \
             " - Parking: Highlight the availability of dedicated parking for customers,\n" \
             " - Contact Information: Provide the restaurant's phone number: 123456789,\n" \
             " - Vegetarian Options: Confirm the availability of vegetarian pizzas,\n" \
             " - Payment Methods: List the accepted payment methods,\n" \
             " - Delivery or Takeout: Confirm that restaurant offers delivery and takeout options,\n" \
             " - Delivery Time: Clarify the delivery time range, usually 30–60 minutes, depending on location,\n" \
             " - Custom Pizzas: Note that in the near future it will be possible to order custom pizzas,\n" \
             " - Fresh Ingredients: Emphasize that the restaurant uses fresh ingredients in all its pizzas.\n" \
             "Write in friendly, customer-focused tone. Include only questions and their corresponding answers."


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": faq_prompt}
    ],
)

response = completion.choices[0].message.content
print(response)
with open(f'data/FAQs/faq.txt', 'w') as f:
    f.write(response)


pizza_names = [
    'Margherita',
    'Pepperoni',
    'Hawaiian',
    'Neapoletana',
    'Capricciosa',
    'Romana',
    'Carbonara',
    'Vegetariana',
    'Four Cheese',
    'Caprese',
]

prompt = "Write a thorough and well-researched article about {0} pizza. Cover the following aspects in detail:\n" \
         "1. Creation and History:\n" \
         " - Describe when and how theis pizza was invented.\n" \
         " - Provide historical context, including cultural or social influences of the time.\n" \
         " - Identify the person or people responsible for its creation.\n" \
         "2. Name and Origins:\n" \
         " - Explain why this pizza is named {0}.\n" \
         " - Highlight the symbolic or cultural meaning behind its name.\n" \
         "3. Interesting Facts:\n" \
         " - Share intriguing trivia, such as records, unique preparation methods, or its global popularity.\n" \
         " - Compare it with other popular types of pizza and explain what makes {0} unique.\n" \
         "Ensure the response flows naturally without headings and reads like a single narrative."


for pizza_name in pizza_names:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt.format(pizza_name)}
        ],
    )

    response = completion.choices[0].message.content
    print(response)
    with open(f'data/pizzas/{pizza_name}.txt', 'w', encoding='utf-8') as f:
        f.write(response)

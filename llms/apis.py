import os
from os.path import join, dirname
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from .models import Conversation
load_dotenv()

key = os.getenv("HUGGINGFACE_TOKEN")
messages=[
            {
                "role": "user",
                "content": "How many 'G's in 'huggingface'?"
            }
        ]


def calling(conv_id, message):
    llm = "deepseek-ai/DeepSeek-R1-0528"
    try:
        conv_id = int(conv_id)
        conversation = Conversation.objects.get(id=conv_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid conversation ID")
    except Conversation.DoesNotExist:
        raise ValueError("Conversation not found")

    db_messages = conversation.messages.order_by('timestamp')
    messages = [
        {
            "role": "user" if msg.sender == "user" else "assistant",
            "content": msg.content
        }
        for msg in db_messages
    ]
    messages.append({
        "role": "user",
        "content": message
    })
    client = InferenceClient(api_key=key)
    completion_deepseek = client.chat.completions.create(
        model=llm,
        messages=messages
    )

    return {"deepseek": completion_deepseek.choices[0].message}

import gradio as gr
from graph import graph


config = {
    'configurable': {
        'thread_id': "1"
    }
}


def inference(message, history):
    partial_message = ""
    output = graph.stream({'messages': ('user', message)}, config, stream_mode="messages")

    for chunk, metadata in output:
        if 'assistant' in metadata['langgraph_node']:
            if isinstance(chunk.content, str):
                partial_message += chunk.content
            elif isinstance(chunk.content, list):
                for item in chunk.content:
                    if isinstance(item, dict) and 'text' in item:
                        partial_message += item['text']

            yield partial_message


gr.ChatInterface(
    inference,
    type='messages',
    textbox=gr.Textbox(placeholder="Send message to Paulo", container=False, scale=7, submit_btn=True, stop_btn=True),
    description="Interact with Paulo to explore the menu, check ingredients, and place an order.",
    title="Paulo - Pizzeria Assistant",
    examples=["Who are you?", "What can i eat?", "I want to place an order", "Tell ma about Neapoletana"],
).queue().launch()

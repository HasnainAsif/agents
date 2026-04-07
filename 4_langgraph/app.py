
# Steps to runs this app:
# 1. Checkout to agents environment of uv in terminal where langgraph is installed
        # uv venv agents - for creating environment
        # source agents/bin/activate - for activating environment
# 2. Command to run the app:
        # Switch to the 4_langgraph directory in terminal
        # uv run app.py

# Link of LangSmith log. I stopped app manually because agent got stuck in infinite loop between worker and tools.
        # https://smith.langchain.com/o/2a0576f1-39e8-4db2-aa62-e1858bb87b7c/projects/p/67f94808-f17b-4208-a7d9-4ee9bddca5d7/r/8888eceb-4f28-456c-8563-e02c09649338?trace_id=8888eceb-4f28-456c-8563-e02c09649338&start_time=2025-11-03T14:10:15.327146

# Link to LangSmith log and image reference of UI: (SUCCESSFULLY RUN)
        # Image Ref: ./assets/image6.png
        # Log Link: https://smith.langchain.com/o/2a0576f1-39e8-4db2-aa62-e1858bb87b7c/projects/p/67f94808-f17b-4208-a7d9-4ee9bddca5d7/r/aa20044b-7814-46a5-86b3-0951c448ba84?trace_id=aa20044b-7814-46a5-86b3-0951c448ba84&start_time=2025-11-03T14:51:17.006972


import gradio as gr
from sidekick import Sidekick

async def setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick


async def process_message(sidekick, message, success_criteria, history):
    results = await sidekick.run_superstep(message, success_criteria, history)
    return results, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick


def free_resources(sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Personal Co-Worker")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success critiera?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    ui.load(setup, [], [sidekick])
    message.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])


ui.launch(inbrowser=True)

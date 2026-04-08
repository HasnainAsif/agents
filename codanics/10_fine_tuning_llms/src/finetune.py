import json
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType

# Load and format dataset
with open("data/alpaca_data.json") as f:
    raw_data = json.load(f)

# Formatting data for causal language modeling
def format_alpaca(example):
    return {
        "text": f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
    }

data = [format_alpaca(d) for d in raw_data]
dataset = Dataset.from_list(data) # Creating a HuggingFace Dataset

# Loading Tokenizer and Model
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" # a causal language model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Converts text → tokens (input_ids)
# Pads all samples to exactly 512 tokens
# Truncates longer samples
def tokenize(sample):
    return tokenizer(sample["text"], padding="max_length", truncation=True, max_length=512)

tokenized = dataset.map(tokenize) # Now each sample has: input_ids, attention_mask
tokenized.set_format(type="torch", columns=["input_ids", "attention_mask"]) # Converts data into PyTorch tensors

# LoRA config - Parameter-Efficient Fine-Tuning
lora_config = LoraConfig(
    r=8, # Rank of the LoRA layers
    lora_alpha=32, # Scaling factor for the LoRA layers
    lora_dropout=0.1, # Dropout rate for the LoRA layers
    bias="none", # Bias handling
    task_type=TaskType.CAUSAL_LM) # Task type for causal language modeling
model = get_peft_model(model, lora_config)

# Training configuration
args = TrainingArguments(
    output_dir="lora-tinyllama",
    per_device_train_batch_size=4, # batch size is 4 samples per step
    num_train_epochs=3, # dataset will be trained 3 times
    save_strategy="epoch", # Model checkpoint saved after each epoch
    logging_steps=10,
    fp16=False, # Set to True if using a GPU with FP16 support
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()
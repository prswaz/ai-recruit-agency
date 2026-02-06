from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer,
    pipeline,
    set_seed
)
from datasets import Dataset
import json
import os
import torch

# --- Paths ---
data_path = "/Users/parsaalizade/Desktop/ai-recruiter-agency/agents/data-set.json"
out_dir = "/Users/parsaalizade/Desktop/ai-recruiter-agency/results"
save_dir = "/Users/parsaalizade/Desktop/ai-recruiter-agency/fine-tuning-results"

# --- Model and Tokenizer ---
model_name = "gpt2"  # Using GPT-2 model
tokenizer = AutoTokenizer.from_pretrained(model_name)

# If there's no pad token, make one
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load the GPT-2 model
model = AutoModelForCausalLM.from_pretrained(model_name)

# --- Load Data ---
with open(data_path, "r") as f:
    raw = json.load(f)



def build_text(ex):
    return (
        "[INST] Extract structured JSON with keys: "
        "technical_skills, years_of_experience, education(level, field), "
        "experience_level, key_achievements, domain_expertise, certifications. "
        "Return ONLY valid JSON. Resume:\n"
        f"{ex['input']} [/INST]\n"
        f"{json.dumps(ex['output'], ensure_ascii=False)}"
    )

texts = [build_text(item) for item in raw]
dataset = Dataset.from_dict({"text": texts})

# --- Tokenizer ---
max_len = 128  # Reduce max length for better memory handling
def tok_fn(batch):
    enc = tokenizer(
        batch["text"],
        truncation=True,
        max_length=max_len,
        padding="max_length",
    )
    enc["labels"] = enc["input_ids"].copy()  # Labels are same as input_ids for causal LM
    return enc

tokenized = dataset.map(tok_fn, batched=True, remove_columns=["text"])

# --- Collator ---
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# --- Training Arguments ---
training_args = TrainingArguments(
    output_dir=out_dir,
    overwrite_output_dir=True,
    learning_rate=5e-5,
    per_device_train_batch_size=1,  # Keep batch size small to avoid memory overflow
    num_train_epochs=5,  # Start small to verify it works
    weight_decay=0.01,
    logging_dir=os.path.join(out_dir, "logs"),
    logging_steps=10,
    save_strategy="steps",  # Save the model every N steps
    save_steps=200,  # Adjust this to your needs
    save_total_limit=2,
    fp16=False,  # Disable mixed-precision training (MPS doesn't support it well)
    bf16=False,  # No BF16 support needed
    load_best_model_at_end=False,  # We are skipping evaluation for now
    gradient_accumulation_steps=8,  # Accumulate gradients over multiple steps
)

# --- Trainer --- 
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

print("Starting training (no eval)...")
trainer.train()

print("Saving...")
trainer.save_model(save_dir)
tokenizer.save_pretrained(save_dir)
print("Done. Saved to:", save_dir)

# --- Text Generation with the Model ---
# Set up the pipeline for text generation using GPT-2
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Set the random seed for reproducibility
set_seed(42)

# Generate text with the model
input_text = "Hello, I'm a language model,"
generated_text = generator(input_text, max_length=30, num_return_sequences=5)

# Display generated text
for i, generated in enumerate(generated_text):
    print(f"Generated {i + 1}: {generated['generated_text']}")

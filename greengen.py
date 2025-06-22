import os
from fastapi import FastAPI, HTTPException, Query
from typing import List
from pydantic import BaseModel
from openai import AzureOpenAI

# ------------------ Azure Configuration ------------------
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "<your-api-key>")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOimport os
from fastapi import FastAPI, HTTPException, Query
from typing import List
from pydantic import BaseModel
from openai import AzureOpenAI

# ------------------ Azure Configuration ------------------
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "<your-api-key>")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# ------------------ FastAPI Setup ------------------
app = FastAPI(title="Virtual Green Assistant API")

class ProductRequest(BaseModel):
    product: str

class TipRequest(BaseModel):
    recent_items: List[str]

class RecommendRequest(BaseModel):
    user_id: str
    history: List[str]

# ------------------ Helper Function ------------------
def ask_ai(prompt: str) -> dict:
    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a sustainability assistant helping users reduce carbon and plastic footprints. Always respond in valid JSON format. 1 eco swap gets 100 eco coins and 1 challenge gets 200 eco coins."},
                {"role": "user", "content": prompt}
            ],
        )
        return eval(response.choices[0].message.content.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

# ------------------ API Routes ------------------

@app.post("/eco-swap")
def eco_swap(req: ProductRequest):
    prompt = (
        f'A user is considering buying "{req.product}". Suggest a greener alternative.\n'
        'Respond in JSON with: eco_alternative, co2_saved (kg), plastic_saved (g), ai_reasoning, confidence_score, amazon_link.'
    )
    return ask_ai(prompt)

@app.get("/user-impact")
def user_impact(user_id: str = Query(...)):
    prompt = (
        f'User "{user_id}" made 6 eco-swaps and 2 challenges.\n'
        'Return JSON: total_swaps, total_challenges, co2_saved (kg), plastic_avoided (kg), badges, eco_coins.'
    )
    return ask_ai(prompt)

@app.post("/generate-tip")
def generate_tip(req: TipRequest):
    prompt = (
        f"User recently bought: {req.recent_items}.\n"
        "Give one upcycling tip in JSON: tip, category."
    )
    return ask_ai(prompt)

@app.post("/recommend-next")
def recommend_next(req: RecommendRequest):
    prompt = (
        f"Based on past swaps {req.history}, suggest the next eco-action.\n"
        "Return JSON: recommended_action, reason, estimated_co2_saved (kg), estimated_plastic_saved (g)."
    )
    return ask_ai(prompt)
INT
)

# ------------------ FastAPI Setup ------------------
app = FastAPI(title="Virtual Green Assistant API")

class ProductRequest(BaseModel):
    product: str

class TipRequest(BaseModel):
    recent_items: List[str]

class RecommendRequest(BaseModel):
    user_id: str
    history: List[str]

# ------------------ Helper Function ------------------
def ask_ai(prompt: str) -> dict:
    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a sustainability assistant helping users reduce carbon and plastic footprints. Always respond in valid JSON format. 1 eco swap gets 100 eco coins and 1 challenge gets 200 eco coins."},
                {"role": "user", "content": prompt}
            ],
        )
        return eval(response.choices[0].message.content.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

# ------------------ API Routes ------------------

@app.post("/eco-swap")
def eco_swap(req: ProductRequest):
    prompt = (
        f'A user is considering buying "{req.product}". Suggest a greener alternative.\n'
        'Respond in JSON with: eco_alternative, co2_saved (kg), plastic_saved (g), ai_reasoning, confidence_score, amazon_link.'
    )
    return ask_ai(prompt)

@app.get("/user-impact")
def user_impact(user_id: str = Query(...)):
    prompt = (
        f'User "{user_id}" made 6 eco-swaps and 2 challenges.\n'
        'Return JSON: total_swaps, total_challenges, co2_saved (kg), plastic_avoided (kg), badges, eco_coins.'
    )
    return ask_ai(prompt)

@app.post("/generate-tip")
def generate_tip(req: TipRequest):
    prompt = (
        f"User recently bought: {req.recent_items}.\n"
        "Give one upcycling tip in JSON: tip, category."
    )
    return ask_ai(prompt)

@app.post("/recommend-next")
def recommend_next(req: RecommendRequest):
    prompt = (
        f"Based on past swaps {req.history}, suggest the next eco-action.\n"
        "Return JSON: recommended_action, reason, estimated_co2_saved (kg), estimated_plastic_saved (g)."
    )
    return ask_ai(prompt)

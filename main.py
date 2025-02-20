from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import plotly.graph_objs as go
import uvicorn

app = FastAPI()

# In-memory storage (use a database for persistence)
data_store = {}

class DataItem(BaseModel):
    category: str
    value: float

@app.post("/send_data/")
def receive_data(item: DataItem):
    """Receive data and store it"""
    data_store[item.category] = item.value
    return {"message": "Data received", "data": data_store}

@app.get("/")
def get_chart():
    """Generate a bar chart from stored data"""
    if not data_store:
        raise HTTPException(status_code=404, detail="No data available")

    fig = go.Figure([go.Bar(x=list(data_store.keys()), y=list(data_store.values()))])
    fig.update_layout(title="Live Data Bar Chart", xaxis_title="Category", yaxis_title="Value")
    return fig.to_html(full_html=False)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

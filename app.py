import sys
import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List


from src.candiate_selection_process.main import SelectionFlow
from src.candiate_selection_process.job_description import JOB_DESCRIPTION


app = FastAPI(
    title="Candidate Selection Flow API",
    description="API for the AI-powered candidate selection and email generation flow.",
    version="1.0.0"
)
@app.get("/health")
async def health_check():
    """
    Health check endpoint to ensure the API is running.
    """
    return {"status": "ok", "message": "Candidate Selection API is running!"}


@app.get("/kickoff")
async def kickoff_candidate_selection():
    """
    Starts the candidate selection and email generation process.
    This endpoint directly triggers the flow without any input.
    """
    try:
        selection_flow = SelectionFlow()


        selection_flow.kickoff()

        if not selection_flow.state.top_candiates:
            raise HTTPException(status_code=500, detail="No top candidates selected. Flow might have encountered an issue or no candidates met the criteria.")

        return selection_flow.state.top_candiates

    except Exception as e:
        print(f"An error occurred during kickoff: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/job_description")
async def get_job_description():
    """
    Returns the current job description used by the selection flow.
    """
    return {"job_description": JOB_DESCRIPTION}



if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
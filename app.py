import sys
import os
from pathlib import Path
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException
from typing import List
from src.candidate_selection.main import SelectionFlow
from src.candidate_selection.job_description import JOB_DESCRIPTION

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
        def run_selection_flow():
            selection_flow = SelectionFlow()
            selection_flow.kickoff()
            return selection_flow.state.top_candidates

        loop = asyncio.get_event_loop()
        top_candidates = await loop.run_in_executor(None, run_selection_flow)

        if not top_candidates:
            raise HTTPException(status_code=500, detail="No top candidates selected. Flow might have encountered an issue or no candidates met the criteria.")

        return [candidate.dict() if hasattr(candidate, 'dict') else candidate.__dict__ for candidate in top_candidates]

    except Exception as e:
        print(f"An error occurred during kickoff: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/job_description")
async def get_job_description():
    """
    Returns the current job description used by the selection flow.
    """
    return {"job_description": JOB_DESCRIPTION}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
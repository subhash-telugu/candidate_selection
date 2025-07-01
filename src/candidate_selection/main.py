from pathlib import Path
import csv
import json
import asyncio
from crewai.flow.flow import Flow,start,listen
from pydantic import BaseModel
from typing import List
from src.candidate_selection.models import candidate,candidateScore,scoredcandidate
from src.candidate_selection.crews.candidate_scoring.crew import ScoreCrew
from src.candidate_selection.crews.emails_to_candidates.crew import HrResponse
from src.candidate_selection.job_description import JOB_DESCRIPTION
from src.candidate_selection.utils.candidateUtils import combined_scored_and_candidated




class SelectionState(BaseModel):
    candidates:List[candidate]=[]
    candidate_scores:List[candidateScore]=[]
    top_candidates:List[scoredcandidate]=[]
    provided_feedback:str=''
    feedback:str=''


class SelectionFlow(Flow[SelectionState]):

    @start()
    def load_candidates(self):
        csv_file=Path(__file__).parent/'leads.csv'
        data=[]    
        with open(csv_file, mode="r", newline="", encoding="utf-8") as f:
            rows=csv.DictReader(f)
            for row in rows:
                data.append(candidate(**row))
        print('candidates data has been loaded')        
        self.state.candidates=data
        return self.state.candidates
    


    
    @listen(load_candidates)
    async def candidate_scoring(self):
        tasks=[]  
        candidates=self.state.candidates
        async def single_candidate_evaluation(candidate:candidate):
            
            result=await (ScoreCrew().crew().kickoff_async(inputs={
                'candidate_id':candidate.id,
                'name':candidate.name,
                'bio':candidate.bio,
                'job_description':JOB_DESCRIPTION,
                "additional_instructions": self.state.feedback,
            }))
            # print(result)
            # JSonStr=str(result)
            # python_format=json.loads(JSonStr)
            self.state.candidate_scores.append(result.pydantic)
        for candidate in candidates:
            print(f'the candidate {candidate.name} evaluation started')
            task=asyncio.create_task(single_candidate_evaluation(candidate))
            tasks.append(task)
        print('all the candidate score have been gathered')    
        candidates_scores=await asyncio.gather(*tasks)   
        print('length of candidates score',len(candidates_scores))

        return  'done with the candidate scores'
    


    @listen(candidate_scoring)
    def top_candidate_selection(self):
        combined_scores=combined_scored_and_candidated(self.state.candidate_scores,self.state.candidates)
        l=sorted(combined_scores,key=lambda c:c.score,reverse=True)
        self.state.top_candidates=l[0:3]

    @listen(top_candidate_selection) 
    async def email_generation(self):
        import re
        from pathlib import Path

        print('writing and saving email to all candidates')
        top_candidate_ids = {
        candidate.id for candidate in self.state.top_candidates
        }

        tasks = []

        output_dir = Path(__file__).parent.parent / "email_responses"
        print("output_dir:", output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        async def write_email(candidate):

            proceed_with_candidate = candidate.id in top_candidate_ids
            
            result = await (
                HrResponse()
                .response_crew()
                .kickoff_async(
                    inputs={
                        "candidate_id": candidate.id,
                        "name": candidate.name,
                        "bio": candidate.bio,
                        "proceed_with_candidate": proceed_with_candidate,
                    }
                )
            )

            safe_name = re.sub(r"[^a-zA-Z0-9_\- ]", "", candidate.name)
            filename = f"{safe_name}.txt"
            print("Filename:", filename)
            
            file_path = output_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result.raw)
           
            return f"Email saved for {candidate.name} as {filename}"
        
        for candidate in self.state.top_candidates:
            task = asyncio.create_task(write_email(candidate))
            tasks.append(task)
  
        email_results = await asyncio.gather(*tasks)

        print("\nAll emails have been written and saved to 'email_responses' folder.")
        for message in email_results:
            print(message)

           

# def kickoff():

#     lead_score_flow = SelectionFlow()

#     lead_score_flow.kickoff()




# if __name__ == "__main__":
#     kickoff()
   

     



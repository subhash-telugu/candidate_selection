from src.candidate_selection_process.models import candidate,candidateScore,scoredcandidate
import csv

def combined_scored_and_candidated(candidate_scores:list[candidateScore],candidates:list[candidate]) ->list[scoredcandidate]:
    d={}
    for each in candidate_scores:
        d[each.id]=each
    scored_candidates_details=[]
    for candidate in candidates:
        candidate_score=d.get(candidate.id)
        if candidate_score.score:
            scored_candidates_details.append(scoredcandidate(id=candidate.id,
                                    name=candidate.name,
                                    email=candidate.email,
                                    bio=candidate.bio,
                                    skills=candidate.skills,
                                    score=candidate_score.score,
                                    reason=candidate_score.reason
                                    ))



    with open('leads_scores.csv','w') as f:
        writer=csv.writer(f)
        writer.writerow(['id','name','email','score'])
        for candidate in scored_candidates_details:
            writer.writerow([candidate.id,candidate.name,candidate.email,candidate.score])



    print('score have be combined with candidates')
    return scored_candidates_details
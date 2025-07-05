🧠 Candidate Selection AI
This project automates the candidate evaluation and communication process using a multi-agent system powered by CrewAI. It streamlines the hiring workflow by programmatically scoring candidates against job descriptions, identifying top profiles, and generating personalized email responses.

🚀 Features
Automated Candidate Scoring: Evaluates candidate resumes/bios against a job description and assigns a compatibility score.

Top Candidate Identification: Ranks and selects the most suitable candidates based on scores.

Personalized Email Generation: Crafts customized email responses for selected and rejected candidates.

Asynchronous Processing: Uses asyncio for efficient, parallel evaluation and communication.

Modular Agent Design: Leverages CrewAI for a composable, maintainable, agent-based architecture.

⚙️ How It Works
The core logic resides in SelectionFlow (main.py) and orchestrates the following steps:

load_candidates
Loads candidate data from src/candidate_selection/leads.csv.

candidate_scoring
Uses ScoreCrew to asynchronously score each candidate’s bio against a job description (job_description.py).

top_candidate_selection
Sorts candidates based on scores and selects the top 3.

email_generation
Generates personalized emails via HrResponse crew and saves them to email_responses/.

🗂 Project Structure
bash
Copy
Edit
.
├── src/
│   ├── candidate_selection/
│   │   ├── crews/
│   │   │   ├── candidate_scoring/
│   │   │   │   ├── config/
│   │   │   │   ├── __init__.py
│   │   │   │   └── crew.py
│   │   │   └── emails_to_candidates/
│   │   │       ├── config/
│   │   │       ├── __init__.py
│   │   │       └── crew.py
│   │   ├── tools/
│   │   ├── utils/
│   │   │   └── candidateUtils.py
│   │   ├── web/
│   │   ├── __init__.py
│   │   ├── job_description.py
│   │   ├── leads.csv
│   │   ├── main.py
│   │   └── models.py
├── email_responses/          # Output emails generated
├── .env                      # API keys (excluded from version control)
├── .gitignore
├── Dockerfile
└── README.md
🧑‍💻 Getting Started
✅ Prerequisites
Python 3.9+

Docker (optional, for containerization)

📦 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/subhash-telugu/candidate_selection.git
cd candidate_selection
Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install crewai pydantic
You may also need:

bash
Copy
Edit
pip install openai  # or google-generativeai, depending on your LLM
🔐 Set Up API Keys
Create a .env file in the project root:

bash
Copy
Edit
GOOGLE_API_KEY="your_google_api_key_here"
# or for OpenAI:
# OPENAI_API_KEY="your_openai_key_here"
⚠️ .env is already included in .gitignore to protect secrets.

▶️ Running the Application
Prepare candidate data:
Add candidates in src/candidate_selection/leads.csv using columns like id, name, bio.

Set your job description:
Update JOB_DESCRIPTION in src/candidate_selection/job_description.py.

Run the application:

bash
Copy
Edit
python src/candidate_selection/main.py
Ensure kickoff() is invoked in main.py.

📤 Output
Generated email responses are saved in the email_responses/ folder.

Console will show evaluation progress and selected candidates.

🔧 Customization
What You Want to Change	How to Do It
Candidate Data	Edit leads.csv
Job Description	Modify job_description.py
Scoring or Email Logic	Update crew.py in respective crews/ subfolders
Number of Top Candidates	Change the slice in top_candidate_selection (e.g. l[0:5])
LLM Model/Provider	Update agent config/ or .env as per provider’s API

🧰 Technologies Used
Python: Core language

CrewAI: Multi-agent orchestration

Pydantic: Data validation

asyncio: For async workflows

LLM APIs: Google Gemini, OpenAI, etc.

📦 Docker Support (Optional)
A Dockerfile is included for containerized deployment. Example build/run:

bash
Copy
Edit
docker build -t candidate-ai .
docker run --env-file .env candidate-ai
📬 Contact
Feel free to contribute or raise issues on the GitHub Repository.
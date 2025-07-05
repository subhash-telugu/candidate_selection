# Candidate Selection AI

This project automates the candidate evaluation and communication process using a multi-agent system powered by **CrewAI**. It streamlines the hiring workflow by programmatically scoring candidates against job descriptions, identifying top profiles, and generating personalized email responses.

---

## Features

* **Automated Candidate Scoring:** Evaluates candidate resumes/bios against a given job description to assign a compatibility score.
* **Top Candidate Identification:** Ranks and selects the most suitable candidates based on their scores.
* **Personalized Email Generation:** Crafts customized email responses for both selected and unselected candidates.
* **Asynchronous Processing:** Leverages `asyncio` for efficient, parallel processing of candidate evaluations and email generation.
* **Modular Agent Design:** Utilizes CrewAI to create specialized agents for each step of the selection process.

---

## How It Works

The core of this application is a **CrewAI Flow** (`SelectionFlow`) defined in `main.py` that orchestrates several key steps:

1.  **`load_candidates`**: Reads candidate data from the `leads.csv` file located in the `src/candidate_selection/` directory.
2.  **`candidate_scoring`**: Asynchronously evaluates each candidate's bio against the `JOB_DESCRIPTION` (defined in `src/candidate_selection/job_description.py`) using a dedicated `ScoreCrew` to generate a `candidateScore`.
3.  **`top_candidate_selection`**: Sorts the scored candidates and identifies the top 3 based on their compatibility scores.
4.  **`email_generation`**: Asynchronously generates and saves personalized email responses for all candidates (acceptance for top candidates, rejection for others) using an `HrResponse` crew. Emails are saved as `.txt` files in the `email_responses/` directory.

---

## Project Structure
```bash
.
├── src/
│   ├── candidate_selection/
│   │   ├── crews/
│   │   │   ├── candidate_scoring/
│   │   │   │   ├── config/
│   │   │   │   ├── init.py
│   │   │   │   └── crew.py
│   │   │   └── emails_to_candidates/
│   │   │       ├── config/
│   │   │       ├── init.py
│   │   │       └── crew.py
│   │   ├── tools/
│   │   ├── utils/
│   │   │   └── candidateUtils.py
│   │   ├── web/
│   │   ├── init.py
│   │   ├── job_description.py
│   │   ├── leads.csv
│   │   ├── main.py
│   │   └── models.py
├── email_responses/ (created after running)
├── .env
├── .gitignore
├── Dockerfile
└── README.md
```

---

## Getting Started

### Prerequisites

* Python 3.9+
* Docker (optional, for containerized deployment)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/subhash-telugu/candidate_selection.git](https://github.com/subhash-telugu/candidate_selection.git)
    cd candidate_selection
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    (You will need a `requirements.txt` file in your project. For now, here are the likely main dependencies.)

    ```bash
    pip install crewai pydantic
    # You might also need specific LLM client libraries (e.g., openai, google-generativeai)
    # depending on your crew implementations and .env configuration.
    ```

4.  **Set up your API Key:**
    Create a `.env` file in the root directory of the project (if it doesn't exist) and add your LLM API key. For example:

    ```
   
    # Google Gemini:
    # GOOGLE_API_KEY="your_google_api_key_here"
    ```
    *Important: Make sure to never commit your `.env` file to version control (it's already listed in `.gitignore`, which is good practice!).*

### Running the Application

1.  **Prepare `leads.csv`:**
    Ensure your `leads.csv` file is located at `src/candidate_selection/leads.csv` and contains candidate data with columns corresponding to your `candidate` Pydantic model (e.g., `id`, `name`, `bio`).

2.  **Define `JOB_DESCRIPTION`:**
    Update the `JOB_DESCRIPTION` variable in `src/candidate_selection/job_description.py` with the actual job description you want to use for candidate evaluation.

3.  **Run the main script:**

    ```bash
    python src/candidate_selection/main.py
    ```
    *(Note: Ensure the `kickoff()` method call within `main.py` is uncommented or called appropriately for direct execution of the flow.)*

---

## Output

After successful execution, you will find generated email responses in the `email_responses/` directory, with filenames corresponding to the candidate's name. The console will also display progress messages about candidate evaluation and email saving.

---

## Customization

* **Candidate Data:** Modify `src/candidate_selection/leads.csv` to include your specific candidate information.
* **Job Description:** Update `src/candidate_selection/job_description.py` for different roles.
* **Agent Logic:** Adjust the `crew.py` files within `src/candidate_selection/crews/` (e.g., `candidate_scoring/crew.py`, `emails_to_candidates/crew.py`) to refine the scoring and email generation logic of the AI agents.
* **Number of Top Candidates:** Change `l[0:3]` in the `top_candidate_selection` method in `main.py` to select a different number of top candidates.
* **LLM Model:** Configure your CrewAI agents to use different LLM models by adjusting the `config` files within the `crews` subdirectories or by setting appropriate environment variables.

---

## Technologies Used

* **Python**
* **CrewAI**: For multi-agent orchestration and workflow management.
* **Pydantic**: For robust data validation and settings management.
* **`asyncio`**: For efficient asynchronous operations, allowing parallel processing.

---

## Contributing

Feel free to fork this repository, open issues, or submit pull requests.

---
# TalentScout AI Hiring Assistant

## Project Overview
The TalentScout AI Hiring Assistant is an intelligent chatbot designed to streamline the initial screening process for technology candidates at a fictional recruitment agency, TalentScout. Built using Python and Streamlit, the chatbot leverages a large language model (LLM) via the Ollama framework to collect candidate information, generate tailored technical questions based on the candidate's tech stack, and maintain a coherent conversation flow. The project demonstrates proficiency in prompt engineering, UI development, and data handling while adhering to data privacy best practices.

Key features include:
- **User-Friendly Interface**: A clean and intuitive Streamlit-based UI for seamless candidate interaction.
- **Information Gathering**: Collects essential details such as full name, email, phone, experience, desired position, location, and tech stack.
- **Technical Question Generation**: Dynamically generates 3 relevant technical questions per technology in the candidate's declared tech stack.
- **Context-Aware Conversations**: Maintains conversation context for a natural and professional user experience.
- **Data Privacy**: Handles candidate data securely using simulated in-memory storage.
- **Graceful Exit**: Allows candidates to end the conversation using keywords like "exit" or "quit".

## Installation Instructions
To set up and run the TalentScout AI Hiring Assistant locally, follow these steps:

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- Ollama server (for running the LLM locally)
- A compatible LLM model (e.g., `llama3`) pulled via Ollama

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/talentscout-ai-hiring-assistant.git
   cd talentscout-ai-hiring-assistant
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` file includes:
   ```
   streamlit==1.29.0
   langchain-ollama==0.2.0
   ```

4. **Set Up Ollama**:
   - Install Ollama: Follow instructions at [Ollama's official site](https://ollama.ai/).
   - Pull the `llama3` model:
     ```bash
     ollama pull llama3
     ```
   - Start the Ollama server:
     ```bash
     ollama serve
     ```
   Ensure the server is running at `http://localhost:11434`.

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
   The application will open in your default browser at `http://localhost:8501`.

## Usage Guide
1. **Start Screening**: Click the "Start Screening" button to begin the process.
2. **Provide Information**: Enter your full name, email, phone number, years of experience, desired position, current location, and tech stack when prompted.
3. **Answer Technical Questions**: For each technology in your tech stack, answer 3 tailored technical questions.
4. **Review Summary**: View a summary of your provided information and answers at the end.
5. **End Conversation**: Type "exit", "quit", "bye", "stop", or "end conversation" at any time to conclude the session.
6. **Next Steps**: The chatbot will thank you and inform you that a recruiter will follow up.

## Technical Details
- **Programming Language**: Python 3.8+
- **Frontend Framework**: Streamlit for a responsive and interactive UI.
- **LLM Integration**:
  - **Model**: `llama3` via Ollama (locally hosted).
  - **Library**: `langchain-ollama` for interfacing with the LLM.
- **Architecture**:
  - **State Management**: Streamlit's `session_state` manages conversation phase, candidate data, and answers.
  - **Modular Functions**: Includes utilities for input validation, prompt generation, question extraction, and data summarization.
  - **Prompt Engineering**: Custom prompts ensure precise information gathering and relevant question generation.
- **Data Handling**: Candidate data is stored in-memory using `session_state` to simulate a backend while ensuring privacy compliance.
- **Error Handling**: Includes validation for email/phone inputs and fallback responses for LLM connection issues.

## Prompt Design
Prompts are crafted to achieve two primary objectives:

1. **Information Gathering**:
   - **Prompt Structure**: System instructions define the chatbot's role as a TalentScout hiring assistant, followed by a concise request for a specific field (e.g., "full name"). Context is provided via a summary of already collected data to maintain coherence.
   - **Example**:
     ```plaintext
     You are an AI hiring assistant for 'TalentScout'. Your goal is to collect essential candidate information. The candidate is currently providing their details for a tech role screening. They have already provided: name: John Doe. Politely ask the candidate for their 'email address'. Keep it concise and professional.
     ```
   - **Outcome**: Ensures polite, context-aware, and focused interactions.

2. **Technical Question Generation**:
   - **Prompt Structure**: Specifies the technology, candidate's experience level, and desired output (3 numbered questions without answers or filler). Emphasizes relevance, challenge, and coverage of fundamentals, practical application, and best practices.
   - **Example**:
     ```plaintext
     Generate exactly 3 unique, challenging, and relevant technical interview questions for a candidate with 5 years of experience in Python. Questions should cover fundamentals, practical application, problem-solving, and best practices relevant to this technology. Do not include answers, explanations, or any conversational filler. Just the numbered list of questions.
     ```
   - **Outcome**: Produces targeted questions that assess candidate proficiency effectively.

3. **Optimization**:
   - **Clarity**: Prompts are concise to minimize ambiguity.
   - **Diversity**: Handles various tech stacks by dynamically inserting technology names.
   - **Temperature Setting**: Set to 0.0 for deterministic responses during information gathering and question generation.

## Challenges & Solutions
1. **Challenge**: Ensuring the LLM generates exactly 3 questions without extraneous text.
   - **Solution**: Used strict prompt instructions and regex-based extraction (`re.findall`) to parse numbered questions, with a fallback to line splitting for robustness.

2. **Challenge**: Maintaining conversation context across multiple phases.
   - **Solution**: Leveraged Streamlit's `session_state` to track phase, candidate data, and answers. Summarized collected data in prompts to provide context to the LLM.

3. **Challenge**: Handling invalid user inputs (e.g., incorrect email formats).
   - **Solution**: Implemented regex-based validation for email and phone inputs, with user-friendly warning messages to prompt corrections.

4. **Challenge**: Simulating data storage while ensuring privacy compliance.
   - **Solution**: Used in-memory storage via `session_state` instead of a persistent database, ensuring no sensitive data is saved.

5. **Challenge**: Ensuring a smooth UI experience with Streamlit's rerun mechanism.
   - **Solution**: Structured the code to minimize unnecessary reruns by using forms and conditional navigation, improving responsiveness.

## Future Enhancements (Optional Features Implemented)
- **Fallback Mechanism**: Provides meaningful responses for unexpected inputs or LLM errors (e.g., "Sorry, I'm having trouble connecting to my AI brain right now. Please try again later.").
- **Exit Handling**: Supports multiple exit keywords for user convenience.

## Bonus Points Consideration
- **Potential Cloud Deployment**: The app is designed to be compatible with cloud platforms like AWS or GCP, requiring only environment setup and Ollama hosting.
- **UI Styling**: Streamlit's default styling is clean, with potential for custom CSS enhancements.
- **Performance**: Modular code and efficient state management ensure prompt responses.

## Repository Structure
```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Excludes unnecessary files
```

## Notes
- Ensure the Ollama server is running before launching the app.
- The chatbot uses simulated data and does not persist any information, aligning with GDPR-compliant practices.
- For a live demo, a video walkthrough can be provided via a tool like Loom (not included in this submission).

## Contact
For any questions or feedback, please reach out via the Career Portal submission or email (provided during screening).

Thank you for reviewing my submission!
import streamlit as st
from langchain_ollama.llms import OllamaLLM
import re
from datetime import datetime

MODEL_NAME = "llama3"
TECH_Q_PER_SKILL = 3
OLLAMA_BASE_URL = "http://localhost:11434"

def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def validate_phone(phone):
    return re.match(r'^\+?\d{7,15}$', phone)

def get_llama_response(prompt_text, system_instruction="", temperature=0.0):
    llm = OllamaLLM(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=temperature)
    full_prompt = f"System: {system_instruction}\nUser: {prompt_text}" if system_instruction else prompt_text
    try:
        response = llm.invoke(full_prompt)
        return response.strip()
    except Exception as e:
        st.error(f"Error communicating with Ollama: {e}. Please ensure Ollama server is running and '{MODEL_NAME}' model is pulled.")
        return "Sorry, I'm having trouble connecting to my AI brain right now. Please try again later."

def generate_info_gathering_prompt(field_name, collected_info_summary=""):
    return (
        f"You are an AI hiring assistant for 'TalentScout'. Your goal is to collect essential candidate information. "
        f"The candidate is currently providing their details for a tech role screening. "
        f"They have already provided: {collected_info_summary if collected_info_summary else 'No information yet.'}\n\n"
        f"Politely ask the candidate for their '{field_name}'. Keep it concise and professional."
    )

def generate_tech_questions_prompt(tech, years_exp):
    return (
        f"Generate exactly {TECH_Q_PER_SKILL} unique, challenging, and relevant technical interview questions for a candidate "
        f"with {years_exp} years of experience in {tech}. "
        "Questions should cover fundamentals, practical application, problem-solving, and best practices relevant to this technology. "
        "Do not include answers, explanations, or any conversational filler. Just the numbered list of questions."
    )

def summarize_candidate_data(candidate_data):
    summary = (
        f"--- Candidate Screening Summary ---\n\n"
        f"- **Full Name:** {candidate_data.get('name', 'N/A')}\n"
        f"- **Email:** {candidate_data.get('email', 'N/A')}\n"
        f"- **Phone:** {candidate_data.get('phone', 'N/A')}\n"
        f"- **Years of Experience:** {candidate_data.get('exp', 'N/A')}\n"
        f"- **Desired Position(s):** {candidate_data.get('position', 'N/A')}\n"
        f"- **Current Location:** {candidate_data.get('location', 'N/A')}\n"
        f"- **Declared Tech Stack:** {', '.join(candidate_data.get('tech_stack', ['N/A']))}\n\n"
        f"--- End Summary ---"
    )
    return summary

def extract_questions(generated_questions):
    # Use regex to extract lines starting with a number and dot/parenthesis
    matches = re.findall(r'(?:^\d+[\.\)]\s*)(.*)', generated_questions, flags=re.MULTILINE)
    if matches:
        return [q.strip() for q in matches]
    # Fallback: split by lines if regex fails
    return [q.strip() for q in generated_questions.split('\n') if q.strip()]

def init_session_state():
    if "phase" not in st.session_state:
        st.session_state.phase = "greeting"
        st.session_state.candidate_data = {
            "name": "",
            "email": "",
            "phone": "",
            "exp": "",
            "position": "",
            "location": "",
            "tech_stack": [],
        }
        st.session_state.tech_questions_generated = {}
        st.session_state.current_tech_index = 0
        st.session_state.current_question_index = 0
        st.session_state.answers = {}  # {tech: [answer1, answer2, ...]}
        st.session_state.exit_requested = False
        st.session_state.start_time = datetime.now()

init_session_state()

def move_to_next_phase():
    order = [
        "greeting", "collect_name", "collect_email", "collect_phone",
        "collect_exp", "collect_position", "collect_location", "collect_tech_stack",
        "ask_questions", "summary", "end"
    ]
    idx = order.index(st.session_state.phase)
    st.session_state.phase = order[min(idx + 1, len(order) - 1)]

def handle_exit_command():
    st.session_state.exit_requested = True
    st.session_state.phase = "end"
    st.success("Conversation ended. Thank you for your time!")

def check_for_exit(user_input_text):
    if user_input_text and user_input_text.strip().lower() in {"exit", "quit", "bye", "stop", "end conversation"}:
        handle_exit_command()
        return True
    return False

def show_exit_input():
    user_exit_input = st.text_input(
        "Type 'exit' anytime to end the conversation:",
        key=f"exit_input_{st.session_state.phase}"
    )
    if check_for_exit(user_exit_input):
        st.stop()

st.set_page_config(page_title="TalentScout AI Hiring Assistant", page_icon="🤖")

st.title("🤖 TalentScout AI Hiring Assistant")
st.caption("Your intelligent, privacy-first recruiter for tech roles.")

collected_summary_for_llm = ", ".join([f"{k}: {v}" for k, v in st.session_state.candidate_data.items() if v and k != "tech_stack"])

# --- Greeting Phase ---
if st.session_state.phase == "greeting":
    st.info("👋 Hello! I'm TalentScout, your AI-powered hiring assistant. I'll guide you through a quick screening process for tech roles.")
    if st.button("Start Screening"):
        move_to_next_phase()
        st.rerun()

# --- Collect Name ---
elif st.session_state.phase == "collect_name":
    llm_prompt_text = get_llama_response(generate_info_gathering_prompt("full name", collected_summary_for_llm))
    st.write(llm_prompt_text)
    with st.form(key=f"form_{st.session_state.phase}"):
        name = st.text_input("Full Name:", key=f"name_input_{st.session_state.phase}")
        submitted = st.form_submit_button("Next")
        if submitted and name:
            st.session_state.candidate_data["name"] = name.strip()
            move_to_next_phase()
            st.rerun()

# --- Collect Email ---
elif st.session_state.phase == "collect_email":
    llm_prompt_text = get_llama_response(generate_info_gathering_prompt("email address", collected_summary_for_llm))
    st.write(llm_prompt_text)
    with st.form(key=f"form_{st.session_state.phase}"):
        email = st.text_input("Email Address:", key=f"email_input_{st.session_state.phase}")
        submitted = st.form_submit_button("Next")
        if submitted and email:
            if validate_email(email):
                st.session_state.candidate_data["email"] = email.strip()
                move_to_next_phase()
                st.rerun()
            else:
                st.warning("That doesn't look like a valid email. Please try again.")

# --- Collect Phone ---
elif st.session_state.phase == "collect_phone":
    llm_prompt_text = get_llama_response(generate_info_gathering_prompt("phone number (including country code)", collected_summary_for_llm))
    st.write(llm_prompt_text)
    with st.form(key=f"form_{st.session_state.phase}"):
        phone = st.text_input("Phone Number (e.g., +1234567890):", key=f"phone_input_{st.session_state.phase}")
        submitted = st.form_submit_button("Next")
        if submitted and phone:
            if validate_phone(phone):
                st.session_state.candidate_data["phone"] = phone.strip()
                move_to_next_phase()
                st.rerun()
            else:
                st.warning("That doesn't look like a valid phone number. Please include country code if applicable.")

# --- Collect Experience ---
elif st.session_state.phase == "collect_exp":
    llm_prompt_text = get_llama_response(generate_info_gathering_prompt("years of professional experience", collected_summary_for_llm))
    st.write(llm_prompt_text)
    with st.form(key=f"form_{st.session_state.phase}"):
        exp = st.text_input("Years of Experience (e.g., 5):", key=f"exp_input_{st.session_state.phase}")
        submitted = st.form_submit_button("Next")
        if submitted and exp:
            if exp.isdigit() and 0 <= int(exp) < 60:
                st.session_state.candidate_data["exp"] = exp.strip()
                move_to_next_phase()
                st.rerun()
            else:
                st.warning("Please enter a valid number for years of experience.")

# --- Collect Desired Position ---
elif st.session_state.phase == "collect_position":
    llm_prompt_text = get_llama_response(generate_info_gathering_prompt("desired position(s)", collected_summary_for_llm))
    st.write(llm_prompt_text)
    with st.form(key=f"form_{st.session_state.phase}"):
        position = st.text_input("Desired Position(s):", key=f"position_input_{st.session_state.phase}")
        submitted = st.form_submit_button("Next")
        if submitted and position:
            st.session_state.candidate_data["position"] = position.strip()
            move_to_next_phase()
            st.rerun()

# --- Collect Current Location ---
elif st.session_state.phase == "collect_location":
    llm_prompt_text = get_llama_response(generate_info_gathering_prompt("current location (city, country)", collected_summary_for_llm))
    st.write(llm_prompt_text)
    with st.form(key=f"form_{st.session_state.phase}"):
        location = st.text_input("Current Location (e.g., London, UK):", key=f"location_input_{st.session_state.phase}")
        submitted = st.form_submit_button("Next")
        if submitted and location:
            st.session_state.candidate_data["location"] = location.strip()
            move_to_next_phase()
            st.rerun()

# --- Collect Tech Stack ---
elif st.session_state.phase == "collect_tech_stack":
    llm_prompt_text = get_llama_response(generate_info_gathering_prompt("tech stack (programming languages, frameworks, tools, etc.)", collected_summary_for_llm))
    st.write(llm_prompt_text)
    with st.form(key=f"form_{st.session_state.phase}"):
        tech_stack_input = st.text_input("Tech Stack (comma-separated, e.g., Python, React, AWS, Docker):", key=f"tech_stack_input_{st.session_state.phase}")
        submitted = st.form_submit_button("Next")
        if submitted and tech_stack_input:
            tech_list = [t.strip() for t in tech_stack_input.split(",") if t.strip()]
            if tech_list:
                st.session_state.candidate_data["tech_stack"] = tech_list
                st.session_state.tech_questions_generated = {}
                st.session_state.current_tech_index = 0
                st.session_state.current_question_index = 0
                st.session_state.answers = {tech: [""] * TECH_Q_PER_SKILL for tech in tech_list}
                move_to_next_phase()
                st.rerun()
            else:
                st.warning("Please list at least one technology in your tech stack.")

# --- Ask Technical Questions ---
elif st.session_state.phase == "ask_questions":
    techs = st.session_state.candidate_data["tech_stack"]
    tech_idx = st.session_state.current_tech_index
    q_idx = st.session_state.current_question_index
    years_exp = st.session_state.candidate_data["exp"]

    if tech_idx < len(techs):
        tech_skill = techs[tech_idx]
        # Generate questions if not already done
        if tech_skill not in st.session_state.tech_questions_generated:
            with st.spinner(f"Generating {TECH_Q_PER_SKILL} questions for {tech_skill}..."):
                questions_prompt = generate_tech_questions_prompt(tech_skill, years_exp)
                generated_questions = get_llama_response(questions_prompt)
                questions = extract_questions(generated_questions)
                st.session_state.tech_questions_generated[tech_skill] = questions[:TECH_Q_PER_SKILL]
                st.session_state.answers[tech_skill] = [""] * TECH_Q_PER_SKILL

        questions = st.session_state.tech_questions_generated[tech_skill]
        answers = st.session_state.answers[tech_skill]

        if q_idx < len(questions):
            question = questions[q_idx]
            st.subheader(f"{tech_skill} - Question {q_idx+1}/{len(questions)}")
            st.markdown(f"**Q:** {question}")

            with st.form(key=f"form_{tech_skill}_{q_idx}_{st.session_state.phase}"):
                user_answer = st.text_area("Your Answer:", key=f"answer_input_{tech_skill}_{q_idx}_{st.session_state.phase}", value=answers[q_idx])
                submitted = st.form_submit_button("Submit Answer")
                if submitted and user_answer:
                    st.session_state.answers[tech_skill][q_idx] = user_answer
                    st.success("Answer submitted!")

            # Navigation
            if answers[q_idx]:
                if q_idx + 1 < len(questions):
                    if st.button("Next Question"):
                        st.session_state.current_question_index += 1
                        st.rerun()
                else:
                    if st.button("Next Technology"):
                        st.session_state.current_tech_index += 1
                        st.session_state.current_question_index = 0
                        st.rerun()
        else:
            st.success(f"All questions for {tech_skill} answered!")
            if st.button("Next Technology"):
                st.session_state.current_tech_index += 1
                st.session_state.current_question_index = 0
                st.rerun()
    else:
        st.success("All technical questions answered! Click 'Continue' to see your summary.")
        if st.button("Continue to Summary"):
            move_to_next_phase()
            st.rerun()

# --- Candidate Summary & End Conversation ---
elif st.session_state.phase == "summary":
    st.header("Screening Complete!")
    st.info("Thank you for participating in TalentScout's AI-powered screening process. Here's a summary of the information collected:")
    st.markdown(summarize_candidate_data(st.session_state.candidate_data))
    # Show answers
    st.header("Your Technical Answers")
    for tech in st.session_state.candidate_data["tech_stack"]:
        if tech in st.session_state.tech_questions_generated:
            questions = st.session_state.tech_questions_generated[tech]
            answers = st.session_state.answers[tech]
            for i, (question, answer) in enumerate(zip(questions, answers)):
                st.markdown(f"**Q{i+1}:** {question}")
                st.markdown(f"**Your Answer:** {answer}")
                st.divider()
    if st.button("Finish"):
        move_to_next_phase()
        st.rerun()

elif st.session_state.phase == "end":
    st.success("Conversation ended. Thank you for your time!")

# Show exit option in all phases except end
if st.session_state.phase != "end":
    show_exit_input()
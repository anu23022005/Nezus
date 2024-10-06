import streamlit as st
import google.generativeai as genai
import random
import os

# Configure the Gemini API
genai.configure(api_key='AIzaSyDFXfOzTpQ-ECSQIiG_krhgu4_vwwIHH2U')  # Replace with your actual API key

# Set up the model
model = genai.GenerativeModel('gemini-pro')

# Define the SDGs
sdgs = {
    1: "No Poverty",
    2: "Zero Hunger",
    3: "Good Health and Well-being",
    4: "Quality Education",
    5: "Gender Equality",
    6: "Clean Water and Sanitation",
    7: "Affordable and Clean Energy",
    8: "Decent Work and Economic Growth",
    9: "Industry, Innovation and Infrastructure",
    10: "Reduced Inequalities",
    11: "Sustainable Cities and Communities",
    12: "Responsible Consumption and Production",
    13: "Climate Action",
    14: "Life Below Water",
    15: "Life on Land",
    16: "Peace, Justice and Strong Institutions",
    17: "Partnerships for the Goals"
}

@st.cache_data
def get_ai_response(prompt):
    try:
        sdg_prompt = f"Respond only if this question is related to Sustainable Development Goals (SDGs). If it's not related to SDGs, respond with 'I can only answer questions related to Sustainable Development Goals.' Here's the question: {prompt}"
        response = model.generate_content(sdg_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def is_sdg_related(text):
    sdg_keywords = [
        "sdg", "sustainable development", "global goals", "2030 agenda",
        "poverty", "hunger", "health", "education", "gender equality",
        "clean water", "sanitation", "clean energy", "economic growth",
        "innovation", "reduced inequalities", "sustainable cities",
        "responsible consumption", "climate action", "life below water",
        "life on land", "peace", "justice", "global partnership"
    ]
    return any(keyword in text.lower() for keyword in sdg_keywords)

def generate_quiz_question():
    selected_sdg = random.choice(list(sdgs.values()))
    prompt = f"""Create a unique and engaging multiple-choice question about the Sustainable Development Goal: {selected_sdg}. 
    Ensure the question is different from any previously asked.
    Provide four options labeled A, B, C, D. 
    Also provide a brief explanation for why the correct answer is right and why each incorrect option is wrong.
    Format the response as follows:
    Question: [Your question here]
    A. [Option A]
    B. [Option B]
    C. [Option C]
    D. [Option D]
    Correct answer: [Correct letter]
    Explanation: [Brief explanation for the correct answer and why each incorrect option is wrong]"""
    response = get_ai_response(prompt)
    
    # Parse the response
    parts = response.split('\n')
    question = parts[0].replace("Question: ", "")
    options = parts[1:5]
    correct_answer = parts[5].replace("Correct answer: ", "")
    explanation = '\n'.join(parts[6:]).replace("Explanation: ", "")
    
    return {
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "explanation": explanation
    }

def main():
    st.set_page_config(page_title="SDG Learning Platform", layout="wide")

    # Custom CSS for better styling
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
    }
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #0066cc;
        color: white;
    }
    .stRadio > div {
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        margin: 5px 0;
    }
    .success-message {
        padding: 20px;
        border-radius: 5px;
        background-color: #d4edda;
        color: #155724;
        margin: 10px 0;
    }
    .error-message {
        padding: 20px;
        border-radius: 5px;
        background-color: #f8d7da;
        color: #721c24;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title with modern styling
    st.title("SDG Learning Platform")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar navigation
    page = st.sidebar.selectbox("Choose a feature", ["Learn", "Quiz", "Chat"])
    
    # Sidebar instructions
    st.sidebar.title("How to Use")
    if page == "Learn":
        st.sidebar.write("""
        1. Select an SDG from the dropdown menu
        2. Click "Get Information" to learn about the selected goal
        3. Explore different SDGs to understand their objectives
        """)
    elif page == "Quiz":
        st.sidebar.write("""
        1. Click "Generate Quiz Question" to get a new question
        2. Select your answer from the options
        3. Click "Submit Answer" to see if you're correct
        4. Generate a new question to continue learning
        """)
    else:  # Chat
        st.sidebar.write("""
        This chatbot can answer questions about:
        - All 17 Sustainable Development Goals
        - SDG implementation strategies
        - Global progress on SDGs
        - SDG indicators and targets
        - Related sustainability topics
        
        Just type your question in the chat input below!
        """)

    # Main content area
    if page == "Learn":
        st.header("Learn About SDGs")
        
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            The Sustainable Development Goals (SDGs) are a collection of 17 interlinked global goals designed to be a 
            "blueprint to achieve a better and more sustainable future for all." Select a goal below to learn more.
        </div>
        """, unsafe_allow_html=True)
        
        selected_sdg = st.selectbox("Choose an SDG to learn about", list(sdgs.values()))
        if st.button("Get Information", key="learn_button"):
            with st.spinner("Gathering information..."):
                prompt = f"Provide a comprehensive overview of the Sustainable Development Goal: {selected_sdg}. Include its main objectives, targets, and why it's important for global sustainability."
                response = get_ai_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)

    elif page == "Quiz":
        st.header("Test Your SDG Knowledge")
        
        # Initialize quiz state if not exists
        if "quiz_state" not in st.session_state:
            st.session_state.quiz_state = {
                "question": None,
                "options": None,
                "correct_answer": None,
                "explanation": None,
                "answered": False,
                "selected_option": None
            }

        # Generate new question button
        if st.button("Generate Quiz Question", key="quiz_button"):
            # Generate a new question
            new_question = generate_quiz_question()
            st.session_state.quiz_state = {
                "question": new_question["question"],
                "options": new_question["options"],
                "correct_answer": new_question["correct_answer"],
                "explanation": new_question["explanation"],
                "answered": False,
                "selected_option": None
            }

        # Display question if available
        if st.session_state.quiz_state["question"]:
            # Display question in a styled container
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.quiz_state["question"])
            st.markdown("</div>", unsafe_allow_html=True)

            # Options selection
            options = [opt.strip() for opt in st.session_state.quiz_state["options"]]
            selected_option = st.radio("Select your answer:", options, key="quiz_options", index=None)
            
            # Submit answer button
            if selected_option and not st.session_state.quiz_state["answered"] and st.button("Submit Answer", key="submit_answer"):
                st.session_state.quiz_state["answered"] = True
                st.session_state.quiz_state["selected_option"] = selected_option[0]  # Store only the letter
                
                if st.session_state.quiz_state["selected_option"] == st.session_state.quiz_state["correct_answer"]:
                    st.success("🎉 Correct! Well done!")
                else:
                    st.error(f"Sorry, that's incorrect. The correct answer is {st.session_state.quiz_state['correct_answer']}.")
                    st.info("Explanation: " + st.session_state.quiz_state["explanation"])
                
                # Add a divider and suggestion for next question
                st.divider()
                st.info("Click 'Generate Quiz Question' to try another question!")
        else:
            # Initial state - prompt user to generate a question
            st.info("Click 'Generate Quiz Question' to start the quiz!")

    elif page == "Chat":
        st.header("Chat with SDG Expert")
        
        # Display welcome message if no messages yet
        if not st.session_state.messages:
            st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                👋 Welcome to the SDG Chat! I'm here to help you learn about the Sustainable Development Goals. 
                Feel free to ask any questions about SDGs, their implementation, progress, or related topics.
            </div>
            """, unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about SDGs..."):
            if is_sdg_related(prompt):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate and display AI response
                with st.spinner("Thinking..."):
                    ai_response = get_ai_response(prompt)
                    with st.chat_message("assistant"):
                        st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.warning("Please ask a question related to Sustainable Development Goals (SDGs).")

if __name__ == "__main__":
    main()

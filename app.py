import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="AI Calculator Chatbot", layout="centered")

# --- Custom Header Styling with Dark Blue Gradient ---
st.markdown("""
    <style>
    /* Dark navy gradient header background for smoother integration */
    header.stAppHeader {
        background: linear-gradient(90deg, #1a2a6c, #141e30, #243b55) !important;
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid #222;
        transition: background-color 0.3s ease;
        z-index: 9999;
    }
    /* White icons and buttons in header */
    header.stAppHeader svg,
    header.stAppHeader button {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    /* Hover effect on header buttons/icons */
    header.stAppHeader button:hover svg {
        fill: #00c6ff !important;
        color: #00c6ff !important;
    }
    /* Cleaner header toolbar padding */
    header.stAppHeader .stAppToolbar {
        padding: 8px 20px !important;
    }
    /* Style the main menu button */
    #MainMenu > button {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 5px;
        padding: 5px 8px;
        transition: all 0.3s ease;
    }
    #MainMenu > button:hover {
        background-color: #00c6ff !important;
        border-color: #00c6ff !important;
        color: #000 !important;
    }
    /* Body background and font */
    body {
        background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', sans-serif;
        color: #f8f8f8;
    }
    /* Main app container with dark overlay for readability */
    .stApp {
        background: rgba(20, 30, 48, 0.85);
        border-radius: 15px;
        padding: 30px 40px;
        margin: 30px auto;
        max-width: 600px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        color: #f8f8f8;
    }
    /* Title styling */
    .title {
        font-size: 36px;
        font-weight: 700;
        color: #00c6ff;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)


# --- Voice Feedback (Safe Import) ---
try:
    import pyttsx3

    engine = pyttsx3.init()

    def speak(text):
        engine.say(text)
        engine.runAndWait()
except Exception:
    def speak(text):
        pass  # no-op if pyttsx3 not installed


# --- UI ---
st.markdown('<div class="title">🤖 AI Calculator Chatbot</div>', unsafe_allow_html=True)
st.markdown("---")

num_values = st.slider("How many numbers do you want to enter?", 2, 10, 2)
numbers = [st.number_input(f"Enter value {i+1}", key=f"num_{i}", format="%.6f") for i in range(num_values)]

operation = st.selectbox(
    "Choose an operation",
    [
        "Addition",
        "Subtraction",
        "Multiplication",
        "Division",
        "Modulus",
        "Exponentiation",
        "Average",
        "Maximum",
        "Minimum",
    ],
)

def calculate(numbers, operation):
    try:
        if operation == "Addition":
            return sum(numbers)
        elif operation == "Subtraction":
            result = numbers[0]
            for num in numbers[1:]:
                result -= num
            return result
        elif operation == "Multiplication":
            result = 1
            for num in numbers:
                result *= num
            return result
        elif operation == "Division":
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    return "Error: Division by zero"
                result /= num
            return result
        elif operation == "Modulus":
            if len(numbers) != 2:
                return "Error: Modulus requires exactly 2 numbers"
            if numbers[1] == 0:
                return "Error: Division by zero in modulus"
            return numbers[0] % numbers[1]
        elif operation == "Exponentiation":
            if len(numbers) != 2:
                return "Error: Exponentiation requires exactly 2 numbers"
            return numbers[0] ** numbers[1]
        elif operation == "Average":
            return sum(numbers) / len(numbers)
        elif operation == "Maximum":
            return max(numbers)
        elif operation == "Minimum":
            return min(numbers)
        else:
            return "Unsupported operation"
    except Exception as e:
        return f"Error: {e}"

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Calculate", use_container_width=True):
    result = calculate(numbers, operation)
    result_str = f"{operation} Result: {result}"
    st.success(result_str)
    speak(result_str)
    st.session_state.history.append(result_str)

if st.session_state.history:
    st.markdown("### 🕒 History (Session Only)")
    for entry in reversed(st.session_state.history[-10:]):
        st.write(entry)

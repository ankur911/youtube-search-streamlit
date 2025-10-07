import streamlit as st

st.title("🧪 Button Test")

# Initialize state
if 'test_player' not in st.session_state:
    st.session_state.test_player = False

st.write(f"Current state: {st.session_state.test_player}")

# Button test - without rerun to prevent page refresh
if st.session_state.test_player:
    if st.button("❌ Hide"):
        st.session_state.test_player = False
else:
    if st.button("▶️ Play"):
        st.session_state.test_player = True

# Show player
if st.session_state.test_player:
    st.success("🎥 Player would be here!")
    st.write("This confirms the button state is working!")
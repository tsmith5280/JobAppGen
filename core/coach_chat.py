import streamlit as st

def run_ai_coach_chat(model, client):
    st.markdown("### 🤖 AI Job Coach Chat")
    if "coach_history" not in st.session_state:
        st.session_state.coach_history = [
            {"role": "system", "content": "You are an empathetic but direct AI job coach named Virel. Keep replies short, sharp, and helpful. Use markdown for bold tips."}
        ]
    if len(st.session_state.coach_history) == 1:
        st.chat_message("assistant").write("Hi there! I’m your job coach, Virel. Ask me anything about resumes, cover letters, or job strategy.")

    if prompt := st.chat_input("Ask the AI Coach..."):
        st.chat_message("user").write(prompt)
        st.session_state.coach_history.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.coach_history
            )
            reply = response.choices[0].message.content
            st.chat_message("assistant").write(reply)
            st.session_state.coach_history.append({"role": "assistant", "content": reply})

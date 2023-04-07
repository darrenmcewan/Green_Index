import streamlit as st
import scripts.state_incentives


st.set_page_config(page_title="State Renewable Incentive", page_icon="📈")

with open('data/states.txt', 'r') as f:
    lines = f.readlines()

states = {}
statesBounding = {}
for line in lines:
    state_data = line.strip().split(': ')
    abbr, name = state_data[0], state_data[1].split(':')[0]
    values = [float(x) for x in state_data[2][1:-1].split(', ')]
    states[abbr] = name
    statesBounding[abbr] = values

st.markdown("# Renewable Resource Incentive")
st.sidebar.header("State Incentives")
state = st.sidebar.selectbox("Find Renewable Energy Near You", states, help="Select a state to zoom in on", index=0)
st.write(
    """Below is a list of incentives for various states in order to adopt renewable resources"""
)





st.markdown(f"## Incentives for renewable energy in {state}:")
incentives = scripts.state_incentives.show_resources(state)
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.write(incentives, unsafe_allow_html=True)
import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge 
from streamlit_flow.layouts import TreeLayout

from utility import check_password

st.set_page_config(
    page_title="Methodology",
    page_icon="🏠",
    layout="wide"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.title("Methodology")

# Define nodes with distinct positions
nodes = [
    StreamlitFlowNode(id='1', pos=(0, 0), data={'content': 'Start Chatbot'}, node_type='input', source_position='bottom'),
    StreamlitFlowNode('2', pos=(0, 1), data={'content': 'Greeting user'}, node_type='default', source_position='bottom', target_position='top'),
    StreamlitFlowNode('3', pos=(0, 2), data={'content': 'User Query'}, node_type='default', source_position='bottom', target_position='top'),
    StreamlitFlowNode('4', pos=(0, 3), data={'content': 'Process Query with CrewAI'}, node_type='default', source_position='bottom', target_position='top'),
    StreamlitFlowNode('5', pos=(0, 4), data={'content': 'Provide Response'}, node_type='default', source_position='bottom', target_position='top'),
    StreamlitFlowNode('6', pos=(0, 5), data={'content': 'End Chat'}, node_type='output', target_position='top')
]

# Define edges
edges = [
    StreamlitFlowEdge('1-2', '1', '2', animated=True),
    StreamlitFlowEdge('2-3', '2', '3', animated=True),
    StreamlitFlowEdge('3-4', '3', '4', animated=True),
    StreamlitFlowEdge('4-5', '4', '5', animated=True),
    StreamlitFlowEdge('5-6', '5', '6', animated=True)
]

# Render the flowchart
streamlit_flow('tree_layout', nodes, edges, layout=TreeLayout(direction='down'), fit_view=True)

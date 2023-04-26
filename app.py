import streamlit as st
import pickle
import plotly.graph_objects as go
import networkx as nx


st.set_page_config(page_title="Flint Graph Streamlit App", layout="wide")

@st.cache_resource
def get_data():
    graph1 = pickle.load(open('saved_graph4_19.p','rb'))
    return graph1

graph1 = get_data()
C = [graph1.subgraph(c) for c in nx.connected_components(graph1)]
G = C[0]

def display_subgraph(node_name):
    G = C[0].subgraph(nx.single_source_shortest_path_length(C[0], node_name, cutoff=1))

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'{str(adjacencies[0])} has '+str(len(adjacencies[1]))+' connection(s)')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title=f'<br>Subgraph containing node {node_name}',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig



st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #23d5ab !important;
        color: #fff !important;
        border-radius: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Flint Node of Interest Subgraph")
st.write("This is a Streamlit app that displays a subgraph containing a node of interest and its neighbors, along with the edges connecting them. You can choose from a pre-defined list of 10 names in a dropdown menu and click a button to display the corresponding subgraph, or you can search for a name by manually entering it in the below text box which has a dropdown of possible names that dynamically updates as you type.")


#-------------------------------------------
# User chooses name from dropdown
#st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid black'>", unsafe_allow_html=True)
st.subheader("Choose from 10 Pre-Defined Names")
example_names = ["Kelenske, Chris (MSP)", "Moore, Kristin", "McShane, Hilda", "Russo, Mark (MSP)", "Leix, Ron (MSP)", "MSP-EOC-MDEQ", "Kuzera, Michelle (MSP)", "Lasher, Tony P.", "Morris, David (MSP)", "Eickholt, Jay (MSP)"]
selected_name = st.selectbox("Select an example name from 10 choices: ", example_names)
if st.button("Display Graph for Selected Name"):
   chart = display_subgraph(selected_name)
   chart.update_layout(
       autosize=True,
       width=1270,
       height=750
   )
   st.plotly_chart(chart)

    
#-------------------------------------------
# User inputs a name
#name = st.text_input('Enter a name: ')
#st.markdown("<hr style='height:3px;border:none;color:#333;background-color:#333;' />", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid black'>", unsafe_allow_html=True)
st.subheader("Manually Enter a Name of your Choosing")
possible_names = list(G.nodes)

name = st.selectbox('Manually type a name and choose from a dynamic dropdown containing all possible names: ', possible_names)

if name != '':
    chart = display_subgraph(name)
    chart.update_layout(
        autosize=True,
        width=1270,
        height=750 
    )
    st.plotly_chart(chart)



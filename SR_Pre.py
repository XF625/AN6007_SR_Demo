### Title: Splay Tree Rotations Visualization for Group A04 Presentation
### Author: Fang Xiran
### Description: This Streamlit app visualizes the Zig (Right) and Zag (Left) rotations in a Splay Tree. Developed with Gemini Pro AI.

import streamlit as st
import graphviz
import time

st.set_page_config(layout="wide", page_title="Splay Tree Rotations")

# --- STATE MANAGEMENT ---
if 'rotated_1' not in st.session_state:
    st.session_state.rotated_1 = False
if 'scenario_2_step' not in st.session_state:
    st.session_state.scenario_2_step = 0

# Zag State
if 'rotated_zag_1' not in st.session_state:
    st.session_state.rotated_zag_1 = False
if 'scenario_zag_2_step' not in st.session_state:
    st.session_state.scenario_zag_2_step = 0

# --- ANIMATION HELPER FUNCTIONS ---

def get_interpolated_pos(start_pos, end_pos, progress):
    """
    Linearly interpolates between two sets of coordinates.
    progress is a float between 0.0 (start) and 1.0 (end).
    """
    current_pos = {}
    all_nodes = set(start_pos.keys()) | set(end_pos.keys())
    
    for node in all_nodes:
        # Get start/end coords, defaulting to the other if missing (to handle appearing/disappearing)
        x1, y1 = start_pos.get(node, end_pos.get(node, (0,0)))
        x2, y2 = end_pos.get(node, start_pos.get(node, (0,0)))
        
        # Linear interpolation
        curr_x = x1 + (x2 - x1) * progress
        curr_y = y1 + (y2 - y1) * progress
        current_pos[node] = f"{curr_x},{curr_y}!" # The '!' forces the position in neato
    
    return current_pos

def render_frame(edges, positions, highlighted_node=None, isolated_nodes=None):
    """
    Renders a single frame of the tree using the 'neato' engine for exact positioning.
    """
    graph = graphviz.Digraph(engine='neato')
    graph.attr(bgcolor='transparent')
    # Standard node styles
    graph.attr('node', shape='circle', style='filled', fillcolor='white', color='black', fontname='Helvetica', width='0.5', fixedsize='true')
    
    # Add nodes with specific positions
    for node_id, pos_raw in positions.items():
        fill = 'white'
        color = 'black'
        
        # Highlight logic
        if highlighted_node and str(node_id) == str(highlighted_node):
            fill = '#ffcccc'
            color = 'red'
        
        # Isolated node logic (Yellowish)
        if isolated_nodes and str(node_id) in isolated_nodes:
            if str(node_id) != str(highlighted_node):
                fill = '#ffffcc'
                color = '#555555'

        # Handle tuple coordinates (from static definitions) vs string coordinates (from interpolation)
        if isinstance(pos_raw, (tuple, list)):
            pos_str = f"{pos_raw[0]},{pos_raw[1]}!"
        else:
            pos_str = pos_raw

        graph.node(str(node_id), pos=pos_str, fillcolor=fill, color=color)

    # Add edges
    for u, v, _ in edges:
        # If an edge involves an isolated node, we might skip it or draw it dashed
        # For this logic, we only draw edges provided in the list
        graph.edge(str(u), str(v))
        
    return graph

def animate_transition(placeholder, start_coords, end_coords, edges, highlighted_node=None, isolated_nodes=None, duration=0.6, steps=15):
    """
    Runs the animation loop.
    """
    for i in range(steps + 1):
        progress = i / steps
        # Easing function for smoother motion (Ease-Out Quad)
        # progress = 1 - (1 - progress) * (1 - progress) 
        
        curr_pos = get_interpolated_pos(start_coords, end_coords, progress)
        placeholder.graphviz_chart(render_frame(edges, curr_pos, highlighted_node, isolated_nodes))
        time.sleep(duration / steps)

# --- COORDINATE DEFINITIONS (X, Y) ---
# Scale: X moves by ~1.5, Y moves by ~1.0

# === ZIG (RIGHT) COORDINATES ===
# Scenario 1 (Keep as 1, 2, 3)
S1_START_POS = {'2': (0,0), '1': (-1.5, -1), '3': (1.5, -1)}
S1_END_POS   = {'1': (0,0), '2': (1.5, -1), '3': (2.5, -2)} 

# Scenario 2 (Renamed to 5, 6, 7, 8)
# Structure: 8 is Root. 6 is Left Child. 6 has Left(5) and Right(7).
# Step 0: Initial
S2_POS_0 = {'8': (0,0), '6': (-1.5, -1), '5': (-2.5, -2), '7': (-0.5, -2)}
# Step 1: Disconnected (6 moves up, 8 moves right, 7 floats)
S2_POS_1 = {'6': (0,0), '8': (1.5, -1), '5': (-1.5, -1), '7': (0, -1.5)} 
# Step 2: Reconnected (7 moves to 8's left)
S2_POS_2 = {'6': (0,0), '8': (1.5, -1), '5': (-1.5, -1), '7': (0.5, -2)}

# === ZAG (LEFT) COORDINATES (MIRRORED X) ===
# Scenario 1 Zag (Root 2, Right Child 3 moves up)
S1_ZAG_START = {'2': (0,0), '3': (1.5, -1), '1': (-1.5, -1)}
S1_ZAG_END   = {'3': (0,0), '2': (-1.5, -1), '1': (-2.5, -2)}

# Scenario 2 Zag (Root 4, Right Child 6 moves up. 6 has Left Child 5)
# Initial: 4(Root), 6(R). 6 has 5(L), 7(R)
S2_ZAG_POS_0 = {'4': (0,0), '6': (1.5, -1), '7': (2.5, -2), '5': (0.5, -2)}
# Step 1: Disconnected (6 moves up, 4 moves left, 5 floats)
S2_ZAG_POS_1 = {'6': (0,0), '4': (-1.5, -1), '7': (1.5, -1), '5': (0, -1.5)}
# Step 2: Reconnected (5 moves to 4's Right)
S2_ZAG_POS_2 = {'6': (0,0), '4': (-1.5, -1), '7': (1.5, -1), '5': (-0.5, -2)}


# --- APP NAVIGATION ---
page = st.sidebar.radio("Select Rotation Type", ["Zig (Right Rotation)", "Zag (Left Rotation)"])

if page == "Zig (Right Rotation)":
    st.title("Splay Tree: Zig (Right) Rotation")
    st.caption("Triggered when node is a **Left Child** of the root.")
    
    col1, col2 = st.columns(2)

    # ====== SCENARIO 1 (ZIG) ======
    with col1:
        st.header("Scenario 1: Simple Zig")
        st.markdown("Goal: Move Node **1** to the Root")
        
        chart_1 = st.empty()
        
        if not st.session_state.rotated_1:
            # Render Initial State
            edges_initial = [('2','1','L'), ('2','3','R')]
            chart_1.graphviz_chart(render_frame(edges_initial, S1_START_POS))
            
            if st.button("Rotate Right (Move 1 Up)", key="btn1"):
                # Motion animation
                edges_target = [('1','2','R'), ('2','3','R')]
                animate_transition(chart_1, S1_START_POS, S1_END_POS, edges_target, highlighted_node='1')
                st.session_state.rotated_1 = True
                st.rerun()
        else:
            # Render Final State
            edges_final = [('1','2','R'), ('2','3','R')]
            chart_1.graphviz_chart(render_frame(edges_final, S1_END_POS, highlighted_node='1'))
            
            if st.button("Reset Tree 1", key="reset1"):
                st.session_state.rotated_1 = False
                st.rerun()

            st.info("""
            **What happened?**
            * Node **1** moved up.
            * Node **2** moved down to the *right* of 1.
            * Node **3** stayed attached to 2.
            """)

    # ====== SCENARIO 2 (ZIG) ======
    with col2:
        st.header("Scenario 2: Moving Subtrees")
        st.markdown("Goal: Move Node **6** to the Root")
        
        chart_2 = st.empty()

        # Step 0: Initial
        if st.session_state.scenario_2_step == 0:
            # Root 8, Target 6 (Left). 6 has children 5(L) and 7(R).
            edges_0 = [('8','6','L'), ('6','5','L'), ('6','7','R')]
            chart_2.graphviz_chart(render_frame(edges_0, S2_POS_0))
            
            if st.button("Step 1: Move Root & Disconnect Child", key="s2_btn1"):
                # Transition: 0 -> 1
                # 6 moves to Root. 8 moves to Right. 7 is missing (floating).
                edges_1 = [('6','5','L'), ('6','8','R')] 
                animate_transition(chart_2, S2_POS_0, S2_POS_1, edges_1, highlighted_node='6', isolated_nodes=['7'])
                st.session_state.scenario_2_step = 1
                st.rerun()

        # Step 1: Disconnected
        elif st.session_state.scenario_2_step == 1:
            edges_1 = [('6','5','L'), ('6','8','R')]
            chart_2.graphviz_chart(render_frame(edges_1, S2_POS_1, highlighted_node='6', isolated_nodes=['7']))
            
            if st.button("Step 2: Reconnect Child (Handover)", key="s2_btn2"):
                # Transition: 1 -> 2
                # 7 gets reconnected to 8's Left
                edges_2 = [('6','5','L'), ('6','8','R'), ('8','7','L')]
                animate_transition(chart_2, S2_POS_1, S2_POS_2, edges_2, highlighted_node='7')
                st.session_state.scenario_2_step = 2
                st.rerun()

            st.warning("""
            **Step 1 Complete:**
            * Node **6** moved to root.
            * Node **8** moved right.
            * **CRITICAL:** Node **7** is "floating" (disconnected).
            """)

        # Step 2: Final
        elif st.session_state.scenario_2_step == 2:
            edges_2 = [('6','5','L'), ('6','8','R'), ('8','7','L')]
            chart_2.graphviz_chart(render_frame(edges_2, S2_POS_2, highlighted_node='6'))
            
            if st.button("Reset Tree 2", key="reset2"):
                st.session_state.scenario_2_step = 0
                st.rerun()

            st.success("""
            **Step 2 Complete:**
            * Node **7** attaches as the **Left child of 8**.
            """)

elif page == "Zag (Left Rotation)":
    st.title("Splay Tree: Zag (Left) Rotation")
    st.caption("Triggered when node is a **Right Child** of the root.")
    
    col1, col2 = st.columns(2)

    # ====== SCENARIO 1 (ZAG) ======
    with col1:
        st.header("Scenario 1: Simple Zag")
        st.markdown("Goal: Move Node **3** to the Root")
        
        chart_zag_1 = st.empty()
        
        if not st.session_state.rotated_zag_1:
            # Initial State: 2 is Root, 3 is Right, 1 is Left
            edges_initial = [('2','3','R'), ('2','1','L')]
            chart_zag_1.graphviz_chart(render_frame(edges_initial, S1_ZAG_START))
            
            if st.button("Rotate Left (Move 3 Up)", key="btn_zag1"):
                # Motion animation
                # Target: 3 is Root, 2 is Left, 1 is Left of 2
                edges_target = [('3','2','L'), ('2','1','L')]
                animate_transition(chart_zag_1, S1_ZAG_START, S1_ZAG_END, edges_target, highlighted_node='3')
                st.session_state.rotated_zag_1 = True
                st.rerun()
        else:
            # Render Final State
            edges_final = [('3','2','L'), ('2','1','L')]
            chart_zag_1.graphviz_chart(render_frame(edges_final, S1_ZAG_END, highlighted_node='3'))
            
            if st.button("Reset Tree 1", key="reset_zag1"):
                st.session_state.rotated_zag_1 = False
                st.rerun()

            st.info("""
            **What happened?**
            * Node **3** moved up.
            * Node **2** moved down to the *left* of 3.
            * Node **1** stayed attached to 2.
            """)

    # ====== SCENARIO 2 (ZAG) ======
    with col2:
        st.header("Scenario 2: Moving Subtrees")
        st.markdown("Goal: Move Node **6** to the Root")
        
        chart_zag_2 = st.empty()

        # Step 0: Initial
        if st.session_state.scenario_zag_2_step == 0:
            # 4 is Root, 6 is Right. 6 has 5(L) and 7(R)
            edges_0 = [('4','6','R'), ('6','5','L'), ('6','7','R')]
            chart_zag_2.graphviz_chart(render_frame(edges_0, S2_ZAG_POS_0))
            
            if st.button("Step 1: Move Root & Disconnect Child", key="s2_zag_btn1"):
                # Transition: 0 -> 1
                # 6 moves to Root. 4 moves to Left. 5 is missing.
                edges_1 = [('6','4','L'), ('6','7','R')] 
                animate_transition(chart_zag_2, S2_ZAG_POS_0, S2_ZAG_POS_1, edges_1, highlighted_node='6', isolated_nodes=['5'])
                st.session_state.scenario_zag_2_step = 1
                st.rerun()

        # Step 1: Disconnected
        elif st.session_state.scenario_zag_2_step == 1:
            edges_1 = [('6','4','L'), ('6','7','R')]
            chart_zag_2.graphviz_chart(render_frame(edges_1, S2_ZAG_POS_1, highlighted_node='6', isolated_nodes=['5']))
            
            if st.button("Step 2: Reconnect Child (Handover)", key="s2_zag_btn2"):
                # Transition: 1 -> 2
                # 5 gets reconnected to 4's Right
                edges_2 = [('6','4','L'), ('6','7','R'), ('4','5','R')]
                animate_transition(chart_zag_2, S2_ZAG_POS_1, S2_ZAG_POS_2, edges_2, highlighted_node='5')
                st.session_state.scenario_zag_2_step = 2
                st.rerun()

            st.warning("""
            **Step 1 Complete:**
            * Node **6** moved to root.
            * Node **4** moved left.
            * **CRITICAL:** Node **5** (Left child of 6) is "floating" (disconnected).
            """)

        # Step 2: Final
        elif st.session_state.scenario_zag_2_step == 2:
            edges_2 = [('6','4','L'), ('6','7','R'), ('4','5','R')]
            chart_zag_2.graphviz_chart(render_frame(edges_2, S2_ZAG_POS_2, highlighted_node='6'))
            
            if st.button("Reset Tree 2", key="reset_zag2"):
                st.session_state.scenario_zag_2_step = 0
                st.rerun()

            st.success("""
            **Step 2 Complete:**
            * Node **5** attaches as the **Right child of 4**.
            """)


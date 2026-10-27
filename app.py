
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from library_data import (
    LIBRARY_GRAPH, BOOKS, NODE_POSITIONS,
    CLOSED_SECTIONS_DEFAULT, RESTRICTED_SHELVES_DEFAULT,
    CROWDED_AISLES_DEFAULT
)
from algorithms import available_graph, bfs, dfs, astar, path_cost
from route_planner import plan_collection

st.set_page_config(
    page_title="Library Search Agent",
    page_icon="📚",
    layout="wide"
)

# Updated styling to match the reference image: mint sidebar, clean white cards, teal accents.
st.markdown("""
<style>
:root {
    color-scheme: light;
    --primary-color: #0D9488;
    --background-color: #F8FAFC;
    --secondary-background-color: #E8F6F5;
    --text-color: #26364B;
}

/* Main app background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #F8FAFC !important;
    color: #26364B !important;
}

/* Typography */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] .stMarkdown,
[data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"],
[data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] p {
    color: #334155 !important;
}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3 {
    color: #172B4D !important;
    font-weight: 700 !important;
}

[data-testid="stAppViewContainer"] h1 {
    font-size: 2.1rem !important;
}

[data-testid="stCaptionContainer"] p {
    color: #718096 !important;
}

/* Header and sidebar */
[data-testid="stHeader"] {
    background-color: #F8FAFC !important;
}

[data-testid="stSidebar"] {
    background-color: #E8F6F5 !important;
    border-right: 1px solid #D2E9E7 !important;
}

[data-testid="stSidebar"] > div {
    background-color: #E8F6F5 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172B4D !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stMarkdown {
    color: #334155 !important;
}

/* Dropdowns and multiselects */
.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D6E3EA !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

.stSelectbox [data-baseweb="select"] *,
.stMultiSelect [data-baseweb="select"] * {
    color: #334155 !important;
}

.stSelectbox svg,
.stMultiSelect svg {
    color: #64748B !important;
    fill: #64748B !important;
}

/* Dropdown popup */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="list"] {
    background-color: #FFFFFF !important;
}

[role="option"] {
    background-color: #FFFFFF !important;
    color: #334155 !important;
}

[role="option"]:hover,
[aria-selected="true"][role="option"] {
    background-color: #E4F5F2 !important;
    color: #115E59 !important;
}


/* Selected pills: lavender purple */
div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background-color: #DCCEF5 !important;
    background: #DCCEF5 !important;
    border: 1px solid #BCA7E8 !important;
}

div[data-testid="stMultiSelect"] [data-baseweb="tag"] span {
    color: #40276B !important;
}

div[data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
    color: #40276B !important;
    fill: #40276B !important;
}


/* Text and number inputs */
.stNumberInput input,
.stTextInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #26364B !important;
    border: 1px solid #D6E3EA !important;
    border-radius: 9px !important;
}

.stNumberInput button {
    background-color: #F1F7F8 !important;
    color: #334155 !important;
    border-color: #D6E3EA !important;
}

/* Primary buttons */
.stButton > button,
.stDownloadButton > button {
    background-color: #0D9488 !important;
    color: #FFFFFF !important;
    border: 1px solid #0D9488 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button *,
.stDownloadButton > button * {
    color: #FFFFFF !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #0F766E !important;
    border-color: #0F766E !important;
    box-shadow: 0 3px 8px rgba(13, 148, 136, 0.18) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #F0F5F9 !important;
    border: 1px solid #E1EAF0 !important;
    border-radius: 11px !important;
    padding: 4px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    border-radius: 9px !important;
    padding: 10px 14px !important;
}

.stTabs [data-baseweb="tab"] p {
    color: #334155 !important;
    font-weight: 600 !important;
}

.stTabs [aria-selected="true"] {
    background-color: #D1F0E8 !important;
    border-bottom: 3px solid #0D9488 !important;
}

.stTabs [aria-selected="true"] p {
    color: #115E59 !important;
}


/* Purple slider */
div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background-color: #7952B3 !important;
    border-color: #7952B3 !important;
}

div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background-color: #7952B3 !important;
}


/* White metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DFE8EF !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #718096 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #0F766E !important;
}

/* Alerts and search-result information */
[data-testid="stAlert"] {
    background-color: #EAF4FF !important;
    border: 1px solid #D7E8F8 !important;
    border-radius: 10px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    color: #334155 !important;
}

[data-testid="stAlert"][kind="success"] {
    background-color: #E5F6EE !important;
    border-color: #BCE7D0 !important;
}

/* Code blocks and data tables */
.stCode,
.stCode pre,
.stCode code {
    background-color: #F0F5F9 !important;
    color: #26364B !important;
    border-radius: 8px !important;
}

[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DFE8EF !important;
    border-radius: 10px !important;
}

/* Layout and dividers */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

hr {
    border-color: #DFE8EF !important;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# Application heading
st.title("📚 Intelligent Library Search & Collection Agent")
st.caption(
    "An AI-based library navigation system using graph search, "
    "heuristic pathfinding and route planning."
)


# Sidebar settings
with st.sidebar:
    st.header("Library Controls")

    all_nodes = list(LIBRARY_GRAPH.keys())

    start_node = st.selectbox(
        "Starting point",
        all_nodes,
        index=0
    )

    st.markdown("### Library Conditions")

    closed_sections = st.multiselect(
        "Closed sections",
        all_nodes,
        default=CLOSED_SECTIONS_DEFAULT
    )

    restricted_shelves = st.multiselect(
        "Restricted shelves",
        all_nodes,
        default=RESTRICTED_SHELVES_DEFAULT
    )

    crowded_aisles = st.multiselect(
        "Crowded aisles",
        all_nodes,
        default=CROWDED_AISLES_DEFAULT
    )

    crowd_penalty = st.slider(
        "Crowded aisle penalty",
        min_value=0,
        max_value=10,
        value=3
    )

    time_limit = st.number_input(
        "Collection time budget (cost units)",
        min_value=1,
        max_value=100,
        value=25
    )


# Apply library conditions
graph = available_graph(
    LIBRARY_GRAPH,
    closed_sections,
    restricted_shelves,
    crowded_aisles,
    crowd_penalty
)

usable_books = [
    book for book in BOOKS
    if book["available"] and book["shelf"] in graph
]


# Main navigation tabs
tab_search, tab_collect, tab_map, tab_catalog = st.tabs([
    "🔎 Find a Book",
    "🧺 Collect Multiple Books",
    "🗺️ Library Graph",
    "📖 Book Catalogue"
])


# --------------------------------------------------
# TAB 1: FIND A BOOK
# --------------------------------------------------
with tab_search:
    left, right = st.columns([1, 1.15], gap="large")

    with left:
        st.subheader("Search Algorithm")

        algorithm = st.radio(
            "Choose algorithm",
            ["BFS", "DFS", "A*"],
            horizontal=True
        )

        target_book_title = st.selectbox(
            "Select a book",
            [book["title"] for book in BOOKS]
        )

        target_book = next(
            book for book in BOOKS
            if book["title"] == target_book_title
        )

        st.write(f"**Author:** {target_book['author']}")
        st.write(f"**Shelf:** {target_book['shelf']}")

        if not target_book["available"]:
            st.warning("This book is currently unavailable.")

        elif target_book["shelf"] not in graph:
            st.warning(
                "This shelf is closed or restricted. "
                "Change the library conditions to access it."
            )

        elif start_node not in graph:
            st.warning(
                "Your starting point is blocked. "
                "Choose an accessible starting point in the sidebar."
            )

        else:
            if st.button("Find Route", key="find_route"):
                if algorithm == "BFS":
                    path, open_list, closed_list = bfs(
                        graph, start_node, target_book["shelf"]
                    )
                    cost = path_cost(graph, path) if path else None

                elif algorithm == "DFS":
                    path, open_list, closed_list = dfs(
                        graph, start_node, target_book["shelf"]
                    )
                    cost = path_cost(graph, path) if path else None

                else:
                    path, open_list, closed_list, cost = astar(
                        graph,
                        start_node,
                        target_book["shelf"],
                        NODE_POSITIONS
                    )

                st.session_state["search_result"] = {
                    "algorithm": algorithm,
                    "path": path,
                    "open": open_list,
                    "closed": closed_list,
                    "cost": cost,
                    "book": target_book_title
                }

    with right:
        st.subheader("Search Results")

        result = st.session_state.get("search_result")

        if result:
            st.write(f"**Algorithm:** {result['algorithm']}")
            st.write(f"**Target book:** {result['book']}")

            if result["path"]:
                st.success("Target shelf found successfully!")

                st.markdown("### Collection Route")

                st.markdown(
                    " → ".join(result["path"])
                )

                st.metric(
                    "Total Path Cost",
                    f"{result['cost']} units"
                )

            else:
                st.error(
                    "No valid route was found with the current restrictions."
                )

            st.markdown("### Open List")
            st.code(
                ", ".join(map(str, result["open"])) or "(empty)",
                language=None
            )

            st.markdown("### Closed List")
            st.code(
                ", ".join(map(str, result["closed"])) or "(empty)",
                language=None
            )

        else:
            st.info(
                "Select a book and an algorithm, then click Find Route."
            )


# --------------------------------------------------
# TAB 2: COLLECT MULTIPLE BOOKS
# --------------------------------------------------
with tab_collect:
    st.subheader("Multiple-Book Collection Planner")

    st.write(
        "Choose books to collect. The planner visits nearby shelves "
        "and uses book priority when estimated costs are equal."
    )

    book_titles = [
        book["title"] for book in usable_books
    ]

    chosen_titles = st.multiselect(
        "Select books to collect",
        book_titles,
        default=book_titles[:3]
    )

    chosen_books = [
        book for book in usable_books
        if book["title"] in chosen_titles
    ]

    if start_node not in graph:
        st.warning(
            "Your starting point is currently inaccessible. "
            "Select another starting point."
        )

    elif st.button("Generate Collection Route", key="collection_route"):
        plan = plan_collection(
            graph,
            start_node,
            chosen_books,
            NODE_POSITIONS,
            time_limit
        )

        st.session_state["collection_result"] = plan

    plan = st.session_state.get("collection_result")

    if plan:
        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Books Planned",
            len(plan["collected"])
        )

        metric2.metric(
            "Total Route Cost",
            f"{plan['total_cost']} units"
        )

        metric3.metric(
            "Not Collected",
            len(plan["skipped"])
        )

        st.markdown("### Planned Collection Route")

        if plan["route"]:
            st.success(" → ".join(plan["route"]))
        else:
            st.info("No collection route is available.")

        if plan["details"]:
            st.markdown("### Collection Details")

            st.dataframe(
                pd.DataFrame(plan["details"]),
                use_container_width=True,
                hide_index=True
            )

        if plan["skipped"]:
            st.warning(
                "These books could not be collected within the budget "
                "or could not be reached: "
                + ", ".join(
                    book["title"] for book in plan["skipped"]
                )
            )

        st.caption(
            "The planner uses a greedy heuristic. It is a practical "
            "approach for this project, but it does not guarantee "
            "the globally shortest route."
        )


# --------------------------------------------------
# TAB 3: LIBRARY GRAPH
# --------------------------------------------------
with tab_map:
    st.subheader("Visual Library Map")

    st.write(
        "Each node represents a library location. "
        "Connections represent walkways, and edge labels show walking costs."
    )

    G = nx.Graph()

    for node, neighbours in graph.items():
        for neighbour, weight in neighbours.items():
            G.add_edge(node, neighbour, weight=weight)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Match the app's light theme
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    pos = {
        node: NODE_POSITIONS[node]
        for node in G.nodes
        if node in NODE_POSITIONS
    }

    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edge_color="#A8C9C4",
        width=2.0
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_color="#D1F0E8",
        edgecolors="#0D9488",
        node_size=2200,
        linewidths=1.8
    )

    nx.draw_networkx_labels(
        G,
        pos,
        ax=ax,
        font_size=8,
        font_weight="bold",
        font_color="#26364B"
    )

    edge_labels = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        ax=ax,
        font_size=8,
        font_color="#64748B",
        rotate=False,
        bbox={
            "alpha": 0.9,
            "color": "#F8FAFC",
            "pad": 1
        }
    )

    ax.set_axis_off()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("### Current Library Conditions")

    condition1, condition2, condition3 = st.columns(3)

    with condition1:
        st.markdown("**Closed Sections**")
        st.write(", ".join(closed_sections) or "None")

    with condition2:
        st.markdown("**Restricted Shelves**")
        st.write(", ".join(restricted_shelves) or "None")

    with condition3:
        st.markdown("**Crowded Aisles**")
        st.write(", ".join(crowded_aisles) or "None")


# --------------------------------------------------
# TAB 4: BOOK CATALOGUE
# --------------------------------------------------
with tab_catalog:
    st.subheader("Library Book Catalogue")

    st.write(
        "Check each book's author, shelf location, availability "
        "and collection priority."
    )

    catalog_rows = []

    for book in BOOKS:
        if not book["available"]:
            status = "Unavailable"

        elif book["shelf"] not in graph:
            status = "Blocked by current settings"

        else:
            status = "Available"

        catalog_rows.append({
            "Title": book["title"],
            "Author": book["author"],
            "Shelf": book["shelf"],
            "Status": status,
            "Priority": book["priority"]
        })

    st.dataframe(
        pd.DataFrame(catalog_rows),
        use_container_width=True,
        hide_index=True
    )


# Footer
st.divider()

st.caption(
    "Intelligent Library Search and Book Collection Agent | "
    "Python, Streamlit and AI Search Algorithms"
)

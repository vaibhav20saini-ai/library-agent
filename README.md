# Intelligent Library Search and Book Collection Agent

A beginner-friendly third-year B.Tech CSE AI project built with Python and Streamlit.

## Features
- Library modeled as a weighted graph.
- BFS, DFS, and A* search.
- Open and closed lists displayed in the interface.
- Closed sections, restricted shelves, unavailable books, and crowded aisle penalties.
- Multiple-book route planner with a time budget and book priority.
- Library graph visualization and book catalogue.
- Soft green and neutral interface; no orange or dark blue theme.

## Files
- `app.py`: Streamlit interface.
- `algorithms.py`: BFS, DFS, A*, graph restrictions, and path cost.
- `library_data.py`: sample library graph, book catalogue, and drawing coordinates.
- `route_planner.py`: greedy multi-book collection planner.
- `requirements.txt`: Python dependencies.

## Run on Windows

Open PowerShell or the VS Code terminal in this project folder.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `python` is not recognized but the Python launcher is installed, try:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Streamlit normally opens the app in your browser at `http://localhost:8501`.

## Connect to Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload all five project files, keeping the same filenames and folder structure.
3. Sign in to Streamlit Community Cloud at https://share.streamlit.io/.
4. Create an app and select the repository, branch, and `app.py` as the main file.
5. Deploy. The `requirements.txt` file tells Streamlit which packages to install.

## How the algorithms work
- **BFS:** explores the graph level by level and finds a path with the fewest edges. It does not necessarily minimize weighted distance.
- **DFS:** explores one branch deeply before backtracking.
- **A\*:** ranks paths using `f(n) = g(n) + h(n)`, where `g(n)` is the cost already paid and `h(n)` estimates remaining distance.
- **Multi-book planner:** greedily visits a nearby shelf and uses priority to break ties. This is an understandable heuristic, not a guarantee of the globally optimal route.

## Important project notes
- The included books and library layout are sample data. Replace them with data collected or designed by your team.
- Edge weights are example walking-cost units, not measured metres.
- The sample A* heuristic uses approximate drawing coordinates. For a formally guaranteed optimal A* route, ensure the heuristic never overestimates the actual remaining cost. You can use `h(n) = 0` to make A* behave like Dijkstra's algorithm.
- The time budget uses route-cost units as a simplified estimate. A real deployment could convert measured walking distances into minutes.
- The app is a prototype, not connected to a university's actual catalogue or live inventory.

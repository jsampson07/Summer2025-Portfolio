
Below is a **11-week Summer 2025 roadmap** (May 28 – Aug 16) that balances **hands-on portfolio projects** with the extra learning time you need for unfamiliar technologies. Each week’s bullets are in dependency order. I’ve budgeted the fact that you may spend **20–30 hrs/week** but like to learn at a comfortable pace. Feel free to scale any week’s tasks up or down.

---

3. **DS&A Focus: BST & Hash Map**
   - **Mini-exercise:** load `/usr/share/dict/words` into your hash map and do O(1) lookups (simulate a wordlist check).

---

## Week 3: June 17 – 23  
**Goal:** Build and refine your **Port & Vulnerability Scanner** project.

1. **Combine Scripts into Port Scanner**  
   - In a new repo `vuln_scanner/`, start with `ping_sweeper.py` and add a **TCP-connect scan** fallback (if ICMP fails) using Python’s `socket` library.  
   - Accept flags: `--subnet`, `--ports` (e.g., `--ports 22,80,443`), and `--timeout`.  
   - **Deliverable:** `port_scanner.py` that prints a Python list/dict of `{ ip: [open_ports] }`.

2. **Add Service Fingerprinting**  
   - Use the `requests` library (install via `pip install requests`) to issue `HEAD` or `GET` to `http://<ip>:80/` for any found HTTP port; parse `Server:` header.  
   - For SSH (port 22), open a raw TCP socket, send a newline, and read the banner.  
   - **Deliverable:** update `vuln_scanner.py` to output JSON:
     ```jsonc
     {
       "ip": "192.168.1.5",
       "open_ports": [22, 80],
       "server_banner": "nginx/1.18.0"
     }
     ```

3. **DS&A Focus: Graph Traversals**  
   - Read **CLRS Ch 22 (BFS & DFS)** (2–3 hrs) and implement each in Python or C.  
   - **Mini-exercise:** treat each discovered host as a node; if host A and host B both have port 80 open, connect them as adjacent. Use BFS to find the shortest “multi-host chain” from one IP to another, or DFS to list all connected hosts.

4. **Debugging Drill**  
   - Introduce a bug in your scanner (e.g., mishandle a closed port timeout). Use `print()` logs and optionally run the Python process under `gdb` (for Python C-extension debugging) to trace the crash.  
   - **Deliverable:** a 200-word “What surprised me about debugging network code” journal entry.

5. **CI & Linting (GitHub Actions)**  
   - Add a `.github/workflows/lint.yml` that runs `flake8` or `pylint` on `vuln_scanner.py` when you push or open a PR.  
   - Fix any lint errors until your code is “lint-clean.”

---

## Week 4: June 24 – 30  
**Goal:** Enhance vuln scanner with async/greedy and tie in DS&A; optional exploit demo.

1. **Async/Concurrent Scanning**  
   - Update `vuln_scanner.py` to use `asyncio` with `aiohttp` (or Python’s `concurrent.futures.ThreadPoolExecutor`) for concurrent port checks.  
   - Compare times: sync vs async on 20 hosts × 3 ports. Print a simple timing table.  
   - **Deliverable:** `vuln_scanner_async.py` plus a brief note on the speedup.

2. **DS&A Focus: Greedy Scheduling**  
   - Read **KT Ch 1 (Greedy Algorithms)** (1–2 hrs) and implement the **Activity-Selection** problem in Python.  
   - **Mini-exercise:** assign each discovered host a “priority score” (e.g., number of open ports), and modify `vuln_scanner_async.py` so it scans higher-priority hosts first (greedy).  

3. **JSON Report Output**  
   - Have `vuln_scanner_async.py` write a final JSON file (`report.json`) summarizing each host’s IP, open ports, and server_banner.  
   - Example:
     ```jsonc
     {
       "scanned_subnet": "192.168.1.0/24",
       "hosts": [
         { "ip":"192.168.1.5","open_ports":[22,80],"server_banner":"nginx/1.18.0" },
         …
       ],
       "duration_seconds": 8.72
     }
     ```

4. **Optional Exploit Demo**  
   - Stand up a toy Flask app with a trivial SQL injection vulnerability (e.g., `SELECT * FROM users WHERE name = '%s'`).  
   - Write a short Python script (`exploit_demo.py`) that injects `' OR '1'='1` and prints “Login as admin.”  
   - **Deliverable:** 1-page write-up and the exploit script.

5. **CI & Tests (Linting Extended)**  
   - Extend your GitHub Actions to also run a **unit test** for a small function in your scanner (e.g., a function that parses JSON output).  
   - If you don’t yet know pytest, write a simple `assert parse_json(…)` test in an ad hoc `test_scanner.py`.

---

## Week 5: July 1 – 7  
**Goal:** Learn Web & Flask fundamentals; start backend CRUD with DS&A integration.

1. **Web Fundamentals & REST Design**  
   - Spend 4–5 hrs reading a concise “REST API Design” guide (e.g., [RESTful API Design Tutorial](https://www.restapitutorial.com/)). Understand HTTP verbs, status codes, and JSON payloads.  
   - **Mini-exercise:** sketch on paper the endpoints for a “Book Wishlist” service:  
     - `GET /api/books`, `POST /api/books`, `GET /api/books/<id>`, etc.  
     - `POST /api/login`, `POST /api/register`, `GET /api/wishlist`, etc.

2. **Flask Basics (Hands-On)**  
   - Over 4–6 hrs, go through **Miguel Grinberg’s Flask Mega-Tutorial Intro** (first 3 lessons):  
     - Install Flask, create a minimal “Hello World” app (`app.py`).  
     - Run `flask run` and hit `http://localhost:5000/`.  
     - Add a simple route `/api/books` that returns a static JSON list of books.  
   - **Deliverable:** a GitHub repo `flask_crud_app` with a barebones Flask app and a README explaining how to run.

3. **DS&A Focus: Merge Sort Integration**  
   - Read **KT Ch 2 (Divide & Conquer)** (1–2 hrs) and implement **Merge Sort** on a list of book titles in Python.  
   - In your Flask app’s `/api/books` route, add an optional query parameter (`?sort=merge`) that sorts the static list via your Merge Sort before returning JSON.  
   - **Deliverable:** proof that `/api/books?sort=merge` returns a sorted list.

4. **Database Setup: SQLAlchemy & Alembic Intro**  
   - Install **SQLAlchemy** and **Flask-SQLAlchemy** (2 hrs). Define a `Book` model with `id`, `title`, `author`.  
   - Install **Alembic** and generate an initial migration to create the `books` table in SQLite.  
   - **Deliverable:** a working `alembic upgrade head` that creates your table; include a simple Python script (`db_seed.py`) to insert two sample rows.

---

## Week 6: July 8 – 14  
**Goal:** Build the Flask REST API with JWT auth, caching (DS&A), and unit tests.

1. **REST API Endpoints & JWT**  
   - In `flask_crud_app/`, expand to include:  
     - `POST /api/register` → create a new `User` (hash password with `werkzeug.security.generate_password_hash`).  
     - `POST /api/login` → verify credentials, return a JWT using **Flask-JWT-Extended** (`pip install flask-jwt-extended`).  
     - Protect routes (`@jwt_required()`) for:  
       - `GET /api/books` (list all books)  
       - `POST /api/books` (add new book)  
       - `GET /api/wishlist` (list logged-in user’s wishlist)  
       - `POST /api/wishlist` (add book to wishlist)  
   - **Deliverable:** a working API where only authenticated users can add or view their wishlist.

2. **DS&A Focus: Caching with LRU (Hash Map + Doubly Linked List)**  
   - Over 3–4 hrs, implement an **LRU cache** in Python: use a hash map mapping keys to nodes in a doubly linked list.  
   - Integrate it into `GET /api/books`:  
     - If the user requests `/api/books?sort=merge`, on the first call run Merge Sort; on subsequent calls (within 30 sec) return cached data (O(1)).  
   - **Mini-exercise:** measure the speedup between cold cache vs. warm cache responses (e.g. 200 ms vs 20 ms) and log them.

3. **Unit Testing with pytest**  
   - Install `pytest` and `pytest-cov`. Over 3–4 hrs:  
     - Write `tests/test_auth.py` to check registration/login flows (valid vs invalid).  
     - Write `tests/test_books.py` to check `GET /api/books` with and without JWT, and caching behavior.  
     - Run:
       ```
       pytest --cov=flask_crud_app tests/
       ```
     - Ensure coverage on your service modules is **≥ 80%**.

4. **CI Integration**  
   - Add `.github/workflows/ci.yml` that:  
     1. Checks out code.  
     2. Runs `flake8` on Python.  
     3. Installs requirements and runs `pytest --cov`.  
   - Ensure every push/PR triggers a green CI pass before merging.

5. **OS Concepts Light Read**  
   - Read **OSTEP Ch 1 (What Is an OS?)** and **Ch 2 (Processes & Threads)**.  
   - Write a 300-word bullet-point summary: “From user-mode `read()` to disk I/O” (no coding—just the conceptual path).

---

## Week 7: July 15 – 21  
**Goal:** Learn JavaScript basics, React introduction, and start building the front-end.

1. **JavaScript (ES6+) Basics**  
   - Spend ~8 hrs on a concise JavaScript tutorial (e.g., MDN “JavaScript Guide” or a 10-hr Codecademy JS track). Cover:  
     - Variables (`let/const`), arrow functions, promises/async-await, `fetch` API, and basic DOM manipulation.  
   - **Mini-exercise:** write `js_basics.js` that fetches `https://jsonplaceholder.typicode.com/posts` and logs the titles of the first 5 posts.

2. **React Fundamentals**  
   - Over ~10 hrs, follow a beginner React tutorial (e.g., Create-React-App Quickstart):  
     - Install Node.js & `npx create-react-app frontend`.  
     - Build a simple component `<App />` that displays “Hello, React.”  
     - Learn **functional components** and **hooks** (`useState`, `useEffect`).  
   - **Deliverable:** a repo `flask_frontend/` containing a barebones React app that runs `npm start` and shows “Welcome to My Front-End.”

3. **Integrate with Static Data**  
   - In your React app, create a component that `fetch("/api/books")` from your local Flask server (you can proxy through `package.json`).  
   - Display the returned JSON list of books in a `<ul>`.  
   - **Deliverable:** React shows a list of static books when the Flask server is running locally.

4. **DS&A Focus (Optional)**  
   - If you finish early, revisit **Merge Sort** or **LRU Cache** in JavaScript—implement them in your React code, even if you don’t yet call your Flask API.

5. **OS Concepts: Memory Virtualization Light**  
   - Read **OSTEP Ch 4 (Memory & Virtualization Basics)** (2–3 hrs): focus on paging and virtual vs physical addresses.  
   - Draw a simple diagram of “virtual→physical” address translation using a single-level page table.

---

## Week 8: July 22 – 28  
**Goal:** Connect React front-end to Flask API, learn Docker basics, and containerize the backend.

1. **React → Flask Integration**  
   - Modify your React state so that on mount (`useEffect`), it calls `fetch("http://localhost:5000/api/books")` with the JWT token (if logged in).  
   - Create simple **Login/Register** forms:  
     - Submit to `POST /api/register` and `POST /api/login`.  
     - On success, store the returned JWT in `localStorage`.  
   - Build a **Wishlist Page**: fetch `GET /api/wishlist` (using `Authorization: Bearer <JWT>`) and display items.  
   - **Deliverable:** A two-page React app (Login/Register & Wishlist) that fully talks to your Flask API.

2. **Docker Basics**  
   - Spend ~6 hrs learning Docker:  
     - Write a simple `Dockerfile` for your Flask app.  
     - Build with `docker build -t flask_api .` and run with `docker run -p 5000:5000 flask_api`.  
   - Write a `docker-compose.yml` that brings up:  
     ```yaml
     version: '3'
     services:
       db:
         image: postgres:13
         environment:
           POSTGRES_USER: youruser
           POSTGRES_PASSWORD: yourpass
           POSTGRES_DB: summerdb
         ports:
           - "5432:5432"

       api:
         build: ./flask_crud_app
         ports:
           - "5000:5000"
         depends_on:
           - db
         environment:
           DATABASE_URL: postgres://youruser:yourpass@db:5432/summerdb
           JWT_SECRET_KEY: your_secret_key
     ```
   - **Deliverable:** `docker-compose up --build` starts both your DB and API.

3. **DS&A Focus: Graph Flows (Optional)**  
   - If time permits (~3 hrs), read **KT Ch 4 (Network Flows)** and implement a simple **Ford-Fulkerson** max-flow in Python.  
   - **Mini-exercise:** model your Docker network (API <→ DB) as a flow graph with capacity = some constant and compute max flow.

---

## Week 9: July 29 – Aug 4  
**Goal:** Finish containerizing full stack (React + Flask), deploy, and perform performance tuning.

1. **Containerize React Front-End**  
   - In `flask_frontend/`, write a `Dockerfile`:  
     ```dockerfile
     # Stage 1: build
     FROM node:16 AS build
     WORKDIR /app
     COPY package.json yarn.lock ./
     RUN yarn install
     COPY . .
     RUN yarn build

     # Stage 2: serve with nginx
     FROM nginx:alpine
     COPY --from=build /app/build /usr/share/nginx/html
     ```
   - Update `docker-compose.yml` to include:
     ```yaml
       frontend:
         build: ./flask_frontend
         ports:
           - "3000:80"
         depends_on:
           - api
     ```
   - Run `docker-compose up --build`: you should have  
     - **DB** on 5432,  
     - **API** on 5000,  
     - **Front-End** on 3000.  
   - **Deliverable:** full stack running locally in Docker.

2. **Deployment**  
   - Tag and push your `flask_api` Docker image to Docker Hub or GitHub Container Registry.  
   - **Deploy API** to Heroku (Container Registry) or a free VPS (e.g., using Docker Compose on an AWS t2.micro):  
     - Set environment variables: `DATABASE_URL`, `JWT_SECRET_KEY`.  
   - **Deploy Front-End** to Netlify (drag-n-drop the `build` folder) or host on the same VPS behind nginx.  
   - **Deliverable:** public URLs for both API (e.g. `https://my-api.herokuapp.com`) and front-end (e.g. `https://my-app.netlify.app`).

3. **Performance Tuning (Python & Docker)**  
   - Re-run your **vuln_scanner_async.py** under `/usr/bin/time` or Python’s `timeit`—document how long a 20-host scan takes.  
   - In your **Flask API**, measure average response time for `GET /api/books` (cold vs warm cache).  
   - Adjust:  
     - If scan is slow, increase concurrency or batch size.  
     - If API is slow, add indexes in SQL (or optimize your merge sort vs Python’s `sorted()` fallback).  
   - **Deliverable:** a 200-word “Lessons Learned” about performance improvements.

---

## Week 10: Aug 5 – Aug 11  
**Goal:** Polish everything, write documentation, and finalize your portfolio site.

1. **Project Polish & Blog Posts**  
   - For each repo (**vuln_scanner**, **flask_crud_app**, **flask_frontend**, and your **DSA-Challenges**), write a **Medium-style post** (or Markdown) that covers:  
     - **Problem statement** (e.g., “Why I built a Vuln Scanner”)  
     - **Architecture & key technologies** (Scapy, asyncio, Flask, React, Docker)  
     - **DS&A tie-ins** (which algorithms you used where and why)  
     - **Screenshots + sample output** (e.g., JSON report, front-end UI).  
   - Aim for **500–700 words** each, with diagrams for the Flask API flow and Docker-Compose network.

2. **DS&A Focus: Pattern Matching**  
   - Implement **Knuth–Morris–Pratt (KMP)** in Python (2–3 hrs).  
   - **Mini-exercise:** integrate it into `vuln_scanner.py` to search HTTP response bodies for known CVE signature strings (maintain a small text file of vulnerable substrings).  
   - Document how KMP’s O(n + m) time improves over naive O(n·m).

3. **Finalize DSA Solutions**  
   - In a repo `DSA-Challenges`, push your key implementations from Weeks 0–9:  
     - Dynamic Array, Linked List, Stack/Queue, Heap, BST, Hash Map, Merge Sort, QuickSelect, BFS/DFS, Max-Flow, DP (Fibonacci), Greedy (Activity-Selection), LRU cache, KMP, Radix Sort, plus **5 LeetCode Medium** solutions.  
   - Ensure each has a `README.md` summarizing time/space complexity.

4. **Prepare Your Portfolio Site (GitHub Pages)**  
   - Create a new repo `Summer2025-Portfolio-Site` and enable Pages on `main` (via `Settings → Pages`).  
   - Write a simple `index.html` or use a Jekyll template to link to:  
     - **Vuln Scanner**: GitHub + demo instructions  
     - **Full-Stack App**: GitHub + live URL  
     - **DSA-Challenges**: GitHub link  
   - Include a short bio and a “Contact Me” section.

---

## Week 11: Aug 12 – Aug 16  
**Goal:** Reflect, rehearse, and prep for Fall.

1. **Rehearse Project Demos**  
   - Draft a **2-minute elevator pitch** for each project:  
     1. **Vuln Scanner**: problem, approach (Scapy, asyncio, DS&A), sample output.  
     2. **Flask Full-Stack App**: REST design, JWT auth, caching with LRU, React front-end, Docker-Compose, deployment.  
     3. **DSA Exhibits**: why each data structure/algorithm matters (e.g., KMP for fast log scanning).

2. **“Lessons Learned” Reflections**  
   - For each domain—**Cybersecurity**, **Software Dev**, **DS&A**, **OS Concepts Review**—write a **200-word summary**:  
     - What you knew vs. what you learned.  
     - Biggest surprises or pain points.  
     - Next steps heading into **Advanced OS** (Fall 2025).

3. **Clean Up & Archive**  
   - Delete or archive any throwaway Git branches you used for experiments.  
   - Make a final commit: update the `Summer2025-Portfolio-Site` repo’s index with all project links, live URLs, and blog links.  
   - **Celebrate**: take a day off, review everything you’ve built, and enjoy shipping three polished, deploy­­­­ed portfolio projects.

4. **Makefile Basics**  
   - Read a concise guide (e.g. [Makefile Tutorial](https://makefiletutorial.com/)) over 2–3 hrs. Learn targets, dependencies, and variables.  
   - Hand-write a simple **Makefile** in `project-scaffold/` that builds a C “hello world”:
     ```makefile
     CC = gcc
     CFLAGS = -Wall -g

     all: hello

     hello: hello.o
         $(CC) $(CFLAGS) -o hello hello.o

     hello.o: hello.c
         $(CC) $(CFLAGS) -c hello.c

     clean:
         rm -f hello hello.o
     ```
   - Run `make all`, `./hello`, then `make clean` to verify.

5. **OS Concepts: System Calls Walkthrough**  
   - Skim **xv6’s** `syscall.c`, `usys.S`, and `trap.c` (in `/xv6-public/`). No coding—just add comments explaining how `open()` or `exit()` goes from user to kernel.  
   - Write a 200-word bullet summary: “What happens when user code calls `fork()` in xv6?” (identify `sys_fork`, `allocproc`, scheduler handoff).

6. **ADD Binary Search Algorithm to CLI-todo list Application**
---

## Prerequisites & Timing Guidance

Because many of these technologies are new to you, here’s a **rough breakdown of prerequisite learning** (parallel to Weeks 0–2). You can spread these hours over the weeks as needed; just ensure you’ve got the core skill before each deliverable.

| Skill/Topic                           | Rough Hours | When to Tackle           |
|---------------------------------------|-------------|--------------------------|
| **Shell Scripting Basics**            | 4–6 hrs     | Week 0 (Linux CLI week)  |
| **RESTful API Design Principles**     | 4–5 hrs     | Week 5 (before Flask)    |
| **Flask Web Framework Basics**        | 8–10 hrs    | Weeks 5–6                |
| **JavaScript (ES6+) Essentials**      | 10–12 hrs   | Week 7                   |
| **React Fundamentals**                | 15–20 hrs   | Weeks 7–8                |
| **Docker & Docker-Compose Basics**     | 8–10 hrs    | Weeks 8–9                |
| **pytest & Unit Testing**             | 4–6 hrs     | Week 6                   |
| **Scapy Packet Library**              | 3–5 hrs     | Week 2                   |
| **DS&A Review (Implementing Key DSAs)** | 25–30 hrs   | Spread Weeks 0 – 9       |

- **If you already know Python, C, and Java**, you may cut **15–20 hrs** from the Python/DSA total.  
- **If you’ve never used React**, expect the full **15–20 hrs** in Weeks 7–8.  
- **Docker** can be picked up in a weekend; allocate **8 hrs** in Week 8.  
- **Scapy** you’ll learn in ~3 hrs (Week 2), then apply immediately in the scanner.

### Weekly Time Estimate

- **Weeks 0–2 (Foundation + Core DSA + Scapy):**  **20–25 hrs/week** (prereqs + initial projects)  
- **Weeks 3–4 (Vuln Scanner + DS&A integration):**  **20–30 hrs/week**  
- **Week 5 (Flask Intro + DS&A merge sort):**  **25–30 hrs** (lots of new material)  
- **Week 6 (REST API, JWT, pytest):**  **25–30 hrs**  
- **Week 7 (JavaScript + React Intro):**  **25–30 hrs** (React is steep)  
- **Week 8 (React→Flask integration + Docker basics):**  **20–25 hrs**  
- **Week 9 (Full Docker-Compose + Deployment + tuning):**  **20–25 hrs**  
- **Week 10 (Polish, blog posts, DSA patterns):**  **20 hrs**  
- **Week 11 (Reflection & buffer):**  **10–15 hrs**  

---

### What You’ll End Up With

- **Cybersecurity Portfolio Tool**  
  - **vuln_scanner_async.py**: a robust Python 3 tool (Scapy, asyncio/threading, requests, DS&A-powered greedy scheduling, KMP pattern matching) that outputs a structured JSON report and flags known CVEs.  
  - **exploit_demo.py**: proof-of-concept for a trivial web vulnerability.  
  - **GitHub repo** with README, examples, lint/tests via GitHub Actions.

- **Full-Stack Authenticated App**  
  - **Flask API** (`flask_crud_app`): SQLAlchemy models (User/Book/Wishlist), JWT auth, LRU cache, unit tests (pytest ≥ 80% coverage), containerized in Docker.  
  - **React Front-End** (`flask_frontend`): Login/Register, Book Dashboard, Wishlist Dashboard, communicates with Flask via JWT, deployed on Netlify (or integrated behind nginx).  
  - **docker-compose.yml**: brings up Postgres, Flask API, and React front end.  
  - **Deployed URLs**: public endpoints you can link on your resume.

- **DSA-Challenges**  
  - A **gated collection** of 15–20 handwritten DS&A implementations (arrays, lists, heap, BST, hash map, merge sort, quickselect, BFS/DFS, max-flow, DP, greedy, KMP, radix sort).  
  - **5 LeetCode Medium solutions** (one from array, linked list, tree/graph, DP, greedy/sorting), each with a brief complexity analysis.

- **Portfolio Site**  
  - A simple GitHub Pages site linking to all code repos, live demos, and blog posts—polished and ready to share with recruiters.

By following this slower-paced, **30 hrs/week** (or flex down to **20 hrs/week** if you want breathing room), you’ll not only produce three **professional, portfolio-worthy projects** but also gain deep mastery over each new tool—**Flask**, **JWT**, **Docker**, **React**, **pytest**, **Scapy**, and a broad spectrum of **DS&A**. That puts you in a great position for Fall 2025 and beyond. Good luck!

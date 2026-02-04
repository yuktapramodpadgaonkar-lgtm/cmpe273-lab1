# CMPE 273 – Week 1 Lab 1: Your First Distributed System (Starter)

This starter provides two implementation tracks:
- `python-http/` (Flask + requests)
- `go-http/` (net/http)

Pick **one** track for Week 1.

## Lab Goal
Build **two services** that communicate over the network:
- **Service A** (port 8080): `/health`, `/echo?msg=...`
- **Service B** (port 8081): `/health`, `/call-echo?msg=...` calls Service A

Minimum requirements:
- Two independent processes
- HTTP (or gRPC if you choose stretch)
- Basic logging per request (service name, endpoint, status, latency)
- Timeout handling in Service B
- Demonstrate independent failure (stop A; B returns 503 and logs error)

## How to Run Locally - PYTHON HTTP TRACK

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd lab1-repo
   ```

2. **Switch to the desired branch**
   ```bash
   git checkout <branch-name>
   ```

3. **Navigate to Python HTTP directory**
   ```bash
   cd cmpe273-week1-lab1-starter/python-http
   ```

4. **Setup Service A (one-time setup)**
   ```bash
   cd service-a
   python -m venv .venv
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Setup Service B (one-time setup)**
   Open a new terminal:
   ```bash
   cd service-b
   python -m venv .venv
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Running the Services

**Important:** Dependencies only need to be installed once. After initial setup, you just need to activate the virtual environment and run the app.

**Service A:**
```bash
cd service-a
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or: source .venv/bin/activate  # macOS/Linux
python app.py
```

**Service B (in a new terminal):**
```bash
cd service-b
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or: source .venv/bin/activate  # macOS/Linux
python app.py
```

For detailed setup instructions, see [`python-http/README.md`](python-http/README.md).

## Testing

### Success Case

Test Service B calling Service A successfully:

```bash
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```

**Expected Response:**
```json
{
  "service_b": "ok",
  "service_a": {
    "echo": "hello"
  }
}
```

### Failure Case

1. Stop Service A (press `Ctrl+C` in Service A terminal)
2. Run the same curl command:
   ```bash
   curl "http://127.0.0.1:8081/call-echo?msg=hello"
   ```

**Expected Response:**
```json
{
  "service_b": "ok",
  "service_a": "unavailable",
  "error": "<connection error details>"
}
```

**HTTP Status:** 503 Service Unavailable

This demonstrates independent failure handling - Service B continues running and gracefully handles Service A's unavailability.

## What Makes This Distributed?

A distributed system is a system where:
- multiple independent processes
- communicate over a network
- coordinate to perform a task
- and can fail independently

They do not share memory and do not run as a single program.

### Why Your System is Distributed (Even on One Laptop)

We have two services on one laptop but the important part is how they interact, not where they run.

#### 1. They are Two Independent Processes

- Service A runs as one Python process (port 8080)
- Service B runs as a different Python process (port 8081)
- They are started separately, stopped separately, and crash separately
- This alone breaks the "single program" model.

#### 2. The Network Communication (Not Function Calls)

Service B does not call a function inside Service A.
Instead, it uses `requests.get("http://127.0.0.1:8080/echo", timeout=1.0)`

That means:
- data is serialized to HTTP
- sent via TCP/IP
- goes through the OS networking stack
- is deserialized on the other side

This introduces:
- latency
- packet loss possibility
- timeouts
- connection failures

Those problems do not exist in a single-process program.

#### 3. There is No Shared Memory

Service A and B:
- do not share variables
- do not share heap or stack
- cannot directly access each other's state

The only way they communicate is via HTTP messages.

#### 4. Independent Failure (Critical)

This is the strongest proof.

You can stop Service A, Service B keeps running.

Service B must detect failure via:
- timeout
- connection error
- Service B returns 503 Service Unavailable

That behavior is impossible in a monolithic app.

This directly demonstrates a core distributed systems property:
**Components fail independently and must handle partial failure.**

#### 5. Explicit Timeouts

In Service B: `timeout=1.0`

Why this matters:
- network calls can hang forever
- distributed systems must bound waiting
- timeouts are unnecessary in local function calls

This line exists only because the system is distributed.

#### 6. Separate Observability (Logging)

Each service:
- logs independently
- has its own latency measurements
- has its own error context

In real distributed systems, logs are often the only way to debug failures across services.

### Both Systems are on Localhost, But...

**Distribution is about architecture, not geography.**

- **Today:** both services run on localhost
- **Tomorrow:** Service A could run on another machine
- Service B wouldn't change — just the host/port
- That's exactly how real systems are designed.

## Deliverables
1. Repo link
2. README updates:
   - ✅ how to run locally
   - ✅ success + failure proof (curl output or screenshot)
   - ✅ "What makes this distributed?" section

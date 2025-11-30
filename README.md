# **Messaging Microservice (FastAPI + Cloud SQL)**

This repository provides the **atomic Messaging Microservice** for the Neighborhood Exchange project (COMS4153). It exposes a standalone API responsible for **threads**, **messages**, and **thread–user relationships**.

It does **not** authenticate users. Authentication is handled by the **Composite Microservice**, which forwards valid, authorized requests here.

---

## **Key Features**

### **1. Threads**
- Create and retrieve message threads  
- Auto-generated UUIDs  
- Tracks author and participant IDs  
- Stores timestamps for creation and updates  

### **2. Messages**
- Post messages to a thread  
- Retrieve full message history  
- Sorted chronologically  
- Validates that the thread exists  

### **3. Thread–User Linking**
- Maintains mapping between users and threads  
- Supports:
  - Listing users in a thread  
  - Listing threads for a user  
- Enables composite services to build richer messaging UI  

### **4. Logging**
- Cloud Run–ready structured logging  
- Logs:
  - All HTTP requests  
  - Database operations  
  - Thread/message creation  
  - Errors & exceptions  
- Organized with module-level loggers  

### **5. Database Integration**
- MySQL on Cloud SQL  
- Async SQLAlchemy (`aiomysql`)  
- Automatic table creation on startup  
- Environment-based configuration  

---

## **No Internal Authentication**

This microservice does **not** validate JWTs.

Instead:
- The **Composite Microservice** authenticates all incoming requests  
- This service trusts the forwarded user info  
- `sender_id`, `author_id`, and other fields must be provided by the composite layer  

This keeps the microservice **atomic**, **stateless**, and **independent**.

---

## **Local Development**

### **1. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate

### **2. Install dependencies**
pip install -r requirements.txt

### **3. Run locally**
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

### **3. Open API docs**
http://localhost:8000/docs

## **API Overview**

### **Threads**
| Method | Path | Description |
|--------|------|-------------|
| POST   | /threads/                | Create a new thread |
| GET    | /threads/{thread_id}     | Retrieve a thread by ID |

### **Messages**
| Method | Path | Description |
|--------|------|-------------|
| POST   | /threads/{thread_id}/messages | Send a message |
| GET    | /threads/{thread_id}/messages | Get all messages in a thread |

## **Requirements**

See requirements.txt.
Typical dependencies include:
- fastapi
- uvicorn
- sqlalchemy
- aiomysql
- pydantic
- python-dotenv
- greenlet




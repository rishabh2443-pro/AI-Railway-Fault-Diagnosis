\# 🚆 AI-Based Railway Fault Diagnosis \& Monitoring System



An intelligent railway monitoring system that collects real-time sensor data, detects possible faults, evaluates risk levels, and generates AI-based diagnosis and maintenance recommendations.



\## 🎯 Project Objective



The main objective of this project is to monitor railway/train sensor parameters and identify abnormal conditions at an early stage.



The system combines:



\- IoT sensor simulation

\- MQTT communication

\- Python backend

\- PostgreSQL database

\- Rule-based fault detection

\- RAG-based knowledge retrieval

\- Local LLM using Ollama

\- Streamlit dashboard



\## 🏗️ System Architecture



Sensor Simulator  

↓  

MQTT Broker  

↓  

Python MQTT Subscriber  

↓  

PostgreSQL Database  

↓  

Fault Detection  

↓  

RAG Knowledge Base  

↓  

Ollama LLM  

↓  

AI Diagnosis \& Recommendation  

↓  

Streamlit Dashboard



\## ⚙️ Technologies Used



| Technology | Purpose |

|---|---|

| Python | Backend and processing |

| MQTT | Sensor data communication |

| Paho MQTT | MQTT client |

| PostgreSQL | Data storage |

| FAISS | Vector similarity search |

| Sentence Transformers | Text embeddings |

| Ollama | Local LLM |

| Streamlit | Web dashboard |

| Pandas | Data processing |



\## 📡 Sensor Parameters



The system monitors:



\- Speed

\- Vibration

\- Temperature

\- Brake Pressure



\## 🚨 Fault Detection



The current rule-based fault detection uses the following thresholds:



| Parameter | Condition | Fault |

|---|---|---|

| Vibration | > 4 | High Vibration |

| Temperature | > 75 | High Temperature |

| Brake Pressure | < 65 | Low Brake Pressure |

| Speed | > 95 | High Speed |



\### Risk Levels



\- \*\*LOW\*\* → No detected fault

\- \*\*MEDIUM\*\* → 1 detected fault

\- \*\*HIGH\*\* → 2 or more detected faults



\## 🤖 AI Diagnosis



The system uses a local Ollama LLM to generate an AI-based diagnosis.



The AI uses:



1\. Latest sensor readings

2\. Detected faults

3\. Fault risk level

4\. Retrieved railway fault knowledge

5\. Maintenance information



The system generates:



\- Fault diagnosis

\- Possible causes

\- Recommended action

\- Safety advice



\## 🧠 RAG System



The project uses Retrieval-Augmented Generation (RAG).



The knowledge base contains railway fault information such as:



\- High Vibration

\- High Temperature

\- Low Brake Pressure

\- High Speed



Sentence Transformers generate embeddings and FAISS performs similarity-based retrieval.



The retrieved information is then provided to the local LLM for diagnosis.



\## 📂 Project Structure



```text

my projectt/

│

├── config/

├── dashboard/

├── Data/

├── database/

├── fault\_detection/

├── knowledge/

├── llm/

├── mqtt/

├── rag/

├── simulator/

├── venv/

│

├── ai\_diagnosis.py

├── app.py

├── insert\_sensor.py

├── live\_fault\_detector.py

├── mqtt\_publisher.py

├── mqtt\_subscriber.py

├── rag\_engine.py

├── test\_db.py

├── requirements.txt

└── README.md


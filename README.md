# AI Personal Health Assistant

## Project Overview
AI Personal Health Assistant is a Streamlit-based healthcare application that helps users manage their daily health activities. It allows users to track medications, monitor fitness data, and get basic health information through an AI chatbot.

## Features
- 💊 Medication Tracker
- 🏃 Fitness Tracker
- 🤖 AI Health Chatbot
- 📊 Health Dashboard
- 💾 SQLite Database

## Technologies Used
- Python
- Streamlit
- SQLite
- LangChain
- Pandas
- Plotly

## Project Structure

AI_Health_Assistant/
│
├── app.py
├── database.py
├── medicine.py
├── health_api.py
├── health_chatbot.py
├── requirements.txt
├── README.md
└── health.db

## How to Run

1. Install the required libraries:

```
pip install -r requirements.txt
```

2. Create the database:

```
python database.py
```

3. Run the application:

```
streamlit run app.py
```

## Future Improvements
- Google Fit API Integration
- Medicine Reminder Notifications
- Health Reports and Charts
- AI-powered Medical Suggestions

## Author
Madival Vaishnavi
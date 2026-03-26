# Blockchain-Based Event Detection & Trust Verification

## Overview

This project focuses on detecting fake news and verifying trust using a combination of **Machine Learning (NLP)** and **Blockchain technology**.
It aims to enhance **data integrity, transparency, and reliability** in digital content systems.

---

## Features

* Fake news detection using Machine Learning (NLP)
* Blockchain-based trust verification
* Web-based interface for user interaction
* Real-time prediction and validation
* Dataset-driven model training

---

## Tech Stack

* **Programming Language:** Python
* **Framework:** Django
* **Machine Learning:** NLP (Text Classification)
* **Blockchain:** Solidity (Smart Contracts)
* **Database:** SQLite

---

## Project Structure

```
Trust_Verification/
│── Dataset/              # Training and testing data
│── FakeMedia/            # Media-related data
│── FakeMediaApp/         # Django application
│── model/                # ML model files
│── screenshots/          # Project screenshots
│── manage.py             # Django entry point
│── FakeMedia.json        # Data file
│── FakeMedia.sol         # Smart contract
│── db.sqlite3            # Database
│── test.py               # Testing script
```

---

## Installation & Setup

### 1️.Clone the repository

```
git clone https://github.com/YOUR_USERNAME/Trust-Verification.git
cd Trust-Verification
```

### 2️.Install dependencies

```
pip install -r requirements.txt
```
---

### 3️.Run the project

```
python manage.py runserver
```

Open browser:

```
http://127.0.0.1:8000/
```

---

## Screenshots

### Home Page
![homepage](screenshots/homepage.png.png)

### Login Page
![login_page](screenshots/login_page.png.png)

### ML Scoring
![ML_scoring](screenshots/ML_scoring.png.png)

### Upload News
![Upload_news](screenshots/Upload_news.png.png)

---

## How It Works

1. User inputs news/content
2. NLP model analyzes text
3. System classifies content as real/fake
4. Blockchain ensures tamper-proof verification
5. Results displayed on web interface

---

## Use Cases

* Fake news detection platforms
* Social media verification systems
* News authentication tools
* Crisis management systems

---

## Future Enhancements

* Improve model accuracy with deep learning
* Deploy on cloud (AWS / Azure)
* Add REST API support
* Integrate real-time blockchain networks

---

## 👨‍💻 Author

**Ayman Rais**

---

This project is open-source and available under the MIT License.

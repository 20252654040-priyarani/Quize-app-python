import os
import random
from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR)

QUESTIONS_PER_QUIZ = 15  # har baar itne random sawal aayenge


def Q(question, answer, others):
    return {"q": question, "answer": answer, "options": [answer] + others}


BANK = [
    Q("What is the capital of India?", "Delhi", ["Mumbai", "Kolkata", "Chennai"]),
    Q("Which planet is known as the Red Planet?", "Mars", ["Earth", "Venus", "Jupiter"]),
    Q("Who wrote the Ramayana?", "Valmiki", ["Tulsidas", "Kalidas", "Ved Vyas"]),
    Q("Which is the largest ocean?", "Pacific", ["Indian", "Atlantic", "Arctic"]),
    Q("HTML stands for?", "Hyper Text Markup Language", ["High Text Machine Language", "Hyper Tool Markup Language", "None of these"]),
    Q("Python is a?", "Programming Language", ["Snake only", "Game", "Operating System"]),
    Q("The Sun rises in the?", "East", ["North", "South", "West"]),
    Q("Which is the national animal of India?", "Tiger", ["Lion", "Elephant", "Leopard"]),
    Q("Which gas do we breathe in?", "Oxygen", ["Hydrogen", "Nitrogen", "Carbon Dioxide"]),
    Q("5 x 6 = ?", "30", ["25", "35", "40"]),
    Q("What is the chemical formula of water?", "H2O", ["CO2", "O2", "NaCl"]),
    Q("Which is the fastest land animal?", "Cheetah", ["Tiger", "Lion", "Horse"]),
    Q("India got independence in?", "1947", ["1945", "1950", "1930"]),
    Q("Who is known as the Father of the Nation?", "Mahatma Gandhi", ["Jawaharlal Nehru", "Subhas Chandra Bose", "Sardar Patel"]),
    Q("Who was the first Prime Minister of India?", "Jawaharlal Nehru", ["Mahatma Gandhi", "Lal Bahadur Shastri", "Indira Gandhi"]),
    Q("Which is the largest planet in our Solar System?", "Jupiter", ["Saturn", "Earth", "Neptune"]),
    Q("In which city is the Taj Mahal located?", "Agra", ["Delhi", "Jaipur", "Lucknow"]),
    Q("Which is the national bird of India?", "Peacock", ["Sparrow", "Parrot", "Eagle"]),
    Q("What is the currency of Japan?", "Yen", ["Won", "Dollar", "Yuan"]),
    Q("What is the chemical symbol of Gold?", "Au", ["Ag", "Gd", "Go"]),
    Q("Which is the hardest natural substance?", "Diamond", ["Iron", "Gold", "Quartz"]),
    Q("How many continents are there in the world?", "7", ["5", "6", "8"]),
    Q("Which is the longest river in India?", "Ganga", ["Yamuna", "Godavari", "Brahmaputra"]),
    Q("CPU stands for?", "Central Processing Unit", ["Central Program Utility", "Computer Personal Unit", "Core Power Unit"]),
    Q("Who invented the telephone?", "Alexander Graham Bell", ["Thomas Edison", "Nikola Tesla", "Isaac Newton"]),
    Q("What is the square root of 144?", "12", ["10", "14", "16"]),
    Q("Which is the largest country by area?", "Russia", ["Canada", "China", "India"]),
    Q("What is the smallest prime number?", "2", ["1", "3", "0"]),
    Q("Which is the national flower of India?", "Lotus", ["Rose", "Marigold", "Jasmine"]),
    Q("Who founded Microsoft?", "Bill Gates", ["Steve Jobs", "Elon Musk", "Mark Zuckerberg"]),
    Q("Which gas do plants absorb for photosynthesis?", "Carbon Dioxide", ["Oxygen", "Nitrogen", "Hydrogen"]),
    Q("What is the capital of Japan?", "Tokyo", ["Seoul", "Beijing", "Bangkok"]),
    Q("How many days are there in a leap year?", "366", ["365", "364", "367"]),
    Q("Which organ pumps blood in the human body?", "Heart", ["Lungs", "Liver", "Kidney"]),
    Q("Which is the highest mountain peak in the world?", "Mount Everest", ["K2", "Kanchenjunga", "Mount Kilimanjaro"]),
    Q("Who is known as the Missile Man of India?", "A.P.J. Abdul Kalam", ["Vikram Sarabhai", "Homi Bhabha", "C.V. Raman"]),
    Q("Which is the largest state of India by area?", "Rajasthan", ["Madhya Pradesh", "Maharashtra", "Uttar Pradesh"]),
    Q("15 + 27 = ?", "42", ["32", "41", "52"]),
    Q("At what temperature does water freeze (in Celsius)?", "0", ["10", "-10", "100"]),
    Q("Which language is used to style web pages?", "CSS", ["Python", "SQL", "Java"]),
    Q("Who wrote the Indian National Anthem?", "Rabindranath Tagore", ["Bankim Chandra Chatterjee", "Sarojini Naidu", "Premchand"]),
    Q("Which is the largest mammal?", "Blue Whale", ["Elephant", "Giraffe", "Shark"]),
    Q("Which planet is closest to the Sun?", "Mercury", ["Venus", "Earth", "Mars"]),
    Q("RAM stands for?", "Random Access Memory", ["Read Access Memory", "Run All Memory", "Rapid Action Module"]),
    Q("Who was the first man to walk on the Moon?", "Neil Armstrong", ["Buzz Aldrin", "Yuri Gagarin", "Rakesh Sharma"]),
    Q("Which festival is known as the Festival of Lights?", "Diwali", ["Holi", "Eid", "Baisakhi"]),
    Q("How many states are there in India?", "28", ["26", "29", "30"]),
    Q("Which vitamin do we get from sunlight?", "Vitamin D", ["Vitamin A", "Vitamin C", "Vitamin B12"]),
    Q("100 / 4 = ?", "25", ["20", "24", "30"]),
    Q("Which of these is a search engine?", "Google", ["Linux", "Windows", "Excel"]),
]

for i, item in enumerate(BANK):
    item["id"] = i

BANK_BY_ID = {item["id"]: item for item in BANK}


@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        raw_ids = request.form.get("ids", "")
        ids = [int(x) for x in raw_ids.split(",") if x.strip().isdigit() and int(x) in BANK_BY_ID]

        score = 0
        review = []
        for qid in ids:
            item = BANK_BY_ID[qid]
            user_ans = request.form.get(f"q{qid}")
            correct = user_ans == item["answer"]
            if correct:
                score += 1
            review.append({
                "q": item["q"],
                "your": user_ans,
                "answer": item["answer"],
                "correct": correct,
            })

        total = len(ids)
        percent = round(score * 100 / total) if total else 0
        return render_template("result.html", score=score, total=total, percent=percent, review=review)

    picked = random.sample(BANK, min(QUESTIONS_PER_QUIZ, len(BANK)))
    questions = []
    for item in picked:
        options = item["options"][:]
        random.shuffle(options)
        questions.append({"id": item["id"], "q": item["q"], "options": options})

    ids = ",".join(str(q["id"]) for q in questions)
    return render_template("index.html", questions=questions, ids=ids)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

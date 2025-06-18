from flask import Flask, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "tajna_lozinka_za_session"
app.permanent_session_lifetime = timedelta(minutes=30)


keywords = {
    "поздрав": ["здраво", "hello", "hi", "cao", "hej", "zdravo", "поздрав"],
    "стрес": ["стрес", "napnat","napnata" ,"napetost", "nervoza", "stres"],
    "осаменост": ["осамен","осамена","osamena", "сам", "osamen", "usamen", "sam"],
    "анксиозност": [
        "анксиоз", "ansioz", "ansioznost","anksiozna" "panika",
        "imam anksioznost", "имам анксиозност"
    ],
    "депресија": ["депрес", "depresija", "taga", "depresivno","tazen", "tazna"],
    "самодоверба": ["самодоверба", "samodoverba", "nesigurnost", "selfesteem", "sigurnost"]
}


responses = {
    "поздрав": "👋 Здраво! Како можам да ти помогнам денес?",
    "стрес": "🧘 Стресот е нормална реакција. Обиди се со длабоко дишење, прошетка или кратка медитација.",
    "осаменост": "👥 Поврзи се со пријатели или најди активности што ти носат радост – не си сам/а.",
    "анксиозност": "💓 Анксиозноста може да се намали со mindfulness, journaling и разговор со блиски. Тука сум за тебе.",
    "депресија": "🌧️ Разговор со стручно лице е многу важен чекор. Не мораш да се справуваш сам/а.",
    "самодоверба": "🌟 Потсети се на своите квалитети. Малите победи се големи чекори. Верувај си."
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        session["chat"] = []

    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        user_input = request.form["message"].strip()
        user_input_lower = user_input.lower()

        found = False
        for theme, words in keywords.items():
            if any(word in user_input_lower for word in words):
                bot_response = responses[theme]
                found = True
                break

        if not found:
            bot_response = "🤔 Не сум сигурен, но обиди се да ми објасниш поинаку или постави друго прашање."

        session["chat"].append(("user", user_input))
        session["chat"].append(("bot", bot_response))
        session.modified = True

    return render_template("index.html", chat=session["chat"])

if __name__ == "__main__":
    app.run(debug=True)

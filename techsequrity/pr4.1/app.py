from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        score = 0

        questions = ["a","b","c","d","e","f","g","h"]

        for q in questions:
            value = request.form.get(q)
            if value:
                score += int(value)

        # Аналіз результату
        if score == 0:
            result = "Ви дуже безпечні в Інтернеті."
        elif 0 < score <= 3:
            result = "Ви більш-менш безпечні, але є що покращити."
        elif 4 <= score <= 17:
            result = "Ваша поведінка небезпечна. Є високий ризик компрометації."
        else:
            result = "Ви дуже небезпечні в Інтернеті! Велика ймовірність злому."

        return render_template("result.html", score=score, result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
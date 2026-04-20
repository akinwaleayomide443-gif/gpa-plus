from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GRADE_MAP = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

BME_COURSES = {
    "BME 102": 1, "CHE 102": 3, "CHE 104": 1, "CSC 102": 2,
    "GNS 102": 2, "GNS 106": 2, "MEE 102": 2, "MTS 102": 3,
    "MTS 104": 3, "PHY 102": 3, "PHY 108": 1
}

@app.route("/")
def home():
    return render_template("index.html", courses=dict(sorted(BME_COURSES.items())))

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    courses_input = data.get("courses", [])
    total_points = 0
    total_units = 0
    for item in courses_input:
        code = item.get("code")
        grade = item.get("grade", "").upper()
        if code in BME_COURSES and grade in GRADE_MAP:
            unit = BME_COURSES[code]
            total_points += (GRADE_MAP[grade] * unit)
            total_units += unit
    return jsonify({"gpa": round(total_points / total_units, 2) if total_units > 0 else 0.00})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        current_cgpa = float(data.get("current_cgpa", 0))
        units_passed = int(data.get("units_passed", 0))
        target_cgpa = float(data.get("target_cgpa", 4.5))
        rem_units = 23 
        
        cur_pts = current_cgpa * units_passed
        req_pts = target_cgpa * (units_passed + rem_units)
        needed_gpa = round((req_pts - cur_pts) / rem_units, 2)
        
        status = "Achievable"
        if needed_gpa > 5.0: status = "Impossible this semester"
        elif needed_gpa < 2.0: status = "Very Realistic"
            
        return jsonify({"needed_gpa": max(0, needed_gpa), "status": status})
    except:
        return jsonify({"error": "Invalid Input"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

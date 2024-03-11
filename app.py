from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    # Retrieve parameters from the form
    speed = float(request.form['speed'])
    angle = float(request.form['angle'])
    # Here, include the logic of your simulation using the input parameters
    # For the sake of example, let's say the result is a placeholder
    result = "Simulation result based on speed {} and angle {}".format(speed, angle)
    return result

if __name__ == '__main__':
    app.run(debug=True)

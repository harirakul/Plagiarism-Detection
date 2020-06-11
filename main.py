from flask import Flask, render_template, request, url_for
import similarity

app = Flask(__name__, template_folder='Templates')

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/report',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form['text']
      return (similarity.returnTable(similarity.report(str(result))))

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=5555)

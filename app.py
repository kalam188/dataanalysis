from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'csv_file' not in request.files:
        return redirect(request.url)
    file = request.files['csv_file']
    if file.filename == '':
        return redirect(request.url)

    # Read the CSV file
    data = pd.read_csv(file)

    # Calculate revenue
    data['Revenue'] = data['Quantity'] * data['Unit Price']

    # Generate the plot
    fig, ax = plt.subplots()
    data.groupby('Product')['Revenue'].sum().plot(kind='bar', ax=ax)

    # Convert the plot to a PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('index.html', plot_url=plot_url, data=data.to_html())


if __name__ == '__main__':
    app.run(debug=True)

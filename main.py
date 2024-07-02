from saie import app

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        alunos_file = request.files.get('file')
        if alunos_file:
            filename, file_extension = os.path.splitext(alunos_file.filename)
            if file_extension.lower() == '.txt' or file_extension.lower() == '.csv':
                file_path = os.path.join(UPLOAD_FOLDER, alunos_file.filename)
                alunos_file.save(file_path)
                import_alunos_from_file(file_path)
                return render_template('home.html')
            else:
                flash('Apenas (.txt e .csv) são permitidos!', 'alert-danger')
    return render_template('home.html')

### rodar App e/ou Site ###
if __name__ == '__main__':
    app.run(host='110.0.0.1', port=8080, debug=True)
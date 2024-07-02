from saie import app

### rodar App e/ou Site ###
if __name__ == '__main__':
    app.run(debug=True)
def flask_app(request):
    return app(request)
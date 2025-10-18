from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # cria as tabelas no banco
    app.run(debug=True)

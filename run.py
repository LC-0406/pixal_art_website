from app import create_app, db
from app.models import User, Canvas

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Canvas': Canvas}

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")
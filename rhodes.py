from flask.ext.script import Manager
from api.app import app
from application.tasks.generate_user_tokens import GenerateUserTokens
from application.tasks.seed import Seed

manager = Manager(app)

manager.add_command('generate_user_tokens', GenerateUserTokens())
manager.add_command('seed', Seed())


@manager.command
def runserver(host='0.0.0.0', port=8080):
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    manager.run()

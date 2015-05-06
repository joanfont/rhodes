from flask.ext.script import Manager
from api.app import app
from application.tasks.generate_user_tokens import GenerateUserTokens

manager = Manager(app)

manager.add_command('generate_user_tokens', GenerateUserTokens())


@manager.command
@manager.option('-h', '--host', name='Host')
@manager.option('-p', '--port', name='Port')
def runserver(host='127.0.0.1', port=8080):
    app.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    manager.run()

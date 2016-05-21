from flask.ext.script import Command, Option

from common.session import manager


class Seed(Command):

    option_list = (
        Option('--sql', '-s', dest='sql_file'),
    )

    def run(self, sql_file):
        with open(sql_file, 'r') as f:
            sql = f.read()

        session = manager.get('standalone')
        session.execute(sql)







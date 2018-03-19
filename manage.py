# coding: utf8
# @Author  : WangYe
# @contact : bigjeffwang@163.com
# @Time    : 2018/3/8 上午11:14
# @File    : manage


from flask_script import Manager, Shell, Server

from apps.app import app

manager = Manager(app)


def make_shell_context():
    return {
        'app': app,
    }


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(
    use_debugger=True, use_reloader=True,
    host='0.0.0.0', port=9000
))

if __name__ == '__main__':
    manager.run()

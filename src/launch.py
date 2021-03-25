import sys, os

# Determine the path to the current dir - should be `/etc/www/test_project`
__dir__ = '/'.join(os.path.abspath(__file__).split('/')[0:-1])
sys.path.insert(0, __dir__)

# Activate the virtual environment stored in `venv`
activate_this = os.path.join(__dir__, 'venv', 'bin', 'activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Load the `create_app` factory function and generate an `application` instance
from flocker import create_app
application = create_app()


if __name__ == '__main__':
    if '-debug' in sys.argv:
        if '-global' in sys.argv:
            # Leave out the `host` argument, if the server should only be reachable as `localhost`
            application.run(host='0.0.0.0', debug=True)
        else:
            application.run(debug=True)


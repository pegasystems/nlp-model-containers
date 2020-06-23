from website.app import flask_app


if __name__ == '__main__':
    flask_app.run(port=3000, debug=True, host='0.0.0.0')
    #flask_app.run()

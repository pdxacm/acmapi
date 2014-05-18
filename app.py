from acmapi import create_app, DB

APP = create_app(None, None, 'SQLALCHEMY_DATABASE_URI')

with APP.test_request_context():
    DB.create_all()
    DB.session.commit()

if __name__ == '__main__':
    APP.run(debug=True)

def create_app(config_name):
    from flask import Flask
    # 实例化flask
    app = Flask(__name__)

    from config import config_mapping
    app.config.from_object(config_mapping[config_name])
    config_mapping[config_name].init_app(app)



    from .models import db
    db.init_app(app)


    from .api_csld import member_blueprint
    app.register_blueprint(member_blueprint, url_prefix='/py')


    @app.before_first_request
    def before_first_request():
        pass
    # def before_first_request():
    # 	pass

    @app.before_request
    def before_request():
        pass

    @app.after_request
    def after_request(response):
        return response

    @app.errorhandler(SyntaxError)
    def syntax_error_handler(error):
        app.logger.exception(error)



    return app

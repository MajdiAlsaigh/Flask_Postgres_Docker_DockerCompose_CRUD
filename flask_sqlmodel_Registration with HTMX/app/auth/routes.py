from flask import Blueprint, render_template, make_response, request, current_app

# Creating blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Adding routes
@auth.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            # Registration logic
            pass

        template = 'components/_forms/_registration_form.html' if request.headers.get(
            'HX-Request') else 'auth/register.html'

        #  Create response and set header
        response = make_response(render_template(template))
        response.headers['X-Page-Title'] = 'Sign up | DAR'
        return response

    except Exception as e:
        # Log error
        current_app.logger.error(f"Registration error: {str(e)}")

        # Return appropriate error response
        if request.headers.get('HX-Request'):
            return render_template('components/_ui/_error_card.html'), 500
        return render_template('errors/500.html'), 500


@auth.route('/login', methods=['GET', 'POST'], endpoint='login')
# Handle login (GET form, POST submit)
def login():
    try:
        if request.method == 'POST':
            # Registration logic
            pass

        template = 'components/_forms/_login_form.html' if request.headers.get(
            'HX-Request') else 'auth/login.html'

        #  Create response and set header
        response = make_response(render_template(template))
        response.headers['X-Page-Title'] = 'Login | DAR'
        return response

    except Exception as e:
        # Log error
        current_app.logger.error(f"Login error: {str(e)}")

        # Return appropriate error response
        if request.headers.get('HX-Request'):
            return render_template('components/_ui/_error_card.html'), 500
        return render_template('errors/500.html'), 500


@auth.route('/forgot-password', methods=['GET', 'POST'], endpoint='forgot_password')
# Show forgot password (GET form)
def forgot_password():
    try:
        if request.method == 'POST':
            # Registration logic
            pass

        template = 'components/_forms/_forgot_password_form.html' if request.headers.get(
            'HX-Request') else 'auth/forgot_password.html'

        #  Create response and set header
        response = make_response(render_template(template))
        response.headers['X-Page-Title'] = 'Reset Password | DAR'
        return response

    except Exception as e:
        # Log error
        current_app.logger.error(f"Forgot Password error: {str(e)}")

        # Return appropriate error response
        if request.headers.get('HX-Request'):
            return render_template('components/_ui/_error_card.html'), 500
        return render_template('errors/500.html'), 500


from flask import Blueprint, render_template, request, current_app, make_response

# Creating blueprint
main_bp = Blueprint('main', __name__)


# Adding routes with caching
@main_bp.route('/', endpoint='root')
@main_bp.route('/home', endpoint='home')
def index():
    try:
        # template = 'components/_hero_section.html' if request.headers.get(
        #     'HX-Request') else 'pages/index.html'
        # return render_template(template)
        is_hx = request.headers.get('HX-Request')

        template = 'components/_sections/_hero_section.html' if is_hx else 'pages/index.html'
        response = make_response(render_template(template))

        # Only cache partials (optional), or cache both but vary by HX header
        response.headers['Cache-Control'] = 'public, max-age=60'
        response.headers['Vary'] = 'HX-Request'  # ← Critical!

        #  Set header
        response.headers['X-Page-Title'] = 'Home | DAR'
        return response

    except Exception as e:
        # Log error
        current_app.logger.error(f"Index error: {str(e)}")

        # Return appropriate error response
        if request.headers.get('HX-Request'):
            return render_template('components/_ui/_error_card.html'), 500
        return render_template('errors/500.html'), 500

from flask import Flask, render_template,jsonify,request
import google.generativeai as genai 
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from flask import redirect, url_for, session, send_file, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from ai.ai_resume_utils import generate_resume_content
import re
import pdfkit

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generatePortfolio')
def generatePortfolio():
    return render_template('portfolioGenerator/userInfoForPortfolio.html')

@app.route('/generateResume')
def generateResume():
    return render_template('resumegenerator/resume_form.html')

genai.configure(api_key="AIzaSyBmryOrJNqM2D3U6kL8Z25qsm_G1eScWao")
    
# Route for AI Suggestions
@app.route('/generate-ai-text', methods=['POST'])
def generate_ai_text():
    try:
        data = request.get_json()
        user_prompt = data.get('prompt')
        model = genai.GenerativeModel('gemini-2.5-flash')
        print(user_prompt)
        response = model.generate_content(user_prompt)
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
import os
app.config['UPLOAD_FOLDER'] = 'static/uploads'
@app.route('/getUserDetailsForPortfolio', methods=['POST'])
def getUserDetailsForPortfolio():
    try:
        # Basic fields
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        bio = request.form.get('bio', '')
        personal = request.form.get('personal', '')

        # Socials
        linkedin = request.form.get('linkedin', '')
        github = request.form.get('github', '')
        socials = request.form.getlist('social') or []

        # Handle file upload
        image = request.files.get('imageUpload')
        image_path = None
        if image and image.filename:
            upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads/')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image.filename)
            image.save(image_path)

        # Dynamic sections with fallbacks
        skills = request.form.getlist('skills[]') or []
        certificates = request.form.getlist('certificate[]') or []
        experience = request.form.getlist('experience[]') or []
        education = request.form.getlist('education[]') or []

        # Projects (robust handling)
        project_titles = request.form.getlist('project_title[]') or []
        project_descs = request.form.getlist('project_desc[]') or []
        project_lives = request.form.getlist('project_live[]') or []
        project_codes = request.form.getlist('project_code[]') or []

        projects = []
        for i in range(len(project_titles)):
            project = {
                'title': project_titles[i] if i < len(project_titles) else '',
                'desc': project_descs[i] if i < len(project_descs) else '',
                'live': project_lives[i] if i < len(project_lives) else '',
                'code': project_codes[i] if i < len(project_codes) else ''
            }
            projects.append(project)

        # Collect everything
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "bio": bio,
            "personal": personal,
            "skills": skills,
            "certificates": certificates,
            "projects": projects,
            "experience": experience,
            "education": education,
            "linkedin": linkedin,
            "github": github,
            "socials": socials,
            "image_path": image_path
        }

        print("🔍 Received Form Data:", data)

        rendered_html = generate_portfolio({
            "name": data["name"],
            "profileImageUrl": data["image_path"] or "",
            "title": data["personal"],
            "about": data["bio"],
            "skills": data["skills"],
            "projects": [
                {
                    "title": p.get("title", ""),
                    "description": p.get("desc", ""),
                    "live": p.get("live", ""),
                    "code": p.get("code", "")
                } for p in data["projects"]
            ],
            "courses": data["certificates"],
            "email": data["email"],
            "phone": data["phone"],
            "year": datetime.now().year
        })

        # ✅ Returning full HTML to preview (no redirect)
        return render_template("/portfolioGenerator/customizePortfolio.html", data=data, rendered_html=rendered_html)

    except Exception as e:
        print("❌ Error in getUserDetailsForPortfolio:", str(e))
        return f"Something went wrong: {str(e)}", 500


def generate_portfolio(data, template_file="portfolio_theme2.html", output_file="generated_portfolio.html"):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, "templates", "portfolioGenerator", "themes")

        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_file)

        rendered = template.render(data)

        # Save locally if needed
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Portfolio generated successfully: {output_file}")
        return rendered
    except Exception as e:
        print("❌ Error in generate_portfolio:", str(e))
        return "<p>Error rendering portfolio.</p>"
    
@app.route("/generate_with_ai", methods=["POST"])
def generate_with_ai():
    data = request.get_json()
    instruction = data.get("instruction", "")
    current_code = data.get("code", "")

    if not instruction or not current_code:
        return jsonify({"error": "Missing instruction or code"}), 400

    prompt = f"""
You are an expert web designer.
Here is the current code of a user's portfolio HTML:
-----
{current_code}
-----
The user wants the following changes:
{instruction}
Update the code accordingly and return the final updated HTML.
----
Only return the code in simple text and not include '```html'
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        updated_code = response.text.strip()

        return jsonify({"updated_code": updated_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user'] = user.username
            return render_template('dashboard.html')
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if already exists
        if User.query.filter_by(username=username).first():
            flash('User already exists.')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return render_template('login.html')

    return render_template('register.html')


# Resume Type Selection
@app.route('/resume-type')
def resume_type():
    return render_template('resume_type.html')


# Resume Form
@app.route('/resume_form', methods=['GET', 'POST'])
def resume_form():
    if request.method == 'POST':
        data = request.form.to_dict()

        if request.form.get('autofill'):
            auto = generate_resume_content(data)
            data.update(auto)

        return render_template(f'resume_templates/{data["template"]}.html', **data)

    return render_template('resume_form.html')

# Resume Download Page
@app.route('/resume-download')
def resume_download_page():
    data = request.args.to_dict()
    return render_template('resume_download.html', **data)

# PDF Download
@app.route('/resume-download-pdf', methods=['POST'])
def resume_download_pdf():
    data = request.form.to_dict()
    rendered = render_template(f"resume_templates/{data['template']}.html", **data)

    pdf_path = os.path.join('static', 'resume.pdf')
    pdfkit.from_string(rendered, pdf_path)

    return send_file(pdf_path, as_attachment=True)

# Customize Page
@app.route('/resume-customize')
def resume_customize():
    return render_template('resume_customize.html')

# Optimize Page
@app.route('/resume-optimize')
def resume_optimize():
    return render_template('resume_optimize.html')

# Dynamic Template Preview
@app.route('/resume-template/<template_name>')
def resume_template(template_name):
    data = request.args.to_dict()
    return render_template(f"resume_templates/{template_name}.html", **data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

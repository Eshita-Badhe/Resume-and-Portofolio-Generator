from flask import Flask, render_template,jsonify,request
import google.generativeai as genai 
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generatePortfolio')
def generatePortfolio():
    return render_template('portfolioGenerator/userInfoForPortfolio.html')

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


def generate_portfolio(data, template_file="portfolio_theme1.html", output_file="generated_portfolio.html"):
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
    
if __name__ == '__main__':
    app.run(debug=True)

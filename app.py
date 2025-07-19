from flask import Flask, render_template,jsonify,request
import google.generativeai as genai 
from jinja2 import Environment, FileSystemLoader
import os

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
    # Basic fields
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    bio = request.form.get('bio')
    personal = request.form.get('personal')

    # Socials
    linkedin = request.form.get('linkedin')
    github = request.form.get('github')
    socials = request.form.getlist('social')

    # Handle file upload
    image = request.files.get('imageUpload')
    image_path = None
    if image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

    # Dynamic sections
    skills = request.form.getlist('skills[]')
    certificates = request.form.getlist('certificate[]')
    experience = request.form.getlist('experience[]')
    education = request.form.getlist('education[]')

    # Projects (updated part)
    project_titles = request.form.getlist('project_title[]')
    project_descs = request.form.getlist('project_desc[]')
    project_lives = request.form.getlist('project_live[]')
    project_codes = request.form.getlist('project_code[]')

    projects = []
    for i in range(len(project_titles)):
        projects.append({
            'title': project_titles[i],
            'desc': project_descs[i],
            'live': project_lives[i],
            'code': project_codes[i]
        })

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

    print(data)
    
    from datetime import datetime

    generate_portfolio({
        "name": data["name"],
        "profileImageUrl": data["image_path"] or "",  
        "title": data["personal"],
        "about": data["bio"],
        "skills": data["skills"],
        "projects": [
            {
                "title": p["title"],
                "description": p["desc"],
                "live": p["live"],
                "code": p["code"]
            } for p in data["projects"]
        ],
        "courses": data["certificates"],
        "email": data["email"],
        "phone": data["phone"],
        "year": datetime.now().year
    })

    return render_template("/portfolioGenerator/customizePortfolio.html", data=data)


def generate_portfolio(data, template_file="portfolio_theme1.html", output_file="generated_portfolio.html"):
    # Get absolute path to the template directory
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    template_dir = os.path.join(base_dir, "templates", "portfolioGenerator", "themes")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    rendered = template.render(data)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ Portfolio generated successfully: {output_file}")

if __name__ == '__main__':
    app.run(debug=True)

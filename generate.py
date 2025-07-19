from jinja2 import Environment, FileSystemLoader
import os

def generate_portfolio(data, template_file="portfolio_theme1.html", output_file="generated_portfolio.html"):
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template(template_file)
    rendered = template.render(data)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ Portfolio generated successfully: {output_file}")

data = {
    "name": "Aarya Chaudhari",
    "profileImageUrl": "abc.jpeg",  
    "title": "Frontend Developer",
    "about": "I love building elegant and functional web interfaces.",
    "skill": ["HTML", "CSS", "JavaScript", "React", "Tailwind", "Bootstrap", "Git", "Figma"],
    "projects": [
        {
            "title": "Weather App",
            "description": "Displays weather data using OpenWeather API.",
            "live": "https://aarya-weather.live",
            "code": "https://github.com/aarya/weatherapp"
        },
        {
            "title": "To-Do List",
            "description": "Task management app with local storage support.",
            "live": "https://aarya-todo.live",
            "code": "https://github.com/aarya/todoapp"
        }
    ],
    "courses": ["Frontend Development Bootcamp", "JavaScript Advanced", "Git & GitHub", "React Fundamentals"],
    "email": "aarya@example.com",
    "phone": "+91 9876543210",
    "year": "2025"
}

generate_portfolio(data)
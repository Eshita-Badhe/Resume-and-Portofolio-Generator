
document.getElementById('generate-summary').addEventListener('click', async () => {
  const name = document.getElementById('name').value;
  const skills = document.getElementById('skills').value;

  const response = await fetch('/api/generate-summary', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, skills })
  });

  const data = await response.json();
  document.getElementById('summary').value = data.summary;
});


document.addEventListener("DOMContentLoaded", () => {
  const generateBtn = document.getElementById("generate-summary");
  const summaryBox = document.getElementById("summary");

  generateBtn.addEventListener("click", async () => {
    const skills = document.getElementById("skills").value.trim();
    const experience = document.getElementById("experience").value.trim();
    const education = document.getElementById("education").value.trim();

    if (!skills || !experience || !education) {
      alert("Please fill in Skills, Experience, and Education first.");
      return;
    }

    generateBtn.textContent = "Generating...";
    generateBtn.disabled = true;

    try {
      const response = await fetch("/generate_summary", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          skills: skills,
          experience: experience,
          education: education
        })
      });

      const data = await response.json();

      if (data && data.summary) {
        summaryBox.value = data.summary;
      } else {
        alert("Failed to generate summary. Try again.");
      }
    } catch (error) {
      console.error("Error generating summary:", error);
      alert("Something went wrong. Please try again.");
    }

    generateBtn.textContent = "Generate with AI";
    generateBtn.disabled = false;
  });
});


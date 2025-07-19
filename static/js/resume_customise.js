
function applyCustomization() {
    const color = document.getElementById('colorTheme').value;
    const font = document.getElementById('fontStyle').value;
    const order = document.getElementById('sectionOrder').value;

    const resumeBox = document.getElementById('resumeContent');
    resumeBox.style.color = '#000';
    resumeBox.style.backgroundColor = '#fff';
    resumeBox.style.borderColor = color;
    resumeBox.style.fontFamily = font;


    if (order === 'skills-first') {
        resumeBox.innerHTML = `
            <h1>Your Name</h1>
            <h3>Skills</h3>
            <p>Python, Flask, SQL</p>
            <h3>Experience</h3>
            <ul><li>Sample job bullet</li></ul>
        `;
    } else if (order === 'experience-first') {
        resumeBox.innerHTML = `
            <h1>Your Name</h1>
            <h3>Experience</h3>
            <ul><li>Sample job bullet</li></ul>
            <h3>Skills</h3>
            <p>Python, Flask, SQL</p>
        `;
    } else {
        resumeBox.innerHTML = `
            <h1>Your Name</h1>
            <p>Summary goes here...</p>
            <h3>Experience</h3>
            <ul><li>Sample job bullet</li></ul>
            <h3>Skills</h3>
            <p>Python, Flask, SQL</p>
        `;
    }
}

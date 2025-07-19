document.getElementById("optimizeForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const resume = document.getElementById("resumeText").value.toLowerCase();
  const jd = document.getElementById("jobDescription").value.toLowerCase();

  // Extract keywords: naive splitting
  const jdWords = jd.match(/\b(\w+)\b/g);
  const resumeWords = new Set(resume.match(/\b(\w+)\b/g));

  const keywordCounts = {};
  jdWords.forEach(word => {
    if (word.length > 3 && !resumeWords.has(word)) {
      keywordCounts[word] = (keywordCounts[word] || 0) + 1;
    }
  });

  const sortedMissing = Object.keys(keywordCounts)
    .sort((a, b) => keywordCounts[b] - keywordCounts[a]);

  const list = document.getElementById("missingKeywords");
  list.innerHTML = "";

  if (sortedMissing.length === 0) {
    list.innerHTML = "<li>✅ Great! All important keywords are covered.</li>";
  } else {
    sortedMissing.slice(0, 20).forEach(word => {
      const li = document.createElement("li");
      li.textContent = word;
      list.appendChild(li);
    });
  }

  document.getElementById("results").style.display = "block";
});

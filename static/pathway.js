// static/pathway.js

async function submitPathway(pathway, responses) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML =
    '<div class="loading">Processing your responses...</div>';
  resultsDiv.style.display = "block";

  try {
    const response = await fetch("/submit_pathway", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pathway, responses }),
    });

    const data = await response.json();

    if (data.success) {
      displayRecommendations(data.recommendations, pathway);
    } else {
      resultsDiv.innerHTML =
        '<div class="message error">Error generating recommendations</div>';
    }
  } catch (error) {
    resultsDiv.innerHTML = '<div class="message error">An error occurred</div>';
  }
}

function displayRecommendations(recommendations, pathway) {
  const resultsDiv = document.getElementById("results");
  let html = "<h2>Your Top Recommendations</h2>";

  recommendations.forEach((rec, index) => {
    const title = rec.title || rec.name || "Recommendation";
    const match = rec.match || 0;
    const meta = rec.metadata || {};

    html += `
      <div class="result-card">
        <span class="match-score">${match}% Match</span>
        <h3>${index + 1}. ${title}</h3>
        <div class="result-details">
    `;

    // Show some metadata fields if available
    if (pathway === "career") {
      html += `
        <div class="detail-item"><span class="detail-label">Growth</span>
          <span class="detail-value">${
            meta.growth || meta["growth"] || "See details"
          }</span></div>
        <div class="detail-item"><span class="detail-label">Related</span>
          <span class="detail-value">${
            meta.related_titles || meta.related || "—"
          }</span></div>
      `;
    } else if (pathway === "education") {
      html += `
        <div class="detail-item"><span class="detail-label">Modality</span>
          <span class="detail-value">${
            meta.modality || meta["modality"] || "—"
          }</span></div>
        <div class="detail-item"><span class="detail-label">Related</span>
          <span class="detail-value">${
            meta.related_programs || meta.related || "—"
          }</span></div>
      `;
    } else if (pathway === "tesda") {
      html += `
        <div class="detail-item"><span class="detail-label">Duration/Notes</span>
          <span class="detail-value">${
            meta.time_available || meta["time_available"] || "See details"
          }</span></div>
        <div class="detail-item"><span class="detail-label">Related</span>
          <span class="detail-value">${
            meta.related_courses || meta.related || "—"
          }</span></div>
      `;
    }

    html += `
        </div>
        <div class="result-actions">
          <button class="btn-save" onclick='saveRecommendation("${pathway}", ${index})'>💾 Save</button>
          <button class="btn-details" onclick='showDetails("${pathway}", ${index})'>📋 View Details</button>
        </div>
      </div>
    `;
  });

  html += `<div style="margin-top: 2rem; text-align:center;"><a href="/dashboard" class="btn-secondary">Back to Dashboard</a></div>`;
  resultsDiv.innerHTML = html;
  resultsDiv.style.display = "block";

  sessionStorage.setItem(
    "currentRecommendations",
    JSON.stringify(recommendations)
  );
  sessionStorage.setItem("currentPathway", pathway);
}

async function saveRecommendation(pathway, index) {
  const recommendations = JSON.parse(
    sessionStorage.getItem("currentRecommendations")
  );
  const recommendation = recommendations[index];

  try {
    const response = await fetch("/save_recommendation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pathway, recommendation }),
    });

    const data = await response.json();

    if (data.success) {
      alert("✅ Recommendation saved successfully!");
    } else {
      alert("❌ Error saving recommendation");
    }
  } catch (error) {
    alert("❌ An error occurred");
  }
}

function showDetails(pathway, index) {
  const recommendations = JSON.parse(
    sessionStorage.getItem("currentRecommendations")
  );
  const rec = recommendations[index];
  const meta = rec.metadata || {};

  let detailsHTML = `
        <div class="modal-overlay" onclick="closeModal()">
            <div class="modal-content" onclick="event.stopPropagation()">
                <span class="modal-close" onclick="closeModal()">&times;</span>
                <h2>${rec.title || rec.name}</h2>
                <div class="match-badge">Match Score: ${rec.match || 0}%</div>
                <div class="modal-body">
    `;

  // Display metadata from ML model dynamically
  if (Object.keys(meta).length > 0) {
    detailsHTML += `<h3>Details from Data</h3>`;
    for (const [key, value] of Object.entries(meta)) {
      if (key !== "title" && value) {
        const displayKey =
          key.replace(/_/g, " ").charAt(0).toUpperCase() +
          key.replace(/_/g, " ").slice(1);
        detailsHTML += `
          <div class="detail-row">
            <strong>${displayKey}:</strong> ${value}
          </div>
        `;
      }
    }
  } else {
    detailsHTML += `<p><em>Detailed information from the machine learning model.</em></p>`;
  }

  detailsHTML += `
                </div>
                <button class="btn-primary" onclick="closeModal()">Close</button>
            </div>
        </div>
    `;

  // Add modal styles if not already present
  if (!document.getElementById("modalStyles")) {
    const styleSheet = document.createElement("style");
    styleSheet.id = "modalStyles";
    styleSheet.textContent = `
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.7);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .modal-content {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
                position: relative;
            }
            .modal-close {
                position: absolute;
                top: 1rem;
                right: 1rem;
                font-size: 2rem;
                cursor: pointer;
                color: #999;
            }
            .modal-close:hover {
                color: #333;
            }
            .match-badge {
                display: inline-block;
                background: #4CAF50;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-weight: bold;
                margin: 0.5rem 0 1rem 0;
                font-size: 0.9rem;
            }
            .modal-body {
                margin: 1rem 0;
            }
            .modal-body h3 {
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                color: var(--primary);
            }
            .detail-row {
                margin: 0.75rem 0;
                padding: 0.5rem;
                background: #f5f5f5;
                border-left: 3px solid var(--primary);
                padding-left: 1rem;
            }
            .detail-row strong {
                color: var(--primary);
            }
        `;
    document.head.appendChild(styleSheet);
  }

  // Add modal to page
  const modalDiv = document.createElement("div");
  modalDiv.id = "detailsModal";
  modalDiv.innerHTML = detailsHTML;
  document.body.appendChild(modalDiv);
}

function closeModal() {
  const modal = document.getElementById("detailsModal");
  if (modal) {
    modal.remove();
  }
}

// Close modal on Escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeModal();
  }
});

/* ============================================================
   SI-POSTURE DASHBOARD SCRIPT — INTERACTIVE LAYOUT LAYER
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
    
    // Tab Button Navigation Elements
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");
    const progressBar = document.getElementById("progressBar");

    // Dynamic Progress Mapping per Tab
    const progressMap = {
        overview: 17,
        dataset: 33,
        training: 50,
        analytics: 67,
        realtime: 83,
        reports: 100
    };

    // Initialize progress bar position for active tab
    const initialActiveTab = document.querySelector(".tab-btn.active");
    if (initialActiveTab) {
        const tabKey = initialActiveTab.getAttribute("data-tab");
        progressBar.style.width = `${progressMap[tabKey] || 17}%`;
    }

    // Tab switcher handler
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.getAttribute("data-tab");

            // 1. Update active nav button
            tabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // 2. Switch visible panel
            tabContents.forEach(content => {
                content.classList.remove("active");
                if (content.getAttribute("id") === targetTab) {
                    content.classList.add("active");
                }
            });

            // 3. Move top progress indicator
            const progressVal = progressMap[targetTab] || 17;
            progressBar.style.width = `${progressVal}%`;
        });
    });

    // ============================================================
    // DYNAMIC METADATA LOADER (session_summary.json)
    // ============================================================
    
    const loadSessionSummary = async () => {
        const timestampEl = document.getElementById("rep-timestamp");
        const avgEl = document.getElementById("rep-avg");
        const minEl = document.getElementById("rep-min");
        const maxEl = document.getElementById("rep-max");
        const fatigueEl = document.getElementById("rep-fatigue");
        
        const cacheBuster = `?t=${new Date().getTime()}`;

        try {
            // Fetch session summary metadata JSON
            const response = await fetch(`assets/latest/session_summary.json${cacheBuster}`);
            
            if (!response.ok) {
                throw new Error("Session summary JSON file not found.");
            }
            
            const data = await response.json();
            
            // Populate card statistics
            if (timestampEl) timestampEl.textContent = data.timestamp || "N/A";
            if (avgEl) avgEl.textContent = data.average_score !== undefined ? data.average_score.toFixed(1) : "N/A";
            if (minEl) minEl.textContent = data.minimum_score !== undefined ? data.minimum_score.toFixed(1) : "N/A";
            if (maxEl) maxEl.textContent = data.maximum_score !== undefined ? data.maximum_score.toFixed(1) : "N/A";
            
            if (fatigueEl) {
                fatigueEl.textContent = (data.fatigue_start_index !== null && data.fatigue_start_index !== undefined)
                    ? `Index #${data.fatigue_start_index}` 
                    : "N/A (No Fatigue)";
            }
            
            console.log("SUCCESS: Session metadata loaded successfully.");

            // Update session trend graph source with cache buster
            const sessionGraphImg = document.getElementById("sessionGraph");
            if (sessionGraphImg) {
                sessionGraphImg.src = `assets/latest/posture_graph.png${cacheBuster}`;
            }

        } catch (error) {
            console.warn("WARNING: Unable to load latest session metadata JSON:", error.message);
            // Revert graph and overlays to static pre-existing fallback paths gracefully
            fallbackGraphSource();
        }
    };

    // Helper to fall back graph if latest is missing
    const fallbackGraphSource = () => {
        const sessionGraphImg = document.getElementById("sessionGraph");
        if (sessionGraphImg && sessionGraphImg.src.includes("assets/latest/")) {
            sessionGraphImg.src = "assets/analytics/posture_graph.png";
        }
    };

    // Setup fallback loaders for dynamically loaded media assets (Defensive Strategy)
    const setupFallbackLoaders = () => {
        // 1. Live Realtime Screenshot
        const realtimeImg = document.getElementById("realtimeScreenshot");
        const screenshotOverlay = document.getElementById("screenshotOverlay");
        const screenshotCaption = document.getElementById("screenshotCaption");
        
        if (realtimeImg) {
            // Apply cache-busting query parameter to force reload of screenshot
            const cb = `?t=${new Date().getTime()}`;
            realtimeImg.src = `assets/latest/latest-demo.png${cb}`;
            
            realtimeImg.onerror = () => {
                // Safe baseline fallback if user has not captured any demo frames yet
                realtimeImg.src = "assets/realtime/yolo-prediction-bad.png";
                if (screenshotCaption) {
                    screenshotCaption.textContent = "Webcam realtime posture analysis (baseline prediction sample).";
                }
                if (screenshotOverlay) {
                    screenshotOverlay.style.display = "none"; // Hide indicator if showing fallback
                }
                console.log("INFO: No custom demo screenshot found, displaying fallback baseline prediction.");
            };
        }

        // 2. Reports Graph Image
        const sessionGraphImg = document.getElementById("sessionGraph");
        if (sessionGraphImg) {
            sessionGraphImg.onerror = () => {
                sessionGraphImg.src = "assets/analytics/posture_graph.png";
                console.log("INFO: No custom session graph found, displaying default visual chart.");
            };
        }
    };

    // Run active dynamic assets updates
    loadSessionSummary();
    setupFallbackLoaders();
});
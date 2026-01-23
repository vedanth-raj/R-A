// AI Research Agent - Frontend JavaScript
// Dark-themed interactive web interface

class AIResearchAgent {
    constructor() {
        this.socket = io();
        this.currentTab = 'search';
        this.papers = [];
        this.selectedPapers = new Set();
        this.activeOperations = {};
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSocketListeners();
        this.loadPapers();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Search form
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchPapers();
        });

        // Extract button
        document.getElementById('extractBtn').addEventListener('click', () => {
            this.extractText();
        });

        // Analyze button
        document.getElementById('analyzeBtn').addEventListener('click', () => {
            this.analyzePaper();
        });

        // Compare button
        document.getElementById('compareBtn').addEventListener('click', () => {
            this.comparePapers();
        });

        // Paper selection
        document.getElementById('paperSelect').addEventListener('change', (e) => {
            const analyzeBtn = document.getElementById('analyzeBtn');
            analyzeBtn.disabled = !e.target.value;
        });
    }

    setupSocketListeners() {
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.showNotification('Connected to AI Research Agent', 'success');
        });

        this.socket.on('operation_update', (data) => {
            this.updateOperationProgress(data);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.showNotification('Disconnected from server', 'error');
        });
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        this.currentTab = tabName;

        // Load data for specific tabs
        if (tabName === 'analyze' || tabName === 'compare') {
            this.loadPapers();
        }
    }

    async searchPapers() {
        const query = document.getElementById('searchQuery').value;
        const maxPapers = document.getElementById('maxPapers').value;
        const yearStart = document.getElementById('yearStart').value;
        const yearEnd = document.getElementById('yearEnd').value;

        if (!query.trim()) {
            this.showNotification('Please enter a search query', 'error');
            return;
        }

        try {
            this.showProgress('search', 'Starting search...');
            
            const response = await fetch('/api/search_papers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query,
                    maxPapers: parseInt(maxPapers),
                    yearStart: yearStart ? parseInt(yearStart) : null,
                    yearEnd: yearEnd ? parseInt(yearEnd) : null
                })
            });

            const data = await response.json();
            
            if (data.status === 'started') {
                this.activeOperations[data.operation_id] = 'search';
                this.showNotification('Search started successfully', 'success');
            } else {
                this.hideProgress('search');
                this.showNotification('Failed to start search', 'error');
            }
        } catch (error) {
            this.hideProgress('search');
            this.showNotification('Search failed: ' + error.message, 'error');
        }
    }

    async extractText() {
        try {
            this.showProgress('extract', 'Starting text extraction...');
            
            const response = await fetch('/api/extract_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();
            
            if (data.status === 'started') {
                this.activeOperations[data.operation_id] = 'extract';
                this.showNotification('Text extraction started', 'success');
            } else {
                this.hideProgress('extract');
                this.showNotification('Failed to start text extraction', 'error');
            }
        } catch (error) {
            this.hideProgress('extract');
            this.showNotification('Text extraction failed: ' + error.message, 'error');
        }
    }

    async analyzePaper() {
        const paperFile = document.getElementById('paperSelect').value;
        
        if (!paperFile) {
            this.showNotification('Please select a paper to analyze', 'error');
            return;
        }

        try {
            this.showProgress('analyze', 'Starting paper analysis...');
            
            const response = await fetch('/api/analyze_paper', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    paper_file: paperFile
                })
            });

            const data = await response.json();
            
            if (data.status === 'started') {
                this.activeOperations[data.operation_id] = 'analyze';
                this.showNotification('Paper analysis started', 'success');
            } else {
                this.hideProgress('analyze');
                this.showNotification('Failed to start paper analysis', 'error');
            }
        } catch (error) {
            this.hideProgress('analyze');
            this.showNotification('Paper analysis failed: ' + error.message, 'error');
        }
    }

    async comparePapers() {
        if (this.selectedPapers.size < 2) {
            this.showNotification('Please select at least 2 papers to compare', 'error');
            return;
        }

        try {
            this.showProgress('compare', 'Starting paper comparison...');
            
            const response = await fetch('/api/compare_papers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    paper_files: Array.from(this.selectedPapers)
                })
            });

            const data = await response.json();
            
            if (data.status === 'started') {
                this.activeOperations[data.operation_id] = 'compare';
                this.showNotification('Paper comparison started', 'success');
            } else {
                this.hideProgress('compare');
                this.showNotification('Failed to start paper comparison', 'error');
            }
        } catch (error) {
            this.hideProgress('compare');
            this.showNotification('Paper comparison failed: ' + error.message, 'error');
        }
    }

    async loadPapers() {
        try {
            const response = await fetch('/api/get_papers');
            const data = await response.json();
            
            this.papers = data.papers || [];
            this.updatePaperSelect();
            this.updatePaperList();
        } catch (error) {
            console.error('Failed to load papers:', error);
        }
    }

    updatePaperSelect() {
        const select = document.getElementById('paperSelect');
        select.innerHTML = '<option value="">Select a paper...</option>';
        
        this.papers.forEach(paper => {
            const option = document.createElement('option');
            option.value = paper.file;
            option.textContent = paper.name;
            select.appendChild(option);
        });
    }

    updatePaperList() {
        const paperList = document.getElementById('paperList');
        
        if (this.papers.length === 0) {
            paperList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No papers found. Please extract text from PDFs first.</p>';
            return;
        }

        paperList.innerHTML = '';
        
        this.papers.forEach(paper => {
            const paperItem = document.createElement('div');
            paperItem.className = 'paper-item';
            
            const isSelected = this.selectedPapers.has(paper.file);
            
            paperItem.innerHTML = `
                <div class="paper-info">
                    <div class="paper-title">${paper.name}</div>
                    <div class="paper-meta">
                        Size: ${(paper.size / 1024).toFixed(1)} KB | 
                        Modified: ${new Date(paper.modified * 1000).toLocaleDateString()}
                    </div>
                </div>
                <div class="paper-actions">
                    <input type="checkbox" class="paper-checkbox" 
                           data-file="${paper.file}" 
                           ${isSelected ? 'checked' : ''}>
                </div>
            `;
            
            // Add checkbox event listener
            const checkbox = paperItem.querySelector('.paper-checkbox');
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.selectedPapers.add(paper.file);
                } else {
                    this.selectedPapers.delete(paper.file);
                }
                this.updateCompareButton();
            });
            
            paperList.appendChild(paperItem);
        });
    }

    updateCompareButton() {
        const compareBtn = document.getElementById('compareBtn');
        compareBtn.disabled = this.selectedPapers.size < 2;
    }

    updateOperationProgress(data) {
        const operationType = this.activeOperations[data.operation_id];
        
        if (!operationType) return;
        
        if (data.status === 'running') {
            this.updateProgress(operationType, data.progress || 50, data.message);
        } else if (data.status === 'completed') {
            this.hideProgress(operationType);
            this.showNotification(data.message, 'success');
            this.handleOperationResult(operationType, data.result);
            delete this.activeOperations[data.operation_id];
        } else if (data.status === 'error') {
            this.hideProgress(operationType);
            this.showNotification(data.message, 'error');
            delete this.activeOperations[data.operation_id];
        }
    }

    handleOperationResult(operationType, result) {
        if (operationType === 'analyze') {
            this.displayAnalysisResults(result);
        } else if (operationType === 'compare') {
            this.displayComparisonResults(result);
        } else if (operationType === 'search' || operationType === 'extract') {
            // Reload papers after search or extraction
            this.loadPapers();
            this.displayResults(result);
        }
    }

    displayAnalysisResults(result) {
        const resultsContainer = document.getElementById('analysisResults');
        resultsContainer.style.display = 'block';
        
        const sections = result.sections || [];
        const textAnalysis = result.text_analysis || {};
        const keyInsights = result.key_insights || [];
        
        let html = `
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3 class="card-title">Analysis Results</h3>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${result.total_sections || 0}</div>
                        <div class="stat-label">Total Sections</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${result.total_words || 0}</div>
                        <div class="stat-label">Total Words</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${(textAnalysis.quality_metrics?.overall_quality * 100).toFixed(1) || 0}%</div>
                        <div class="stat-label">Text Quality</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${keyInsights.length}</div>
                        <div class="stat-label">Key Insights</div>
                    </div>
                </div>
                
                <h4 style="margin: 2rem 0 1rem 0; color: var(--text-primary);">Sections</h4>
                <div class="section-list">
        `;
        
        sections.forEach(section => {
            html += `
                <div class="section-item">
                    <div class="section-title">${section.title}</div>
                    <div class="section-meta">
                        Type: ${section.section_type} | 
                        Words: ${section.word_count} | 
                        Pages: ${section.start_page}-${section.end_page}
                    </div>
                    <div class="section-content">
                        ${section.content.substring(0, 300)}${section.content.length > 300 ? '...' : ''}
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        
        if (keyInsights.length > 0) {
            html += `
                <h4 style="margin: 2rem 0 1rem 0; color: var(--text-primary);">Key Insights</h4>
                <div class="result-item">
                    <ul style="color: var(--text-secondary); line-height: 1.8;">
            `;
            
            keyInsights.forEach(insight => {
                html += `<li>${insight}</li>`;
            });
            
            html += '</ul></div>';
        }
        
        html += '</div>';
        resultsContainer.innerHTML = html;
    }

    displayComparisonResults(result) {
        const resultsContainer = document.getElementById('comparisonResults');
        resultsContainer.style.display = 'block';
        
        const comparison = result.comparison || {};
        const papers = comparison.papers || [];
        
        let html = `
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-balance-scale"></i>
                    </div>
                    <h3 class="card-title">Comparison Results</h3>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${papers.length}</div>
                        <div class="stat-label">Papers Compared</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${comparison.average_sections_per_paper?.toFixed(1) || 0}</div>
                        <div class="stat-label">Avg Sections/Paper</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${Object.keys(comparison.common_sections || {}).length}</div>
                        <div class="stat-label">Common Sections</div>
                    </div>
                </div>
                
                <h4 style="margin: 2rem 0 1rem 0; color: var(--text-primary);">Paper Details</h4>
        `;
        
        papers.forEach(paper => {
            html += `
                <div class="result-item">
                    <div class="result-header">
                        <div class="result-title">${paper.file_name}</div>
                        <div class="result-meta">${paper.section_count} sections</div>
                    </div>
                    <div class="result-content">
                        <strong>Section Types:</strong> ${paper.section_types.join(', ')}
                    </div>
                </div>
            `;
        });
        
        if (comparison.common_sections && Object.keys(comparison.common_sections).length > 0) {
            html += `
                <h4 style="margin: 2rem 0 1rem 0; color: var(--text-primary);">Common Sections</h4>
                <div class="result-item">
                    <div class="result-content">
                        <ul style="color: var(--text-secondary); line-height: 1.8;">
            `;
            
            Object.entries(comparison.common_sections).forEach(([section, count]) => {
                html += `<li>${section}: ${count} papers</li>`;
            });
            
            html += '</ul></div></div>';
        }
        
        html += '</div>';
        resultsContainer.innerHTML = html;
    }

    displayResults(result) {
        const resultsContent = document.getElementById('resultsContent');
        
        let html = `
            <div class="result-item">
                <div class="result-header">
                    <div class="result-title">Operation Completed</div>
                    <div class="result-meta">${new Date().toLocaleString()}</div>
                </div>
                <div class="result-content">
                    <pre style="background: var(--bg-secondary); padding: 1rem; border-radius: 4px; overflow-x: auto;">
${JSON.stringify(result, null, 2)}
                    </pre>
                </div>
            </div>
        `;
        
        resultsContent.innerHTML = html;
    }

    showProgress(type, message) {
        const progressContainer = document.getElementById(`${type}Progress`);
        const progressFill = document.getElementById(`${type}ProgressFill`);
        const progressText = document.getElementById(`${type}ProgressText`);
        
        progressContainer.style.display = 'block';
        progressFill.style.width = '0%';
        progressText.textContent = message;
    }

    updateProgress(type, progress, message) {
        const progressFill = document.getElementById(`${type}ProgressFill`);
        const progressText = document.getElementById(`${type}ProgressText`);
        
        progressFill.style.width = `${progress}%`;
        progressText.textContent = message;
    }

    hideProgress(type) {
        const progressContainer = document.getElementById(`${type}Progress`);
        progressContainer.style.display = 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 400px;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }
}

// Add slide animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.aiResearchAgent = new AIResearchAgent();
});

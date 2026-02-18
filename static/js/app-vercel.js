// AI Research Agent - Vercel-compatible Frontend (REST API)

class AIResearchAgent {
    constructor() {
        this.papers = [];
        this.selectedPapers = new Set();
        this.currentDraft = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadSearchResults();
    }

    setupEventListeners() {
        // Search form
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.searchPapers();
            });
        }

        // Generate draft button
        const generateBtn = document.getElementById('generateDraftBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.generateDraft();
            });
        }

        // Chat form
        const chatForm = document.getElementById('chatForm');
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendChatMessage();
            });
        }
    }

    async searchPapers() {
        const query = document.getElementById('searchQuery').value;
        const maxResults = document.getElementById('maxResults').value || 10;
        
        if (!query) {
            this.showNotification('Please enter a search query', 'error');
            return;
        }

        this.showLoading('Searching papers...');

        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, max_results: parseInt(maxResults) })
            });

            const data = await response.json();

            if (data.success) {
                this.papers = data.results;
                this.displaySearchResults(data.results);
                this.showNotification(`Found ${data.count} papers`, 'success');
            } else {
                this.showNotification(data.error || 'Search failed', 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displaySearchResults(results) {
        const container = document.getElementById('searchResults');
        if (!container) return;

        if (results.length === 0) {
            container.innerHTML = '<p class="no-results">No papers found</p>';
            return;
        }

        container.innerHTML = results.map((paper, index) => `
            <div class="paper-card">
                <div class="paper-header">
                    <input type="checkbox" class="paper-checkbox" data-index="${index}">
                    <h3>${paper.title || 'Untitled'}</h3>
                </div>
                <p class="paper-authors">${paper.authors || 'Unknown authors'}</p>
                <p class="paper-abstract">${paper.abstract || 'No abstract available'}</p>
                <div class="paper-meta">
                    <span>Year: ${paper.year || 'N/A'}</span>
                    <span>Citations: ${paper.citationCount || 0}</span>
                </div>
            </div>
        `).join('');

        // Add checkbox listeners
        container.querySelectorAll('.paper-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const index = parseInt(e.target.dataset.index);
                if (e.target.checked) {
                    this.selectedPapers.add(index);
                } else {
                    this.selectedPapers.delete(index);
                }
            });
        });
    }

    async generateDraft() {
        if (this.selectedPapers.size === 0) {
            this.showNotification('Please select at least one paper', 'error');
            return;
        }

        const selectedPapersData = Array.from(this.selectedPapers).map(i => this.papers[i]);
        const customInstructions = document.getElementById('customInstructions')?.value || '';

        this.showLoading('Generating draft...');

        try {
            const response = await fetch('/api/generate_draft', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    selected_papers: selectedPapersData,
                    custom_instructions: customInstructions
                })
            });

            const data = await response.json();

            if (data.success) {
                this.currentDraft = data.draft;
                this.displayDraft(data.draft);
                this.showNotification('Draft generated successfully', 'success');
            } else {
                this.showNotification(data.error || 'Draft generation failed', 'error');
            }
        } catch (error) {
            this.showNotification('Error: ' + error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayDraft(draft) {
        const container = document.getElementById('draftOutput');
        if (!container) return;

        container.innerHTML = `
            <div class="draft-content">
                <pre>${draft}</pre>
            </div>
        `;
    }

    async sendChatMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();

        if (!message) return;

        this.addChatMessage(message, 'user');
        input.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message,
                    context: { draft: this.currentDraft }
                })
            });

            const data = await response.json();

            if (data.success) {
                this.addChatMessage(data.response, 'assistant');
            } else {
                this.addChatMessage('Error: ' + (data.error || 'Unknown error'), 'error');
            }
        } catch (error) {
            this.addChatMessage('Error: ' + error.message, 'error');
        }
    }

    addChatMessage(message, type) {
        const container = document.getElementById('chatMessages');
        if (!container) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}`;
        messageDiv.textContent = message;
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
    }

    loadSearchResults() {
        // Load any cached results from localStorage
        const cached = localStorage.getItem('searchResults');
        if (cached) {
            try {
                this.papers = JSON.parse(cached);
                this.displaySearchResults(this.papers);
            } catch (e) {
                console.error('Failed to load cached results', e);
            }
        }
    }

    showLoading(message) {
        const loader = document.getElementById('loadingIndicator');
        if (loader) {
            loader.textContent = message;
            loader.style.display = 'block';
        }
    }

    hideLoading() {
        const loader = document.getElementById('loadingIndicator');
        if (loader) {
            loader.style.display = 'none';
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.agent = new AIResearchAgent();
});

// AI Research Agent - Frontend JavaScript
// Dark-themed interactive web interface

class AIResearchAgent {
    constructor() {
        this.socket = io();
        this.currentTab = 'search';
        this.papers = [];
        this.selectedPapers = new Set();
        this.activeOperations = {};
        this.currentDraft = null; // Store current draft for corrections
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupSocketListeners();
        this.loadPapers();
        this.loadDownloadedPapers();
        this.loadSearchResults();
        this.loadPapersDirectory();
        this.updateDraftPaperList();
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

        // Extract buttons
        const extractSelectedBtn = document.getElementById('extractSelectedBtn');
        if (extractSelectedBtn) {
            extractSelectedBtn.addEventListener('click', () => {
                this.extractSelectedPaper();
            });
        }

        const extractAllBtn = document.getElementById('extractAllBtn');
        if (extractAllBtn) {
            extractAllBtn.addEventListener('click', () => {
                this.extractText();
            });
        }

        // Extract paper selection
        const extractPaperSelect = document.getElementById('extractPaperSelect');
        if (extractPaperSelect) {
            extractPaperSelect.addEventListener('change', (e) => {
                const extractBtn = document.getElementById('extractSelectedBtn');
                if (extractBtn) {
                    extractBtn.disabled = !e.target.value;
                }
            });
        }

        // Refresh papers directory button
        const refreshPapersBtn = document.getElementById('refreshPapersBtn');
        if (refreshPapersBtn) {
            refreshPapersBtn.addEventListener('click', () => {
                this.loadPapersDirectory();
            });
        }

        // Analyze button
        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => {
                this.analyzePaper();
            });
        }

        // Compare button
        const compareBtn = document.getElementById('compareBtn');
        if (compareBtn) {
            compareBtn.addEventListener('click', () => {
                this.comparePapers();
            });
        }

        // Draft generation buttons
        const generateDraftBtn = document.getElementById('generateDraftBtn');
        if (generateDraftBtn) {
            generateDraftBtn.addEventListener('click', () => {
                this.generateDraft();
            });
        }

        const generateComprehensiveBtn = document.getElementById('generateComprehensiveBtn');
        if (generateComprehensiveBtn) {
            generateComprehensiveBtn.addEventListener('click', () => {
                this.generateComprehensiveDraft();
            });
        }

        // Paper selection
        const paperSelect = document.getElementById('paperSelect');
        if (paperSelect) {
            paperSelect.addEventListener('change', (e) => {
                const analyzeBtn = document.getElementById('analyzeBtn');
                if (analyzeBtn) {
                    analyzeBtn.disabled = !e.target.value;
                }
            });
        }
        
        // AI Conversation Mode
        const useAIConversation = document.getElementById('useAIConversation');
        if (useAIConversation) {
            useAIConversation.addEventListener('change', (e) => {
                const aiChatInterface = document.getElementById('aiChatInterface');
                if (aiChatInterface) {
                    aiChatInterface.style.display = e.target.checked ? 'block' : 'none';
                }
            });
        }
        
        // AI Chat Send Button
        const aiChatSendBtn = document.getElementById('aiChatSendBtn');
        if (aiChatSendBtn) {
            aiChatSendBtn.addEventListener('click', () => {
                this.sendAIMessage();
            });
        }
        
        // AI Chat Input Enter Key
        const aiChatInput = document.getElementById('aiChatInput');
        if (aiChatInput) {
            aiChatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendAIMessage();
                }
            });
        }
        
        // PDF Download buttons
        const downloadComprehensivePdfBtn = document.getElementById('downloadComprehensivePdfBtn');
        if (downloadComprehensivePdfBtn) {
            downloadComprehensivePdfBtn.addEventListener('click', () => {
                this.downloadDraftPDF('comprehensive');
            });
        }
        
        const downloadTopicWisePdfBtn = document.getElementById('downloadTopicWisePdfBtn');
        if (downloadTopicWisePdfBtn) {
            downloadTopicWisePdfBtn.addEventListener('click', () => {
                this.downloadDraftPDF('topic_wise');
            });
        }
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
        
        const tabButton = document.querySelector(`[data-tab="${tabName}"]`);
        if (tabButton) {
            tabButton.classList.add('active');
        }

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        const tabContent = document.getElementById(tabName);
        if (tabContent) {
            tabContent.classList.add('active');
        }

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

    async extractSelectedPaper() {
        const paperFile = document.getElementById('extractPaperSelect').value;
        
        if (!paperFile) {
            this.showNotification('Please select a paper to extract', 'error');
            return;
        }

        try {
            this.showProgress('extract', 'Starting text extraction...');
            
            const response = await fetch('/api/extract_selected_paper', {
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

    async loadPapersDirectory() {
        try {
            const response = await fetch('/api/view_papers_directory');
            const data = await response.json();
            
            this.displayPapersDirectory(data.papers || [], data.total_count || 0);
        } catch (error) {
            console.error('Failed to load papers directory:', error);
        }
    }

    displayPapersDirectory(papers, totalCount) {
        const papersList = document.getElementById('papersDirectoryList');
        
        if (papers.length === 0) {
            papersList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No papers found in data/papers directory.</p>';
            return;
        }

        papersList.innerHTML = `<div style="color: var(--text-secondary); margin-bottom: 1rem;">Found ${totalCount} papers in directory:</div>`;
        
        papers.forEach(paper => {
            const paperItem = document.createElement('div');
            paperItem.className = 'paper-item';
            
            paperItem.innerHTML = `
                <div class="paper-info">
                    <div class="paper-title">${paper.name}</div>
                    <div class="paper-meta">
                        Size: ${(paper.size / 1024).toFixed(1)} KB | 
                        Modified: ${new Date(paper.modified * 1000).toLocaleDateString()}
                    </div>
                </div>
                <div class="paper-actions">
                    <button class="btn btn-sm btn-primary" onclick="window.downloadPaper('${paper.filename}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            `;
            
            papersList.appendChild(paperItem);
        });
    }

    async loadSearchResults() {
        try {
            const response = await fetch('/api/get_search_results');
            const data = await response.json();
            
            this.displaySearchResults(data.papers || []);
        } catch (error) {
            console.error('Failed to load search results:', error);
        }
    }

    displaySearchResults(papers) {
        const resultsContainer = document.getElementById('searchResultsContainer');
        const resultsList = document.getElementById('searchResultsList');
        
        if (papers.length === 0) {
            resultsContainer.style.display = 'none';
            return;
        }

        resultsContainer.style.display = 'block';
        resultsList.innerHTML = '';
        
        papers.forEach(paper => {
            const paperItem = document.createElement('div');
            paperItem.className = 'paper-item';
            
            paperItem.innerHTML = `
                <div class="paper-info">
                    <div class="paper-title">${paper.name}</div>
                    <div class="paper-meta">
                        Size: ${(paper.size / 1024).toFixed(1)} KB | 
                        Modified: ${new Date(paper.modified * 1000).toLocaleDateString()}
                    </div>
                </div>
                <div class="paper-actions">
                    <button class="btn btn-sm btn-primary" onclick="window.downloadPaper('${paper.file}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            `;
            
            resultsList.appendChild(paperItem);
        });
    }

    updateExtractPaperSelect() {
        const select = document.getElementById('extractPaperSelect');
        if (!select) return;
        
        select.innerHTML = '<option value="">Select a paper...</option>';
        
        this.downloadedPapers.forEach(paper => {
            const option = document.createElement('option');
            option.value = paper.file;
            option.textContent = paper.name;
            select.appendChild(option);
        });
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

    async generateDraft() {
        if (this.selectedPapers.size === 0) {
            this.showNotification('Please select at least 1 paper for draft generation', 'error');
            return;
        }

        const topic = document.getElementById('draftTopic').value.trim();
        if (!topic) {
            this.showNotification('Please enter a research topic', 'error');
            return;
        }

        const sectionType = document.getElementById('draftSectionType').value;
        const paperFiles = Array.from(this.selectedPapers);
        const customInstructions = document.getElementById('customInstructions').value.trim();
        const useAIConversation = document.getElementById('useAIConversation').checked;

        try {
            this.showProgress('draft', 'Generating draft...');

            // Check if using conversational AI mode
            if (useAIConversation) {
                // Load paper data for context
                const papersData = await this.loadPapersData(paperFiles);
                
                const response = await fetch('/api/ai_generate_conversational', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        section_type: sectionType,
                        topic: topic,
                        papers: papersData,
                        instruction: customInstructions
                    })
                });

                const data = await response.json();

                if (data.status === 'started') {
                    this.activeOperations[data.operation_id] = 'draft';
                    this.showNotification('AI is working on your draft...', 'success');
                } else {
                    this.hideProgress('draft');
                    this.showNotification('Failed to start AI generation', 'error');
                }
            } else if (customInstructions) {
                // Use custom instructions endpoint
                const response = await fetch('/api/generate_with_instructions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        paper_files: paperFiles,
                        section_type: sectionType,
                        topic: topic,
                        custom_instructions: customInstructions
                    })
                });

                const data = await response.json();

                if (data.status === 'started') {
                    this.activeOperations[data.operation_id] = 'draft';
                    this.showNotification('Draft generation with custom instructions started', 'success');
                } else {
                    this.hideProgress('draft');
                    this.showNotification('Failed to start draft generation', 'error');
                }
            } else {
                // Use standard endpoint
                const response = await fetch('/api/generate_draft', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        paper_files: paperFiles,
                        section_type: sectionType,
                        topic: topic
                    })
                });

                const data = await response.json();

                if (data.status === 'started') {
                    this.activeOperations[data.operation_id] = 'draft';
                    this.showNotification('Draft generation started', 'success');
                } else {
                    this.hideProgress('draft');
                    this.showNotification('Failed to start draft generation', 'error');
                }
            }
        } catch (error) {
            this.hideProgress('draft');
            this.showNotification('Draft generation failed: ' + error.message, 'error');
        }
    }
    
    async loadPapersData(paperFiles) {
        // Helper to load paper data for AI context
        const papersData = [];
        for (const file of paperFiles) {
            papersData.push({
                title: file.split('/').pop().replace('_extracted.txt', ''),
                file: file
            });
        }
        return papersData;
    }
    
    async sendAIMessage() {
        const input = document.getElementById('aiChatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        const topic = document.getElementById('draftTopic').value.trim();
        const paperFiles = Array.from(this.selectedPapers);
        
        // Add user message to chat
        this.addChatMessage(message, 'user');
        input.value = '';
        
        try {
            // Load paper data
            const papersData = await this.loadPapersData(paperFiles);
            
            const response = await fetch('/api/ai_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    topic: topic,
                    papers: papersData
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addChatMessage(data.response, 'ai');
            } else {
                this.addChatMessage('Sorry, I encountered an error: ' + data.error, 'ai');
            }
        } catch (error) {
            this.addChatMessage('Sorry, I encountered an error: ' + error.message, 'ai');
        }
    }
    
    addChatMessage(message, role) {
        const messagesContainer = document.getElementById('aiChatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = role === 'user' ? 'user-message' : 'ai-message';
        messageDiv.textContent = message;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async generateComprehensiveDraft() {
        if (this.selectedPapers.size === 0) {
            this.showNotification('Please select at least 1 paper for comprehensive draft generation', 'error');
            return;
        }

        const topic = document.getElementById('draftTopic').value.trim();
        if (!topic) {
            this.showNotification('Please enter a research topic', 'error');
            return;
        }

        const paperFiles = Array.from(this.selectedPapers);
        const customInstructions = document.getElementById('customInstructions').value.trim();

        try {
            this.showProgress('draft', 'Generating comprehensive draft...');

            // Note: For comprehensive drafts, custom instructions apply to all sections
            // In future, could add per-section instructions
            const response = await fetch('/api/generate_comprehensive_draft', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    paper_files: paperFiles,
                    topic: topic,
                    custom_instructions: customInstructions || null
                })
            });

            const data = await response.json();

            if (data.status === 'started') {
                this.activeOperations[data.operation_id] = 'draft';
                this.showNotification('Comprehensive draft generation started', 'success');
            } else {
                this.hideProgress('draft');
                this.showNotification('Failed to start comprehensive draft generation', 'error');
            }
        } catch (error) {
            this.hideProgress('draft');
            this.showNotification('Comprehensive draft generation failed: ' + error.message, 'error');
        }
    }

    async loadDownloadedPapers() {
        try {
            const response = await fetch('/api/get_downloaded_papers');
            const data = await response.json();
            
            this.downloadedPapers = data.papers || [];
            this.updateExtractPaperSelect();
        } catch (error) {
            console.error('Failed to load downloaded papers:', error);
        }
    }

    async loadPapers() {
        try {
            const response = await fetch('/api/get_papers');
            const data = await response.json();
            
            this.papers = data.papers || [];
            this.updatePaperSelect();
            this.updatePaperList();
            this.updateDraftPaperList();
        } catch (error) {
            console.error('Failed to load papers:', error);
        }
    }

    updatePaperSelect() {
        const select = document.getElementById('paperSelect');
        if (!select) return;
        
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
        if (!paperList) return;
        
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
            if (checkbox) {
                checkbox.addEventListener('change', (e) => {
                    if (e.target.checked) {
                        this.selectedPapers.add(paper.file);
                    } else {
                        this.selectedPapers.delete(paper.file);
                    }
                    this.updateCompareButton();
                });
            }
            
            paperList.appendChild(paperItem);
        });
    }

    updateCompareButton() {
        const compareBtn = document.getElementById('compareBtn');
        const generateDraftBtn = document.getElementById('generateDraftBtn');
        const generateComprehensiveBtn = document.getElementById('generateComprehensiveBtn');
        
        const hasSelectedPapers = this.selectedPapers.size > 0;
        
        if (compareBtn) {
            compareBtn.disabled = this.selectedPapers.size < 2;
        }
        if (generateDraftBtn) {
            generateDraftBtn.disabled = !hasSelectedPapers;
        }
        if (generateComprehensiveBtn) {
            generateComprehensiveBtn.disabled = !hasSelectedPapers;
        }
    }

    updateDraftPaperList() {
        const draftPaperList = document.getElementById('draftPaperList');
        if (!draftPaperList) return;
        
        draftPaperList.innerHTML = '';
        
        // Combine both extracted papers and section papers
        const allPapers = [...this.papers, ...this.getSectionPapers()];
        
        if (allPapers.length === 0) {
            draftPaperList.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 2rem;">No papers available. Please extract text from PDFs first.</p>';
            return;
        }
        
        allPapers.forEach(paper => {
            const paperItem = document.createElement('div');
            paperItem.className = 'paper-item';
            
            const isSelected = this.selectedPapers.has(paper.file);
            
            paperItem.innerHTML = `
                <div class="paper-info">
                    <div class="paper-title">${paper.name}</div>
                    <div class="paper-meta">
                        ${paper.size ? `Size: ${(paper.size / 1024).toFixed(1)} KB | ` : ''}
                        ${paper.modified ? `Modified: ${new Date(paper.modified * 1000).toLocaleDateString()}` : ''}
                        ${paper.sections ? `Sections: ${paper.sections}` : ''}
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
            if (checkbox) {
                checkbox.addEventListener('change', (e) => {
                    if (e.target.checked) {
                        this.selectedPapers.add(paper.file);
                    } else {
                        this.selectedPapers.delete(paper.file);
                    }
                    this.updateCompareButton();
                });
            }
            
            draftPaperList.appendChild(paperItem);
        });
    }

    getSectionPapers() {
        // Get section analysis papers
        const sectionPapers = [];
        try {
            // This would need to be implemented to fetch section papers
            // For now, return empty array
        } catch (error) {
            console.error('Failed to load section papers:', error);
        }
        return sectionPapers;
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
        } else if (operationType === 'draft') {
            this.displayDraftResults(result);
        } else if (operationType === 'correction' || operationType === 'improvement') {
            this.displayCorrectionResults(result);
        } else if (operationType === 'extract') {
            // Show extracted text if available
            if (result.extracted_text) {
                this.displayExtractedText(result);
            }
            // Reload papers after extraction
            this.loadPapers();
            this.loadDownloadedPapers();
            this.loadSearchResults();
            this.loadPapersDirectory();
        } else if (operationType === 'search') {
            // Reload papers after search
            this.loadPapers();
            this.loadDownloadedPapers();
            this.loadSearchResults();
            this.loadPapersDirectory();
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

    displayDraftResults(result) {
        if (result.drafts) {
            // Comprehensive draft results
            this.displayComprehensiveDraftResults(result);
        } else if (result.draft) {
            // Single draft results
            this.displaySingleDraftResults(result);
        }
    }

    displaySingleDraftResults(result) {
        const resultsContainer = document.getElementById('draftResults');
        const comprehensiveResultsContainer = document.getElementById('comprehensiveDraftResults');
        
        if (!resultsContainer) {
            console.error('draftResults element not found');
            return;
        }
        
        resultsContainer.style.display = 'block';
        if (comprehensiveResultsContainer) {
            comprehensiveResultsContainer.style.display = 'none';
        }
        
        const draft = result.draft;
        
        // Debug logging
        console.log('Draft result:', draft);
        console.log('Draft content length:', draft.content ? draft.content.length : 0);
        
        const confidenceClass = draft.confidence_score > 0.8 ? 'confidence-high' : 
                               draft.confidence_score > 0.6 ? 'confidence-medium' : 'confidence-low';
        
        let html = `
            <h4><i class="fas fa-file-alt"></i> Generated Draft</h4>
        `;
        
        // Show AI explanation if available
        if (draft.ai_explanation) {
            html += `
                <div class="ai-explanation">
                    <div class="ai-explanation-title">
                        <i class="fas fa-robot"></i> AI's Approach
                    </div>
                    <div>${this.escapeHtml(draft.ai_explanation)}</div>
                </div>
            `;
        }
        
        html += `
            <div class="draft-meta">
                <div class="draft-meta-item">
                    <i class="fas fa-file-alt"></i>
                    <span>${draft.title}</span>
                </div>
                <div class="draft-meta-item">
                    <span>Word Count:</span>
                    <span>${draft.word_count}</span>
                </div>
                <div class="draft-meta-item confidence-score ${confidenceClass}">
                    <span>Confidence:</span>
                    <span>${(draft.confidence_score * 100).toFixed(1)}%</span>
                </div>
            </div>
            
            <div style="margin: 1rem 0;">
                <h5 style="color: var(--accent-primary); margin-bottom: 0.5rem;">
                    <i class="fas fa-file-text"></i> Draft Content
                </h5>
            </div>
            
            <div class="draft-content" id="currentDraftContent" style="background: var(--bg-card); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border); white-space: pre-wrap; line-height: 1.8; max-height: 600px; overflow-y: auto; font-size: 1rem; color: var(--text-primary);">
                ${this.escapeHtml(draft.content || 'No content generated')}
            </div>
            
            <!-- Correction Section -->
            <div id="correctionSection" style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">
                <h5 style="color: var(--accent-primary); margin-bottom: 1rem;">
                    <i class="fas fa-edit"></i> Improve with AI
                </h5>
                <div class="form-group">
                    <label for="correctionInstructions">Tell AI what to improve:</label>
                    <textarea id="correctionInstructions" class="form-control" rows="3" placeholder="Tell the AI what to fix or improve (e.g., 'Make it more concise', 'Add more technical details', 'Improve the flow')"></textarea>
                </div>
                <button id="correctDraftBtn" class="btn btn-primary">
                    <i class="fas fa-magic"></i> Improve Draft with AI
                </button>
            </div>
        `;
        
        resultsContainer.innerHTML = html;
        
        // Store current draft data for correction
        this.currentDraft = {
            content: draft.content,
            section_type: draft.section_type
        };
        
        // Add event listener for correction button
        const correctBtn = document.getElementById('correctDraftBtn');
        if (correctBtn) {
            correctBtn.addEventListener('click', () => {
                this.correctDraft();
            });
        }
    }

    displayComprehensiveDraftResults(result) {
        const resultsContainer = document.getElementById('draftResults');
        const comprehensiveResultsContainer = document.getElementById('comprehensiveDraftResults');
        
        if (!comprehensiveResultsContainer) {
            console.error('comprehensiveDraftResults element not found');
            return;
        }
        
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
        }
        comprehensiveResultsContainer.style.display = 'block';
        
        const drafts = result.drafts;
        let html = '<h4><i class="fas fa-file-alt"></i> Comprehensive Draft</h4>';
        
        // Helper function to capitalize section names
        const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);
        
        Object.keys(drafts).forEach(sectionType => {
            const draft = drafts[sectionType];
            if (draft.error) {
                html += `
                    <div class="draft-section">
                        <h5><i class="fas fa-exclamation-triangle"></i> ${capitalize(sectionType)}</h5>
                        <div style="color: var(--error); padding: 1rem; background: rgba(255, 68, 68, 0.1); border-radius: 4px;">
                            ${draft.error}
                        </div>
                    </div>
                `;
            } else {
                const confidenceClass = draft.confidence_score > 0.8 ? 'confidence-high' : 
                                       draft.confidence_score > 0.6 ? 'confidence-medium' : 'confidence-low';
                
                html += `
                    <div class="draft-section">
                        <h5>${capitalize(sectionType)}</h5>
                        <div class="draft-meta">
                            <div class="draft-meta-item">
                                <span>Word Count:</span>
                                <span>${draft.word_count}</span>
                            </div>
                            <div class="draft-meta-item confidence-score ${confidenceClass}">
                                <span>Confidence:</span>
                                <span>${(draft.confidence_score * 100).toFixed(1)}%</span>
                            </div>
                        </div>
                        <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 8px; margin-top: 1rem; max-height: 500px; overflow-y: auto; white-space: pre-wrap; line-height: 1.8; font-size: 0.95rem; color: var(--text-primary);">
                            ${draft.content}
                        </div>
                    </div>
                `;
            }
        });
        
        comprehensiveResultsContainer.innerHTML = html;
    }

    async correctDraft() {
        const correctionInstructions = document.getElementById('correctionInstructions').value.trim();
        
        if (!correctionInstructions) {
            this.showNotification('Please enter improvement instructions', 'error');
            return;
        }
        
        if (!this.currentDraft) {
            this.showNotification('No draft available to improve', 'error');
            return;
        }
        
        const useAIConversation = document.getElementById('useAIConversation').checked;
        
        try {
            this.showProgress('draft', 'AI is improving your draft...');
            
            if (useAIConversation) {
                // Use conversational AI improvement
                const response = await fetch('/api/ai_improve_draft', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        draft_content: this.currentDraft.content,
                        improvement_request: correctionInstructions
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'started') {
                    this.activeOperations[data.operation_id] = 'improvement';
                    this.showNotification('AI is working on improvements...', 'success');
                } else {
                    this.hideProgress('draft');
                    this.showNotification('Failed to start improvement', 'error');
                }
            } else {
                // Use standard correction
                const response = await fetch('/api/correct_draft', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        draft_content: this.currentDraft.content,
                        correction_instructions: correctionInstructions,
                        section_type: this.currentDraft.section_type
                    })
                });
                
                const data = await response.json();
                
                if (data.status === 'started') {
                    this.activeOperations[data.operation_id] = 'correction';
                    this.showNotification('AI correction started', 'success');
                } else {
                    this.hideProgress('draft');
                    this.showNotification('Failed to start correction', 'error');
                }
            }
        } catch (error) {
            this.hideProgress('draft');
            this.showNotification('Improvement failed: ' + error.message, 'error');
        }
    }

    displayCorrectionResults(result) {
        // Update the draft content with corrected version
        const draftContentElement = document.getElementById('currentDraftContent');
        
        const correctedContent = result.improved_content || result.corrected_content;
        const aiExplanation = result.ai_explanation;
        
        console.log('Correction result:', result);
        console.log('Corrected content length:', correctedContent ? correctedContent.length : 0);
        
        if (draftContentElement && correctedContent) {
            // Show AI explanation if available
            if (aiExplanation) {
                // Check if explanation already exists
                let explanationDiv = draftContentElement.previousElementSibling;
                if (!explanationDiv || !explanationDiv.classList.contains('ai-explanation')) {
                    explanationDiv = document.createElement('div');
                    explanationDiv.className = 'ai-explanation';
                    draftContentElement.parentNode.insertBefore(explanationDiv, draftContentElement);
                }
                
                explanationDiv.innerHTML = `
                    <div class="ai-explanation-title">
                        <i class="fas fa-robot"></i> AI's Improvements
                    </div>
                    <div>${this.escapeHtml(aiExplanation)}</div>
                `;
            }
            
            // Update the displayed content with proper escaping
            draftContentElement.textContent = correctedContent;
            
            // Update stored draft
            this.currentDraft.content = correctedContent;
            
            // Show success message with word count change
            const wordCountChange = result.word_count - result.original_word_count;
            const changeText = wordCountChange > 0 ? `+${wordCountChange}` : wordCountChange;
            
            this.showNotification(
                `Draft improved successfully! Word count: ${result.original_word_count} → ${result.word_count} (${changeText})`,
                'success'
            );
            
            // Clear correction instructions
            const correctionTextarea = document.getElementById('correctionInstructions');
            if (correctionTextarea) {
                correctionTextarea.value = '';
            }
            
            // Scroll to the updated content
            draftContentElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            console.error('Failed to display improved draft - element or content missing');
            this.showNotification('Failed to display improved draft', 'error');
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    displayExtractedText(result) {
        // Create or get extracted text container
        let extractedTextContainer = document.getElementById('extractedTextResults');
        
        if (!extractedTextContainer) {
            // Create container if it doesn't exist
            const extractTab = document.getElementById('extract');
            if (!extractTab) return;
            
            extractedTextContainer = document.createElement('div');
            extractedTextContainer.id = 'extractedTextResults';
            extractedTextContainer.className = 'card';
            extractedTextContainer.style.marginTop = '2rem';
            extractTab.appendChild(extractedTextContainer);
        }
        
        extractedTextContainer.style.display = 'block';
        
        const wordCount = result.word_count || 0;
        const charCount = result.char_count || 0;
        const extractedText = result.extracted_text || '';
        
        extractedTextContainer.innerHTML = `
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <h3 class="card-title">Extracted Text</h3>
            </div>
            
            <div class="stats-grid" style="margin-bottom: 1.5rem;">
                <div class="stat-card">
                    <div class="stat-value">${wordCount.toLocaleString()}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${charCount.toLocaleString()}</div>
                    <div class="stat-label">Characters</div>
                </div>
            </div>
            
            <div style="margin-bottom: 1rem; display: flex; justify-content: flex-end;">
                <button id="copyExtractedTextBtn" class="btn btn-primary" style="display: flex; align-items: center; gap: 0.5rem;">
                    <i class="fas fa-copy"></i> Copy Text
                </button>
            </div>
            
            <div id="extractedTextContent" style="background: var(--bg-card); padding: 1.5rem; border-radius: 8px; max-height: 500px; overflow-y: auto; white-space: pre-wrap; line-height: 1.8; font-size: 0.9rem; color: var(--text-primary); border: 1px solid var(--border);">
                ${extractedText}
            </div>
        `;
        
        // Add copy button functionality
        const copyBtn = document.getElementById('copyExtractedTextBtn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(extractedText).then(() => {
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    copyBtn.style.background = 'var(--success)';
                    
                    setTimeout(() => {
                        copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy Text';
                        copyBtn.style.background = '';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text:', err);
                    this.showNotification('Failed to copy text', 'error');
                });
            });
        }
        
        // Scroll to extracted text
        extractedTextContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
        
        if (!progressContainer) {
            console.warn(`Progress container ${type}Progress not found`);
            return;
        }
        
        progressContainer.style.display = 'block';
        if (progressFill) {
            progressFill.style.width = '0%';
        }
        if (progressText) {
            progressText.textContent = message;
        }
    }

    updateProgress(type, progress, message) {
        const progressFill = document.getElementById(`${type}ProgressFill`);
        const progressText = document.getElementById(`${type}ProgressText`);
        
        if (progressFill) {
            progressFill.style.width = `${progress}%`;
        }
        if (progressText) {
            progressText.textContent = message;
        }
    }

    hideProgress(type) {
        const progressContainer = document.getElementById(`${type}Progress`);
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
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
    
    async downloadDraftPDF(pdfType) {
        if (!this.currentDraft) {
            this.showNotification('No draft available to download', 'error');
            return;
        }
        
        try {
            this.showNotification(`Generating ${pdfType} PDF...`, 'info');
            
            const response = await fetch('/api/download_draft_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    draft_text: this.currentDraft,
                    pdf_type: pdfType,
                    title: 'Research Draft - AI Generated'
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to generate PDF');
            }
            
            // Get the blob and create download link
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${pdfType}_draft_${new Date().getTime()}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            this.showNotification(`${pdfType} PDF downloaded successfully!`, 'success');
            
        } catch (error) {
            console.error('Error downloading PDF:', error);
            this.showNotification('Failed to download PDF: ' + error.message, 'error');
        }
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
    
    // Clear session on page unload (close/refresh)
    window.addEventListener('beforeunload', () => {
        // Use sendBeacon for reliable cleanup on page close
        const clearUrl = '/api/clear_session';
        const data = new Blob([JSON.stringify({})], { type: 'application/json' });
        navigator.sendBeacon(clearUrl, data);
    });
});

// Global window functions for paper actions
window.downloadPaper = (file) => {
    const filename = file.split('\\').pop().split('/').pop();
    window.open(`/api/download_paper/${filename}`, '_blank');
};

window.extractPaper = (file) => {
    const select = document.getElementById('extractPaperSelect');
    select.value = file;
    document.getElementById('extractSelectedBtn').disabled = false;
    window.aiResearchAgent.extractSelectedPaper();
};

/**
 * AI Application Compiler - Frontend JavaScript
 * Handles UI interactions and API communication
 */

class AppCompiler {
    constructor() {
        this.currentResult = null;
        this.initializeEventListeners();
        this.loadExamplePrompt();
    }

    initializeEventListeners() {
        document.getElementById('compileBtn').addEventListener('click', () => this.compile());
        document.getElementById('clearBtn').addEventListener('click', () => this.clear());
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadJSON());

        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Allow Enter+Cmd/Ctrl to compile
        document.getElementById('promptInput').addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.compile();
            }
        });
    }

    loadExamplePrompt() {
        const examples = [
            "Build a CRM system with Users, Contacts, Companies, and Deals. Include role-based access (admin/user), email integration, and activity tracking.",
            "Create an inventory management system with Products, Warehouses, Orders, and Suppliers. Include real-time stock tracking and low-stock alerts.",
            "Build a social media platform with Users, Posts, Comments, Likes, and Followers. Include notifications and user profiles."
        ];
        
        // Randomly select an example on page load
        const randomExample = examples[Math.floor(Math.random() * examples.length)];
        // Uncomment to show example
        // document.getElementById('promptInput').placeholder = randomExample;
    }

    async compile() {
        const prompt = document.getElementById('promptInput').value.trim();
        
        if (!prompt) {
            this.showError('Please enter an application description');
            return;
        }

        this.showLoading();
        this.hideError();

        try {
            console.log('[v0] Sending compilation request...');
            const response = await fetch('/api/compile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Compilation failed');
            }

            const data = await response.json();
            console.log('[v0] Compilation successful:', data);

            this.currentResult = data;
            this.displayResults(data);
            this.hideLoading();
            
            // Scroll to results
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('[v0] Compilation error:', error);
            this.showError(error.message);
            this.hideLoading();
        }
    }

    displayResults(data) {
        document.getElementById('resultsSection').style.display = 'block';

        // Update overview tab
        document.getElementById('appName').textContent = data.app_name;
        document.getElementById('overviewApp').textContent = data.app_name;
        document.getElementById('overviewDesc').textContent = data.description || 'Application for ' + data.app_name;

        // Entities
        const entitiesList = document.getElementById('overviewEntities');
        entitiesList.innerHTML = data.entities.map(e => `<li><strong>${e.name}</strong> (${e.attributes.length} fields)</li>`).join('');

        // Roles
        const rolesList = document.getElementById('overviewRoles');
        rolesList.innerHTML = data.roles.map(r => `<li>${r}</li>`).join('');

        // Features
        const featuresList = document.getElementById('overviewFeatures');
        featuresList.innerHTML = data.features.map(f => `<li>${f}</li>`).join('');

        // Integrations
        const integrationsList = document.getElementById('overviewIntegrations');
        integrationsList.innerHTML = data.integrations.length > 0 
            ? data.integrations.map(i => `<li>${i}</li>`).join('')
            : '<li>None specified</li>';

        // Database Schema
        const dbContent = document.getElementById('dbContent');
        dbContent.innerHTML = `<pre>${JSON.stringify(data.database_schema, null, 2)}</pre>`;

        // API Schema
        const apiContent = document.getElementById('apiContent');
        const apiEndpoints = data.api_schema.endpoints.map(e => 
            `${e.method.padEnd(8)} ${e.path.padEnd(30)} → ${e.entity_name}`
        ).join('\n');
        apiContent.innerHTML = `<pre>Endpoints (${data.api_schema.endpoints.length}):\n\n${apiEndpoints}</pre>`;

        // UI Schema
        const uiContent = document.getElementById('uiContent');
        const uiPages = data.ui_schema.pages.map(p => 
            `${p.name.padEnd(25)} Route: ${p.route || '/'}  Auth: ${p.requires_auth}`
        ).join('\n');
        uiContent.innerHTML = `<pre>Pages (${data.ui_schema.pages.length}):\n\n${uiPages}</pre>`;

        // Auth Schema
        const authContent = document.getElementById('authContent');
        authContent.innerHTML = `<pre>${JSON.stringify(data.auth_schema, null, 2)}</pre>`;

        // Diagnostics
        const confidenceScore = document.getElementById('confidenceScore');
        const confidence = Math.round(data.diagnostics.confidence * 100);
        confidenceScore.textContent = `${confidence}%`;
        confidenceScore.style.color = confidence > 80 ? '#10b981' : confidence > 60 ? '#f59e0b' : '#ef4444';

        const warningsList = document.getElementById('warningsList');
        warningsList.innerHTML = data.diagnostics.warnings.length > 0
            ? data.diagnostics.warnings.map(w => `<li>${w}</li>`).join('')
            : '<li>No warnings</li>';

        const assumptionsList = document.getElementById('assumptionsList');
        assumptionsList.innerHTML = data.diagnostics.assumptions.length > 0
            ? data.diagnostics.assumptions.map(a => `<li>${a}</li>`).join('')
            : '<li>No assumptions needed</li>';

        const repairsList = document.getElementById('repairsList');
        repairsList.innerHTML = data.diagnostics.repairs.length > 0
            ? data.diagnostics.repairs.map(r => `<li>${r}</li>`).join('')
            : '<li>No repairs needed</li>';

        // Switch to overview tab
        this.switchTab('overview');
    }

    switchTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    }

    downloadJSON() {
        if (!this.currentResult) return;

        const jsonStr = JSON.stringify(this.currentResult, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${this.currentResult.app_name}_specification.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    clear() {
        document.getElementById('promptInput').value = '';
        document.getElementById('resultsSection').style.display = 'none';
        this.hideError();
        this.hideLoading();
    }

    showLoading() {
        document.getElementById('loadingMsg').style.display = 'flex';
        document.getElementById('compileBtn').disabled = true;
    }

    hideLoading() {
        document.getElementById('loadingMsg').style.display = 'none';
        document.getElementById('compileBtn').disabled = false;
    }

    showError(message) {
        const errorMsg = document.getElementById('errorMsg');
        errorMsg.textContent = message;
        errorMsg.style.display = 'block';
    }

    hideError() {
        document.getElementById('errorMsg').style.display = 'none';
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('[v0] Initializing AI Application Compiler...');
    window.appCompiler = new AppCompiler();
    console.log('[v0] Application ready');
});

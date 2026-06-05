// AI Application Compiler - Turn-by-Turn Chat Interface
class CompilerChat {
  constructor() {
    this.conversationId = null;
    this.currentIntent = null;
    this.isLoading = false;

    this.init();
  }

  init() {
    this.cacheDOM();
    this.attachEventListeners();
    this.startNewConversation();
  }

  cacheDOM() {
    this.userInput = document.getElementById('user-input');
    this.sendBtn = document.getElementById('send-btn');
    this.clearBtn = document.getElementById('clear-btn');
    this.chatMessages = document.getElementById('chat-messages');
    this.previewContent = document.getElementById('preview-content');
    this.statusBadge = document.getElementById('status-badge');
    this.downloadBtn = document.getElementById('download-btn');
    this.newConvBtn = document.getElementById('new-conversation-btn');

    this.assumptionsModal = document.getElementById('assumptions-modal');
    this.assumptionsBody = document.getElementById('assumptions-body');
    this.approveBtn = document.getElementById('approve-btn');
    this.modifyBtn = document.getElementById('modify-btn');

    this.modifyModal = document.getElementById('modify-modal');
    this.modifyInput = document.getElementById('modify-input');
    this.applyChangesBtn = document.getElementById('apply-changes-btn');
    this.cancelChangesBtn = document.getElementById('cancel-changes-btn');
  }

  attachEventListeners() {
    this.sendBtn.addEventListener('click', () => this.sendMessage());
    this.clearBtn.addEventListener('click', () => this.userInput.value = '');
    this.newConvBtn.addEventListener('click', () => this.startNewConversation());
    this.downloadBtn.addEventListener('click', () => this.downloadApp());

    this.userInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && e.ctrlKey) this.sendMessage();
    });

    this.approveBtn.addEventListener('click', () => this.closeModal(this.assumptionsModal));
    this.modifyBtn.addEventListener('click', () => this.openModal(this.modifyModal));
    this.applyChangesBtn.addEventListener('click', () => this.applyChanges());
    this.cancelChangesBtn.addEventListener('click', () => this.closeModal(this.modifyModal));

    // Modal close buttons
    document.querySelectorAll('.close-modal').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.target.closest('.modal').classList.add('hidden');
      });
    });
  }

  async startNewConversation() {
    try {
      this.statusBadge.textContent = 'Starting...';
      const response = await fetch('/api/conversation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) throw new Error('Failed to start conversation');

      const data = await response.json();
      this.conversationId = data.conversation_id;
      this.currentIntent = null;

      this.chatMessages.innerHTML = `
        <div class="message assistant-message welcome">
          <div class="message-content">
            <h3>👋 Welcome to the AI App Compiler</h3>
            <p>I'll help you build an application through turn-by-turn conversation. Here's how it works:</p>
            <ul>
              <li><strong>Describe your app:</strong> Tell me what you want to build</li>
              <li><strong>I'll show assumptions:</strong> I'll ask clarifying questions if I'm not confident</li>
              <li><strong>Refine on the fly:</strong> Change requirements anytime during the conversation</li>
              <li><strong>Download when ready:</strong> Export your complete app as a ZIP file</li>
            </ul>
            <p><strong>Let's start! What would you like to build?</strong></p>
          </div>
        </div>
      `;

      this.previewContent.innerHTML = `
        <div class="empty-state">
          <div class="icon">🚀</div>
          <p>Your app structure will appear here</p>
        </div>
      `;

      this.downloadBtn.disabled = true;
      this.statusBadge.textContent = 'Ready';
      console.log('[Chat] Started conversation:', this.conversationId);
    } catch (error) {
      console.error('[Chat] Error starting conversation:', error);
      this.addMessage('assistant', '❌ Failed to start conversation. Please refresh the page.');
      this.statusBadge.textContent = 'Error';
    }
  }

  async sendMessage() {
    const message = this.userInput.value.trim();
    if (!message || this.isLoading) return;

    this.isLoading = true;
    this.sendBtn.disabled = true;
    this.statusBadge.textContent = 'Processing...';

    try {
      // Add user message to chat
      this.addMessage('user', message);
      this.userInput.value = '';

      // Send to backend
      const response = await fetch(`/api/conversation/${this.conversationId}/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      if (!response.ok) throw new Error('Failed to send message');

      const data = await response.json();

      if (data.status === 'success' && data.response.type === 'assumptions') {
        // Show assumptions modal
        this.showAssumptions(data.response);
        this.currentIntent = data.response.assumptions;
        this.updatePreview(data.response.assumptions);
        this.downloadBtn.disabled = false;
      } else if (data.status === 'clarification_needed') {
        this.addMessage('assistant', data.response.message);
      }

      console.log('[Chat] Message sent successfully');
    } catch (error) {
      console.error('[Chat] Error sending message:', error);
      this.addMessage('assistant', `❌ Error: ${error.message}`);
    } finally {
      this.isLoading = false;
      this.sendBtn.disabled = false;
      this.statusBadge.textContent = 'Ready';
    }
  }

  addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;

    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.innerHTML = `
      <div class="message-content">
        <p>${this.escapeHtml(content)}</p>
        <small class="timestamp">${timestamp}</small>
      </div>
    `;

    this.chatMessages.appendChild(messageDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  showAssumptions(response) {
    const { assumptions, confidence, next_question } = response;

    const html = `
      <div class="assumptions-container">
        <div class="assumption-item">
          <h4>📊 Confidence: <strong>${(confidence * 100).toFixed(0)}%</strong></h4>
        </div>
        
        <div class="assumption-item">
          <h4>🏗️ Entities (${assumptions.entities.length})</h4>
          <ul class="assumption-list">
            ${assumptions.entities.map(e => `<li>${e}</li>`).join('')}
          </ul>
        </div>

        <div class="assumption-item">
          <h4>👥 Roles (${assumptions.roles.length})</h4>
          <ul class="assumption-list">
            ${assumptions.roles.map(r => `<li>${r}</li>`).join('')}
          </ul>
        </div>

        <div class="assumption-item">
          <h4>✨ Features (${assumptions.features.length})</h4>
          <ul class="assumption-list">
            ${assumptions.features.slice(0, 5).map(f => `<li>${f}</li>`).join('')}
            ${assumptions.features.length > 5 ? `<li>... and ${assumptions.features.length - 5} more</li>` : ''}
          </ul>
        </div>

        <div class="assumption-item">
          <h4>🔗 Integrations (${assumptions.integrations.length})</h4>
          <ul class="assumption-list">
            ${assumptions.integrations.length > 0 ? assumptions.integrations.map(i => `<li>${i}</li>`).join('') : '<li>None</li>'}
          </ul>
        </div>

        <div class="next-question">
          <p><strong>❓ ${next_question}</strong></p>
        </div>
      </div>
    `;

    this.assumptionsBody.innerHTML = html;
    this.openModal(this.assumptionsModal);
  }

  updatePreview(assumptions) {
    const html = `
      <div class="preview-structure">
        <div class="structure-section">
          <h4>🏗️ Database Entities</h4>
          <div class="structure-list">
            ${assumptions.entities.map(e => `<div class="structure-item">${e}</div>`).join('')}
          </div>
        </div>

        <div class="structure-section">
          <h4>👥 User Roles</h4>
          <div class="structure-list">
            ${assumptions.roles.map(r => `<div class="structure-item">${r}</div>`).join('')}
          </div>
        </div>

        <div class="structure-section">
          <h4>✨ Key Features</h4>
          <div class="structure-list">
            ${assumptions.features.slice(0, 4).map(f => `<div class="structure-item">${f}</div>`).join('')}
          </div>
        </div>

        <div class="structure-section">
          <h4>🔗 Integrations</h4>
          <div class="structure-list">
            ${assumptions.integrations.length > 0 ? assumptions.integrations.map(i => `<div class="structure-item">${i}</div>`).join('') : '<div class="structure-item">None</div>'}
          </div>
        </div>
      </div>
    `;

    this.previewContent.innerHTML = html;
  }

  async applyChanges() {
    const changes = this.modifyInput.value.trim();
    if (!changes) {
      alert('Please enter what you want to change');
      return;
    }

    this.closeModal(this.modifyModal);
    this.addMessage('user', changes);
    this.statusBadge.textContent = 'Refining...';
    this.modifyInput.value = '';

    try {
      const response = await fetch(`/api/conversation/${this.conversationId}/refine`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ changes })
      });

      if (!response.ok) throw new Error('Failed to apply changes');

      const data = await response.json();
      
      if (data.status === 'success' && data.response.type === 'assumptions') {
        // Show updated assumptions
        this.addMessage('assistant', data.response.message);
        this.showAssumptions(data.response);
        this.updatePreview(data.response.assumptions);
        this.statusBadge.textContent = 'Ready';
      } else if (data.status === 'clarification_needed') {
        this.addMessage('assistant', data.response.message);
        this.statusBadge.textContent = 'Needs Clarification';
      }
    } catch (error) {
      console.error('[Chat] Error applying changes:', error);
      this.addMessage('assistant', `Error: ${error.message}`);
      this.statusBadge.textContent = 'Error';
    }
  }

  async downloadApp() {
    if (!this.conversationId) {
      alert('No active conversation to download');
      return;
    }

    try {
      this.downloadBtn.disabled = true;
      this.downloadBtn.textContent = '📥 Downloading...';

      const response = await fetch(`/api/conversation/${this.conversationId}/generate-app`, {
        method: 'POST'
      });

      if (!response.ok) throw new Error('Failed to generate app');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `app_${this.conversationId.slice(0, 8)}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      this.addMessage('assistant', '✅ App downloaded successfully!');
      console.log('[Chat] App downloaded');
    } catch (error) {
      console.error('[Chat] Error downloading app:', error);
      alert(`Error downloading app: ${error.message}`);
    } finally {
      this.downloadBtn.disabled = false;
      this.downloadBtn.textContent = '📥 Download App';
    }
  }

  openModal(modal) {
    modal.classList.remove('hidden');
  }

  closeModal(modal) {
    modal.classList.add('hidden');
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize chat when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  console.log('[Chat] Initializing AI Application Compiler Chat...');
  window.compilerChat = new CompilerChat();
  console.log('[Chat] Application ready');
});

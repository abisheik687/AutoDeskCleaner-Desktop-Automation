// AutoDeskCleaner Frontend JavaScript
const API_BASE = 'http://localhost:5000/api';

let scannedFiles = [];
let currentConfig = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('scanBtn').addEventListener('click', scanDesktop);
    document.getElementById('cleanupBtn').addEventListener('click', executeCleanup);
    document.getElementById('configBtn').addEventListener('click', openConfig);
    document.getElementById('logsBtn').addEventListener('click', openLogs);
});

// Scan Desktop
async function scanDesktop() {
    showLoading('Scanning desktop...');
    
    try {
        const response = await fetch(`${API_BASE}/scan`);
        const data = await response.json();
        
        if (data.success) {
            scannedFiles = data.files;
            displayFiles(data.files);
            displayStats(data.categories, data.total);
            document.getElementById('cleanupBtn').disabled = data.total === 0;
            showToast('Scan complete!', 'success');
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Network error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Display Files
function displayFiles(files) {
    const fileList = document.getElementById('fileList');
    const filePreview = document.getElementById('filePreview');
    
    if (files.length === 0) {
        fileList.innerHTML = '<p class="empty-state">No files found. Your desktop is clean! 🎉</p>';
        filePreview.classList.remove('hidden');
        return;
    }
    
    // Group by category
    const grouped = {};
    files.forEach(file => {
        if (!grouped[file.category]) {
            grouped[file.category] = [];
        }
        grouped[file.category].push(file);
    });
    
    let html = '';
    for (const [category, categoryFiles] of Object.entries(grouped)) {
        html += `
            <div class="category-group">
                <h3 class="category-header ${getCategoryClass(category)}">
                    ${getCategoryIcon(category)} ${category} (${categoryFiles.length})
                </h3>
                <div class="file-items">
        `;
        
        categoryFiles.forEach(file => {
            html += `
                <div class="file-item">
                    <span class="file-icon">${getFileIcon(file.extension)}</span>
                    <span class="file-name">${file.name}</span>
                    <span class="file-ext">${file.extension}</span>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    fileList.innerHTML = html;
    filePreview.classList.remove('hidden');
}

// Display Statistics
function displayStats(categories, total) {
    const statsPanel = document.getElementById('statsPanel');
    document.getElementById('totalFiles').textContent = total;
    
    const categoryStats = document.getElementById('categoryStats');
    let html = '<div class="category-bars">';
    
    for (const [category, count] of Object.entries(categories)) {
        const percentage = (count / total * 100).toFixed(1);
        html += `
            <div class="category-bar-item">
                <div class="category-bar-label">
                    <span class="${getCategoryClass(category)}">${category}</span>
                    <span>${count} files (${percentage}%)</span>
                </div>
                <div class="category-bar-bg">
                    <div class="category-bar-fill ${getCategoryClass(category)}" 
                         style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    categoryStats.innerHTML = html;
    statsPanel.classList.remove('hidden');
}

// Execute Cleanup
async function executeCleanup() {
    if (!confirm(`Are you sure you want to organize ${scannedFiles.length} files?`)) {
        return;
    }
    
    showLoading('Organizing files...');
    
    try {
        const response = await fetch(`${API_BASE}/cleanup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ files: scannedFiles })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const summary = data.summary;
            document.getElementById('movedFiles').textContent = summary.moved;
            document.getElementById('failedFiles').textContent = summary.failed;
            
            showToast(`Cleanup complete! Moved ${summary.moved} files.`, 'success');
            
            // Clear file list
            scannedFiles = [];
            document.getElementById('fileList').innerHTML = 
                '<p class="empty-state">Cleanup complete! 🎉</p>';
            document.getElementById('cleanupBtn').disabled = true;
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Network error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Configuration
async function openConfig() {
    showLoading('Loading configuration...');
    
    try {
        const response = await fetch(`${API_BASE}/config`);
        const data = await response.json();
        
        if (data.success) {
            currentConfig = data.config;
            document.getElementById('configEditor').value = 
                JSON.stringify(data.config, null, 2);
            document.getElementById('configPanel').classList.remove('hidden');
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Network error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

function closeConfig() {
    document.getElementById('configPanel').classList.add('hidden');
}

async function saveConfig() {
    const configText = document.getElementById('configEditor').value;
    
    try {
        const config = JSON.parse(configText);
        
        showLoading('Saving configuration...');
        
        const response = await fetch(`${API_BASE}/config`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Configuration saved successfully!', 'success');
            closeConfig();
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Invalid JSON: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Logs
async function openLogs() {
    showLoading('Loading logs...');
    
    try {
        const response = await fetch(`${API_BASE}/logs`);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('logsContent').textContent = 
                data.logs || 'No logs available yet.';
            document.getElementById('logsPanel').classList.remove('hidden');
        } else {
            showToast(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Network error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

function closeLogs() {
    document.getElementById('logsPanel').classList.add('hidden');
}

// Helper Functions
function getCategoryClass(category) {
    const classes = {
        'Documents': 'cat-documents',
        'Images': 'cat-images',
        'Videos': 'cat-videos',
        'Audio': 'cat-audio',
        'Archives': 'cat-archives',
        'Code': 'cat-code',
        'Others': 'cat-others'
    };
    return classes[category] || 'cat-others';
}

function getCategoryIcon(category) {
    const icons = {
        'Documents': '📄',
        'Images': '🖼️',
        'Videos': '🎬',
        'Audio': '🎵',
        'Archives': '📦',
        'Code': '💻',
        'Others': '📁'
    };
    return icons[category] || '📁';
}

function getFileIcon(extension) {
    const ext = extension.toLowerCase();
    if (['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'].includes(ext)) return '🖼️';
    if (['.mp4', '.avi', '.mkv', '.mov'].includes(ext)) return '🎬';
    if (['.mp3', '.wav', '.flac', '.aac'].includes(ext)) return '🎵';
    if (['.pdf', '.doc', '.docx', '.txt'].includes(ext)) return '📄';
    if (['.zip', '.rar', '.7z', '.tar'].includes(ext)) return '📦';
    if (['.py', '.js', '.java', '.cpp', '.html'].includes(ext)) return '💻';
    return '📄';
}

function showLoading(text = 'Loading...') {
    document.getElementById('loadingText').textContent = text;
    document.getElementById('loadingOverlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    const container = document.getElementById('toastContainer');
    container.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

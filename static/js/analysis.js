/**
 * ModelYourData - Analysis Page JavaScript
 * Handles data visualization and analysis operations via AJAX
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const vizContent = document.getElementById('viz-content');
    const vizResult = document.getElementById('viz-result');
    const vizTitle = document.getElementById('viz-title');
    const vizInfo = document.getElementById('viz-info');
    const infoContent = document.getElementById('info-content');
    const loadingSpinner = document.getElementById('loading-spinner');
    const parametersPanel = document.getElementById('parameters-panel');
    const parametersContent = document.getElementById('parameters-content');
    const applyParamsBtn = document.getElementById('apply-params-btn');
    const exportBtn = document.getElementById('export-btn');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const visualizationBox = document.querySelector('.visualization-box');
    
    // Get file ID and column data
    const fileId = document.getElementById('file-id').value;
    const { numericColumns, categoricalColumns, allColumns } = window.fileData;
    
    // Current state
    let currentOperation = 'table';
    let currentImageData = null;
    let currentParams = {};
    
    // API endpoints
    const endpoints = {
        table: `/api/table/${fileId}/`,
        linear_regression: `/api/linear-regression/${fileId}/`,
        clustering: `/api/clustering/${fileId}/`,
        distribution: `/api/distribution/${fileId}/`,
        statistics: `/api/statistics/${fileId}/`,
        eda: `/api/eda/${fileId}/`,
        correlation: `/api/correlation/${fileId}/`,
        scatter: `/api/scatter/${fileId}/`,
        histogram: `/api/histogram/${fileId}/`,
        boxplot: `/api/boxplot/${fileId}/`,
    };
    
    // Operation titles and icons
    const operationInfo = {
        table: { title: 'Data Preview', icon: 'fa-table' },
        linear_regression: { title: 'Linear Regression', icon: 'fa-chart-line' },
        clustering: { title: 'Clustering (KMeans)', icon: 'fa-project-diagram' },
        distribution: { title: 'Distribution Plot', icon: 'fa-chart-area' },
        statistics: { title: 'Statistical Summary', icon: 'fa-calculator' },
        eda: { title: 'Exploratory Data Analysis', icon: 'fa-search-plus' },
        correlation: { title: 'Correlation Matrix', icon: 'fa-th' },
        scatter: { title: 'Scatter Plot', icon: 'fa-braille' },
        histogram: { title: 'Histogram', icon: 'fa-chart-bar' },
        boxplot: { title: 'Box Plot', icon: 'fa-box' },
    };
    
    // Parameter configurations for each operation
    const paramConfigs = {
        linear_regression: [
            { name: 'x_column', label: 'X Variable', type: 'select', options: numericColumns },
            { name: 'y_column', label: 'Y Variable', type: 'select', options: numericColumns },
        ],
        clustering: [
            { name: 'n_clusters', label: 'Number of Clusters', type: 'number', min: 2, max: 10, default: 3 },
        ],
        distribution: [
            { name: 'column', label: 'Column', type: 'select', options: numericColumns, allowEmpty: true },
        ],
        scatter: [
            { name: 'x_column', label: 'X Variable', type: 'select', options: numericColumns },
            { name: 'y_column', label: 'Y Variable', type: 'select', options: numericColumns },
        ],
        histogram: [
            { name: 'column', label: 'Column', type: 'select', options: numericColumns },
            { name: 'bins', label: 'Number of Bins', type: 'number', min: 5, max: 100, default: 30 },
        ],
    };
    
    // Initialize - load table preview
    loadOperation('table');
    
    // Operation button click handlers
    document.querySelectorAll('.btn-operation').forEach(btn => {
        btn.addEventListener('click', function() {
            const operation = this.dataset.operation;
            
            // Update active state
            document.querySelectorAll('.btn-operation').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show parameters if needed
            if (paramConfigs[operation]) {
                showParameters(operation);
            } else {
                parametersPanel.style.display = 'none';
                loadOperation(operation);
            }
            
            currentOperation = operation;
        });
    });
    
    // Apply parameters button
    applyParamsBtn.addEventListener('click', function() {
        currentParams = collectParameters();
        loadOperation(currentOperation, currentParams);
    });
    
    // Export button
    exportBtn.addEventListener('click', function() {
        if (currentImageData) {
            const filename = `${currentOperation}_${new Date().toISOString().slice(0, 10)}.png`;
            Utils.downloadImage(currentImageData, filename);
            Utils.showToast('Visualization exported successfully!', 'success');
        } else {
            Utils.showToast('No visualization to export', 'warning');
        }
    });
    
    // Fullscreen button
    fullscreenBtn.addEventListener('click', function() {
        visualizationBox.classList.toggle('fullscreen');
        const icon = this.querySelector('i');
        if (visualizationBox.classList.contains('fullscreen')) {
            icon.className = 'fas fa-compress';
        } else {
            icon.className = 'fas fa-expand';
        }
    });
    
    // ESC key to exit fullscreen
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && visualizationBox.classList.contains('fullscreen')) {
            visualizationBox.classList.remove('fullscreen');
            fullscreenBtn.querySelector('i').className = 'fas fa-expand';
        }
    });
    
    /**
     * Show parameters panel for an operation
     */
    function showParameters(operation) {
        const config = paramConfigs[operation];
        if (!config) return;
        
        let html = '';
        config.forEach(param => {
            html += `<div class="param-group">`;
            html += `<label class="param-label">${param.label}</label>`;
            
            if (param.type === 'select') {
                html += `<select class="form-select" name="${param.name}">`;
                if (param.allowEmpty) {
                    html += `<option value="">All columns</option>`;
                }
                param.options.forEach((opt, idx) => {
                    const selected = idx === 0 && !param.allowEmpty ? 'selected' : '';
                    html += `<option value="${opt}" ${selected}>${opt}</option>`;
                });
                html += `</select>`;
            } else if (param.type === 'number') {
                html += `<input type="number" class="form-input" name="${param.name}" 
                         min="${param.min}" max="${param.max}" value="${param.default || param.min}">`;
            }
            
            html += `</div>`;
        });
        
        parametersContent.innerHTML = html;
        parametersPanel.style.display = 'block';
    }
    
    /**
     * Collect parameters from the form
     */
    function collectParameters() {
        const params = {};
        parametersContent.querySelectorAll('select, input').forEach(el => {
            if (el.value) {
                params[el.name] = el.value;
            }
        });
        return params;
    }
    
    /**
     * Load and display an operation result
     */
    async function loadOperation(operation, params = {}) {
        showLoading();
        hideInfo();
        currentImageData = null;
        
        try {
            // Build URL with query params
            let url = endpoints[operation];
            const queryParams = new URLSearchParams(params).toString();
            if (queryParams) {
                url += '?' + queryParams;
            }
            
            const response = await Utils.fetchAPI(url);
            
            if (response.success) {
                displayResult(operation, response.data);
                updateTitle(operation);
            } else {
                showError(response.error || 'An error occurred');
            }
        } catch (error) {
            showError(error.message || 'Failed to load data');
        }
    }
    
    /**
     * Display the result based on operation type
     */
    function displayResult(operation, data) {
        hideLoading();
        
        switch (operation) {
            case 'table':
                displayTable(data);
                break;
            case 'statistics':
                displayStatistics(data);
                break;
            case 'eda':
                displayEDA(data);
                break;
            default:
                displayImage(data);
        }
    }
    
    /**
     * Display table preview
     */
    function displayTable(data) {
        let html = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">${data.rows.toLocaleString()}</div>
                    <div class="stat-label">Total Rows</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.columns}</div>
                    <div class="stat-label">Columns</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.numeric_columns.length}</div>
                    <div class="stat-label">Numeric</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.categorical_columns.length}</div>
                    <div class="stat-label">Categorical</div>
                </div>
            </div>
            <div class="table-wrapper">
                ${data.html}
            </div>
        `;
        vizResult.innerHTML = html;
    }
    
    /**
     * Display statistical summary
     */
    function displayStatistics(data) {
        let html = `
            <div class="eda-report">
                <div class="eda-section">
                    <h3 class="eda-section-title">
                        <i class="fas fa-info-circle"></i>
                        Dataset Overview
                    </h3>
                    <div class="stats-grid">
        `;
        
        for (const [key, value] of Object.entries(data.basic_stats)) {
            html += `
                <div class="stat-card">
                    <div class="stat-value">${typeof value === 'number' ? value.toLocaleString() : value}</div>
                    <div class="stat-label">${key}</div>
                </div>
            `;
        }
        
        html += `
                    </div>
                </div>
                <div class="eda-section">
                    <h3 class="eda-section-title">
                        <i class="fas fa-calculator"></i>
                        Descriptive Statistics
                    </h3>
                    <div class="table-wrapper">
                        ${data.summary_html}
                    </div>
                </div>
                <div class="eda-section">
                    <h3 class="eda-section-title">
                        <i class="fas fa-exclamation-triangle"></i>
                        Missing Values
                    </h3>
                    <div class="table-wrapper">
                        ${data.missing_html}
                    </div>
                </div>
            </div>
        `;
        
        vizResult.innerHTML = html;
    }
    
    /**
     * Display EDA report with multiple visualizations
     */
    function displayEDA(data) {
        let html = '<div class="eda-report">';
        
        // Statistics section
        html += `
            <div class="eda-section">
                <h3 class="eda-section-title">
                    <i class="fas fa-info-circle"></i>
                    Dataset Overview
                </h3>
                <div class="stats-grid">
        `;
        
        for (const [key, value] of Object.entries(data.summary.basic_stats)) {
            html += `
                <div class="stat-card">
                    <div class="stat-value">${typeof value === 'number' ? value.toLocaleString() : value}</div>
                    <div class="stat-label">${key}</div>
                </div>
            `;
        }
        
        html += '</div></div>';
        
        // Images
        data.images.forEach(img => {
            const titles = {
                correlation: 'Correlation Matrix',
                missing: 'Missing Values Analysis',
                boxplots: 'Box Plots',
                pairplot: 'Pair Plot',
            };
            
            html += `
                <div class="eda-section">
                    <h3 class="eda-section-title">
                        <i class="fas fa-chart-bar"></i>
                        ${titles[img.type] || img.type}
                    </h3>
                    <img src="data:image/png;base64,${img.image}" alt="${img.type}" 
                         onclick="Utils.downloadImage('${img.image}', '${img.type}.png')" 
                         style="cursor: pointer;" title="Click to download">
                </div>
            `;
        });
        
        // Descriptive stats table
        html += `
            <div class="eda-section">
                <h3 class="eda-section-title">
                    <i class="fas fa-calculator"></i>
                    Descriptive Statistics
                </h3>
                <div class="table-wrapper">
                    ${data.summary.summary_html}
                </div>
            </div>
        </div>`;
        
        vizResult.innerHTML = html;
        
        // Store first image for export
        if (data.images.length > 0) {
            currentImageData = data.images[0].image;
        }
    }
    
    /**
     * Display image-based visualization
     */
    function displayImage(data) {
        if (data.image) {
            vizResult.innerHTML = `
                <img src="data:image/png;base64,${data.image}" 
                     alt="Visualization" 
                     id="current-viz-image">
            `;
            currentImageData = data.image;
            
            // Show additional info if available
            showResultInfo(data);
        }
    }
    
    /**
     * Show result info panel
     */
    function showResultInfo(data) {
        let infoItems = [];
        
        if (data.r2_score !== undefined) {
            infoItems.push({ label: 'R² Score', value: data.r2_score });
        }
        if (data.equation) {
            infoItems.push({ label: 'Equation', value: data.equation });
        }
        if (data.coefficient !== undefined) {
            infoItems.push({ label: 'Coefficient', value: data.coefficient });
        }
        if (data.intercept !== undefined) {
            infoItems.push({ label: 'Intercept', value: data.intercept });
        }
        if (data.n_clusters !== undefined) {
            infoItems.push({ label: 'Clusters', value: data.n_clusters });
        }
        if (data.inertia !== undefined) {
            infoItems.push({ label: 'Inertia', value: data.inertia });
        }
        if (data.mean !== undefined) {
            infoItems.push({ label: 'Mean', value: data.mean });
        }
        if (data.median !== undefined) {
            infoItems.push({ label: 'Median', value: data.median });
        }
        if (data.std !== undefined) {
            infoItems.push({ label: 'Std Dev', value: data.std });
        }
        
        if (infoItems.length > 0) {
            let html = '';
            infoItems.forEach(item => {
                html += `
                    <div class="info-item">
                        <span class="info-label">${item.label}</span>
                        <span class="info-value">${item.value}</span>
                    </div>
                `;
            });
            infoContent.innerHTML = html;
            vizInfo.style.display = 'block';
        }
    }
    
    /**
     * Update visualization title
     */
    function updateTitle(operation) {
        const info = operationInfo[operation];
        if (info) {
            vizTitle.innerHTML = `
                <i class="fas ${info.icon}"></i>
                ${info.title}
            `;
        }
    }
    
    /**
     * Show loading spinner
     */
    function showLoading() {
        loadingSpinner.style.display = 'flex';
        vizResult.innerHTML = '';
    }
    
    /**
     * Hide loading spinner
     */
    function hideLoading() {
        loadingSpinner.style.display = 'none';
    }
    
    /**
     * Hide info panel
     */
    function hideInfo() {
        vizInfo.style.display = 'none';
    }
    
    /**
     * Show error message
     */
    function showError(message) {
        hideLoading();
        vizResult.innerHTML = `
            <div class="error-message" style="display: flex; justify-content: center; margin-top: 2rem;">
                <i class="fas fa-exclamation-circle"></i>
                <span>${message}</span>
            </div>
        `;
        Utils.showToast(message, 'error');
    }
});

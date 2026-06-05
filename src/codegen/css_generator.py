import logging

logger = logging.getLogger(__name__)


class CSSGenerator:
    """
    Generates production-ready CSS for generated applications.
    Provides responsive design, component styling, and utility classes.
    """

    @staticmethod
    def generate() -> str:
        """Generate main stylesheet"""
        return """/* Generated Application Stylesheet */
/* This file is auto-generated. Modify with caution. */

:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    --success-color: #16a34a;
    --danger-color: #dc2626;
    --warning-color: #ea580c;
    --info-color: #0284c7;
    --light-bg: #f8fafc;
    --border-color: #e2e8f0;
    --text-color: #1e293b;
    --text-light: #64748b;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--light-bg);
}

/* Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header, .page-header {
    background: white;
    padding: 20px 0;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 30px;
}

header h1, .page-header h1 {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 5px;
}

.subtitle {
    color: var(--text-light);
    font-size: 14px;
}

main, .page-content {
    min-height: 400px;
}

footer, .page-footer {
    text-align: center;
    padding: 20px;
    color: var(--text-light);
    font-size: 12px;
    margin-top: 40px;
    border-top: 1px solid var(--border-color);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--text-color);
}

h1 { font-size: 28px; }
h2 { font-size: 24px; }
h3 { font-size: 20px; }
h4 { font-size: 18px; }
h5 { font-size: 16px; }
h6 { font-size: 14px; }

p {
    margin-bottom: 15px;
}

a {
    color: var(--primary-color);
    text-decoration: none;
    transition: var(--transition);
}

a:hover {
    color: #1d4ed8;
    text-decoration: underline;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
    text-align: center;
    text-decoration: none;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: #1d4ed8;
}

.btn-secondary {
    background-color: var(--secondary-color);
    color: white;
}

.btn-secondary:hover {
    background-color: #475569;
}

.btn-danger {
    background-color: var(--danger-color);
    color: white;
}

.btn-danger:hover {
    background-color: #b91c1c;
}

.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Forms */
form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

label {
    font-weight: 500;
    margin-bottom: 5px;
    color: var(--text-color);
}

input[type="text"],
input[type="email"],
input[type="password"],
input[type="number"],
input[type="date"],
input[type="datetime-local"],
textarea,
select {
    padding: 10px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 14px;
    font-family: inherit;
    transition: var(--transition);
}

input:focus,
textarea:focus,
select:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

input[type="checkbox"],
input[type="radio"] {
    margin-right: 5px;
}

small {
    display: block;
    color: var(--text-light);
    font-size: 12px;
    margin-top: 3px;
}

.form-actions {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

.form-message {
    padding: 12px 15px;
    border-radius: 4px;
    font-size: 14px;
    margin-top: 10px;
    display: none;
}

.form-message:not(:empty) {
    display: block;
}

.form-message.success {
    background-color: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
}

.form-message.error {
    background-color: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;
}

.form-message.info {
    background-color: #dbeafe;
    color: #0c4a6e;
    border: 1px solid #93c5fd;
}

/* Tables */
.data-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

.data-table thead {
    background-color: var(--light-bg);
    border-bottom: 2px solid var(--border-color);
}

.data-table th {
    padding: 12px 15px;
    text-align: left;
    font-weight: 600;
    color: var(--text-color);
}

.data-table td {
    padding: 12px 15px;
    border-bottom: 1px solid var(--border-color);
}

.data-table tbody tr:hover {
    background-color: var(--light-bg);
}

.data-table tbody tr:last-child td {
    border-bottom: none;
}

.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.table-container {
    overflow-x: auto;
    margin-bottom: 20px;
}

/* Statistics Cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 4px;
    box-shadow: var(--shadow);
    text-align: center;
}

.stat-card h3 {
    color: var(--text-light);
    font-size: 12px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.stat-value {
    font-size: 28px;
    font-weight: 600;
    color: var(--primary-color);
}

/* Components */
.component {
    background: white;
    padding: 20px;
    border-radius: 4px;
    box-shadow: var(--shadow);
    margin-bottom: 20px;
}

.component h2 {
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border-color);
}

.component-header {
    text-align: center;
    padding: 40px 20px;
}

.component-header h1 {
    font-size: 32px;
    margin-bottom: 10px;
}

.component-header .description {
    color: var(--text-light);
    font-size: 16px;
}

.component-nav {
    background: white;
    margin: 0 -20px;
    padding: 0;
}

.nav-menu {
    list-style: none;
    display: flex;
    gap: 0;
}

.nav-menu li {
    margin: 0;
}

.nav-menu a {
    display: block;
    padding: 15px 20px;
    color: var(--text-color);
    border-bottom: 2px solid transparent;
    transition: var(--transition);
}

.nav-menu a:hover {
    background-color: var(--light-bg);
    border-bottom-color: var(--primary-color);
}

.component-chart {
    min-height: 450px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }

    header, .page-header {
        padding: 15px 0;
        margin-bottom: 20px;
    }

    h1 { font-size: 24px; }
    h2 { font-size: 20px; }
    h3 { font-size: 18px; }

    .stats-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
    }

    .stat-value {
        font-size: 24px;
    }

    .table-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .data-table {
        font-size: 14px;
    }

    .data-table th,
    .data-table td {
        padding: 10px;
    }

    .form-actions {
        flex-direction: column;
    }

    .btn {
        width: 100%;
    }

    .nav-menu {
        flex-direction: column;
    }

    .nav-menu a {
        border-bottom: 1px solid var(--border-color);
    }
}

@media (max-width: 480px) {
    body {
        font-size: 14px;
    }

    .container {
        padding: 10px;
    }

    h1 { font-size: 20px; }
    h2 { font-size: 18px; }
    h3 { font-size: 16px; }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .component {
        padding: 15px;
    }
}

/* Utility Classes */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-left { text-align: left; }

.mt-10 { margin-top: 10px; }
.mt-20 { margin-top: 20px; }
.mb-10 { margin-bottom: 10px; }
.mb-20 { margin-bottom: 20px; }
.p-10 { padding: 10px; }
.p-20 { padding: 20px; }

.hidden { display: none; }
.visible { display: block; }

.text-muted { color: var(--text-light); }
.text-danger { color: var(--danger-color); }
.text-success { color: var(--success-color); }
"""

    logger.info("[CSSGen] Generated stylesheet")

// Améliorations JavaScript pour l'interface d'administration Django

document.addEventListener('DOMContentLoaded', function() {
    
    // Amélioration des tableaux
    enhanceTables();
    
    // Amélioration des formulaires
    enhanceForms();
    
    // Amélioration des messages
    enhanceMessages();
    
    // Amélioration de la navigation
    enhanceNavigation();
    
    // Ajout d'animations
    addAnimations();
    
    // Amélioration de l'accessibilité
    enhanceAccessibility();
});

function enhanceTables() {
    // Ajouter des effets de survol améliorés aux tableaux
    const tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row, index) {
            // Ajouter un délai pour l'animation
            row.style.animationDelay = (index * 0.05) + 's';
            
            // Améliorer l'effet de survol
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.01)';
                this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.15)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
            });
        });
    });
}

function enhanceForms() {
    // Améliorer les champs de formulaire
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(function(input) {
        // Ajouter des effets de focus améliorés
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
            this.parentElement.style.boxShadow = '0 4px 15px rgba(52, 152, 219, 0.2)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
            this.parentElement.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        });
        
        // Ajouter une validation visuelle en temps réel
        if (input.type === 'email') {
            input.addEventListener('input', function() {
                const email = this.value;
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (email && !emailRegex.test(email)) {
                    this.style.borderColor = '#e74c3c';
                    this.style.boxShadow = '0 0 0 3px rgba(231, 76, 60, 0.1)';
                } else {
                    this.style.borderColor = '#27ae60';
                    this.style.boxShadow = '0 0 0 3px rgba(39, 174, 96, 0.1)';
                }
            });
        }
    });
}

function enhanceMessages() {
    // Améliorer l'affichage des messages
    const messages = document.querySelectorAll('.messagelist li');
    messages.forEach(function(message, index) {
        // Ajouter un délai pour l'animation
        message.style.animationDelay = (index * 0.2) + 's';
        
        // Ajouter un bouton de fermeture
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '×';
        closeButton.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: inherit;
            opacity: 0.7;
        `;
        
        closeButton.addEventListener('click', function() {
            message.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                message.remove();
            }, 300);
        });
        
        message.style.position = 'relative';
        message.appendChild(closeButton);
    });
}

function enhanceNavigation() {
    // Améliorer la navigation
    const breadcrumbs = document.querySelector('.breadcrumbs');
    if (breadcrumbs) {
        breadcrumbs.style.animation = 'slideInFromTop 0.5s ease-out';
    }
    
    // Améliorer les liens de navigation
    const navLinks = document.querySelectorAll('a');
    navLinks.forEach(function(link) {
        if (link.href && !link.href.includes('#')) {
            link.addEventListener('click', function(e) {
                // Ajouter un effet de chargement
                if (!this.classList.contains('button')) {
                    this.style.opacity = '0.7';
                    this.style.transform = 'scale(0.95)';
                    
                    setTimeout(() => {
                        this.style.opacity = '1';
                        this.style.transform = 'scale(1)';
                    }, 150);
                }
            });
        }
    });
}

function addAnimations() {
    // Ajouter des animations CSS personnalisées
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInFromTop {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideOut {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        .slide-in {
            animation: slideInFromTop 0.5s ease-out;
        }
        
        .pulse {
            animation: pulse 0.5s ease-in-out;
        }
        
        .shake {
            animation: shake 0.5s ease-in-out;
        }
    `;
    document.head.appendChild(style);
    
    // Ajouter des classes d'animation aux éléments
    const modules = document.querySelectorAll('.module, .inline-group');
    modules.forEach(function(module, index) {
        module.classList.add('fade-in');
        module.style.animationDelay = (index * 0.1) + 's';
    });
}

function enhanceAccessibility() {
    // Améliorer l'accessibilité
    const buttons = document.querySelectorAll('button, .button, input[type="submit"], input[type="button"]');
    buttons.forEach(function(button) {
        // Ajouter des attributs ARIA si manquants
        if (!button.getAttribute('aria-label') && button.textContent.trim()) {
            button.setAttribute('aria-label', button.textContent.trim());
        }
        
        // Améliorer la navigation au clavier
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Ajouter des raccourcis clavier
    document.addEventListener('keydown', function(e) {
        // Ctrl+S pour sauvegarder
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            const saveButton = document.querySelector('input[type="submit"][value*="Save"], input[type="submit"][value*="Sauvegarder"]');
            if (saveButton) {
                saveButton.click();
            }
        }
        
        // Échap pour fermer les messages
        if (e.key === 'Escape') {
            const messages = document.querySelectorAll('.messagelist li');
            messages.forEach(function(message) {
                message.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
    });
}

// Fonction pour afficher des notifications toast
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideInFromRight 0.3s ease-out;
        border-left: 4px solid;
    `;
    
    // Couleurs selon le type
    const colors = {
        success: '#27ae60',
        error: '#e74c3c',
        warning: '#f39c12',
        info: '#3498db'
    };
    
    toast.style.borderLeftColor = colors[type] || colors.info;
    
    document.body.appendChild(toast);
    
    // Auto-suppression après 3 secondes
    setTimeout(() => {
        toast.style.animation = 'slideOutToRight 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Ajouter l'animation pour les toasts
const toastStyle = document.createElement('style');
toastStyle.textContent = `
    @keyframes slideInFromRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutToRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(toastStyle);

// Exposer la fonction showToast globalement
window.showToast = showToast; 
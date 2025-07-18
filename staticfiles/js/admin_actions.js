// Script pour améliorer l'interaction avec les boutons d'action dans l'admin Django

document.addEventListener('DOMContentLoaded', function() {
    // Améliorer l'apparence des boutons d'action
    const actionButtons = document.querySelectorAll('.actions_buttons .button, .export_print_buttons .button');
    
    actionButtons.forEach(function(button) {
        // Ajouter des effets de survol
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        
        // Améliorer la confirmation de suppression
        if (button.classList.contains('btn-danger')) {
            button.addEventListener('click', function(e) {
                const confirmed = confirm('Êtes-vous vraiment sûr de vouloir supprimer cet élément ? Cette action est irréversible.');
                if (!confirmed) {
                    e.preventDefault();
                }
            });
        }
        
        // Ajouter des confirmations pour les actions d'export et d'impression
        if (button.classList.contains('btn-success')) {
            button.addEventListener('click', function(e) {
                const confirmed = confirm('Voulez-vous exporter cet élément en format CSV ?');
                if (!confirmed) {
                    e.preventDefault();
                }
            });
        }
        
        if (button.classList.contains('btn-info')) {
            button.addEventListener('click', function(e) {
                const confirmed = confirm('Voulez-vous imprimer cet élément ?');
                if (!confirmed) {
                    e.preventDefault();
                }
            });
        }
    });
    
    // Ajouter des tooltips pour les boutons
    actionButtons.forEach(function(button) {
        const title = button.getAttribute('title');
        if (title) {
            button.setAttribute('data-toggle', 'tooltip');
            button.setAttribute('data-placement', 'top');
        }
    });
    
    // Améliorer l'affichage sur mobile
    function adjustButtonsForMobile() {
        const isMobile = window.innerWidth <= 768;
        const actionColumns = document.querySelectorAll('.actions_buttons, .export_print_buttons');
        
        actionColumns.forEach(function(column) {
            if (isMobile) {
                column.style.textAlign = 'center';
            } else {
                column.style.textAlign = 'left';
            }
        });
    }
    
    // Appeler la fonction au chargement et lors du redimensionnement
    adjustButtonsForMobile();
    window.addEventListener('resize', adjustButtonsForMobile);
    
    // Ajouter des animations pour les boutons d'export et d'impression
    const exportPrintButtons = document.querySelectorAll('.export_print_buttons .button');
    exportPrintButtons.forEach(function(button) {
        // Animation spéciale pour les boutons d'export
        if (button.classList.contains('btn-success')) {
            button.addEventListener('click', function() {
                this.style.animation = 'pulse 0.5s';
                setTimeout(() => {
                    this.style.animation = '';
                }, 500);
            });
        }
        
        // Animation spéciale pour les boutons d'impression
        if (button.classList.contains('btn-info')) {
            button.addEventListener('click', function() {
                this.style.animation = 'shake 0.5s';
                setTimeout(() => {
                    this.style.animation = '';
                }, 500);
            });
        }
    });
});

// Ajouter des styles CSS pour les animations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-2px); }
        75% { transform: translateX(2px); }
    }
`;
document.head.appendChild(style); 
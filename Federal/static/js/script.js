/**
 * Loteria Federal - JavaScript Utilities
 */

// Formata número para moeda brasileira
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

// Formata data brasileira
function formatarData(dataStr) {
    if (!dataStr) return 'Data não disponível';
    
    // Se já está no formato dd/mm/yyyy
    if (dataStr.includes('/')) {
        return dataStr;
    }
    
    // Se está no formato yyyy-mm-dd
    const partes = dataStr.split('-');
    if (partes.length === 3) {
        return `${partes[2]}/${partes[1]}/${partes[0]}`;
    }
    
    return dataStr;
}

// Valida número da Federal (6 dígitos)
function validarNumeroFederal(numero) {
    const numStr = String(numero).replace(/\D/g, '');
    return numStr.length === 6;
}

// Formata número da Federal com zeros à esquerda
function formatarNumeroFederal(numero) {
    return String(numero).padStart(6, '0');
}

// Mostra toast de notificação
function mostrarNotificacao(mensagem, tipo = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Remove após 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Copia texto para clipboard
function copiarParaClipboard(texto) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(texto)
            .then(() => mostrarNotificacao('Copiado para a área de transferência!', 'success'))
            .catch(() => mostrarNotificacao('Erro ao copiar', 'danger'));
    } else {
        // Fallback para navegadores antigos
        const textArea = document.createElement('textarea');
        textArea.value = texto;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            mostrarNotificacao('Copiado!', 'success');
        } catch (err) {
            mostrarNotificacao('Erro ao copiar', 'danger');
        }
        document.body.removeChild(textArea);
    }
}

// Adiciona botão de copiar aos números
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona evento de clique aos números da Federal
    document.querySelectorAll('.numero-federal').forEach(elemento => {
        elemento.style.cursor = 'pointer';
        elemento.title = 'Clique para copiar';
        
        elemento.addEventListener('click', function() {
            const numero = this.textContent.trim();
            copiarParaClipboard(numero);
        });
    });
});

// Valida formulários
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    
    return true;
}

// Debounce para otimizar eventos
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Log de erros
window.addEventListener('error', function(e) {
    console.error('Erro capturado:', e.error);
});

// Previne múltiplos submits
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                setTimeout(() => {
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });
});

console.log('✅ Loteria Federal - JavaScript carregado com sucesso!');

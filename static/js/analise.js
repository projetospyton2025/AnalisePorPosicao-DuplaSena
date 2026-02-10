// Script para página de análise

// Função para mostrar notificação
function showNotification(message, type = 'danger') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const tipoBusca = document.getElementById('tipo-busca');
    const opcaoUltimos = document.getElementById('opcao-ultimos');
    const opcaoIntervalo = document.getElementById('opcao-intervalo');
    const formAnalise = document.getElementById('form-analise');
    const loading = document.getElementById('loading');
    const resultado = document.getElementById('resultado');
    
    // Alternar entre tipos de busca
    tipoBusca.addEventListener('change', function() {
        if (this.value === 'ultimos') {
            opcaoUltimos.style.display = 'block';
            opcaoIntervalo.style.display = 'none';
        } else {
            opcaoUltimos.style.display = 'none';
            opcaoIntervalo.style.display = 'block';
        }
    });
    
    // Submeter formulário
    formAnalise.addEventListener('submit', function(e) {
        e.preventDefault();
        realizarAnalise();
    });
    
    function realizarAnalise() {
        const tipo = tipoBusca.value;
        let dados = {};
        
        if (tipo === 'ultimos') {
            dados.quantidade = document.getElementById('quantidade').value;
        } else {
            dados.inicio = document.getElementById('inicio').value;
            dados.fim = document.getElementById('fim').value;
        }
        
        // Mostrar loading
        loading.style.display = 'block';
        resultado.style.display = 'none';
        
        // Fazer requisição
        fetch('/api/analisar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            
            if (data.erro) {
                showNotification('Erro: ' + data.erro, 'danger');
                return;
            }
            
            exibirResultado(data);
        })
        .catch(error => {
            loading.style.display = 'none';
            console.error('Erro:', error);
            showNotification('Erro ao realizar análise. Tente novamente.', 'danger');
        });
    }
    
    function exibirResultado(data) {
        // Mostrar total de concursos
        document.getElementById('total-concursos').textContent = 
            `Total de ${data.total_concursos} concursos analisados`;
        
        // Exibir análise do sorteio 1
        exibirAnaliseSorteio(data.sorteio_1, 'analise-sorteio1');
        exibirSugestoes(data.sugestoes_sorteio1, 'sugestoes-sorteio1');
        
        // Exibir análise do sorteio 2
        exibirAnaliseSorteio(data.sorteio_2, 'analise-sorteio2');
        exibirSugestoes(data.sugestoes_sorteio2, 'sugestoes-sorteio2');
        
        // Mostrar resultado
        resultado.style.display = 'block';
        resultado.scrollIntoView({ behavior: 'smooth' });
    }
    
    function exibirAnaliseSorteio(analise, elementId) {
        let html = '';
        
        for (let pos = 0; pos < 6; pos++) {
            const stat = analise[pos];
            if (!stat) continue;
            
            html += `
                <div class="card mb-3">
                    <div class="card-header posicao-header">
                        <h5 class="mb-0">Posição ${stat.posicao}</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="stat-item">
                                    <span class="stat-label">Média:</span>
                                    <span class="stat-value">${stat.media}</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-label">Mediana:</span>
                                    <span class="stat-value">${stat.mediana}</span>
                                </div>
                                ${stat.moda ? `
                                <div class="stat-item">
                                    <span class="stat-label">Moda:</span>
                                    <span class="stat-value">${stat.moda}</span>
                                </div>
                                ` : ''}
                                <div class="stat-item">
                                    <span class="stat-label">Desvio Padrão:</span>
                                    <span class="stat-value">${stat.desvio_padrao}</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-label">Intervalo:</span>
                                    <span class="stat-value">[${stat.minimo} - ${stat.maximo}]</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-label">Números Únicos:</span>
                                    <span class="stat-value">${stat.numeros_unicos}</span>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <h6 class="mb-3">10 Números Mais Frequentes:</h6>
                                <ul class="frequencia-list">
                                    ${stat.mais_frequentes.map(([num, freq]) => {
                                        const percentual = ((freq / stat.total_ocorrencias) * 100).toFixed(1);
                                        return `
                                            <li class="frequencia-item">
                                                <span class="frequencia-numero">${num}</span>
                                                <span class="frequencia-count">${freq}x (${percentual}%)</span>
                                            </li>
                                        `;
                                    }).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        document.getElementById(elementId).innerHTML = html;
    }
    
    function exibirSugestoes(sugestoes, elementId) {
        let html = '<div class="row">';
        
        for (let pos = 1; pos <= 6; pos++) {
            const numeros = sugestoes[pos] || [];
            
            html += `
                <div class="col-md-6 mb-3">
                    <div class="sugestao-posicao">
                        <h6 class="mb-0">Posição ${pos}</h6>
                        <div class="sugestao-numeros">
                            ${numeros.map(num => 
                                `<span class="sugestao-numero">${num}</span>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            `;
        }
        
        html += '</div>';
        document.getElementById(elementId).innerHTML = html;
    }
});

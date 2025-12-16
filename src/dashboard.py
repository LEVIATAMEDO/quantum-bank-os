"""
🏦 QuantumBank OS - Dashboard Interativo
Dashboard profissional para demonstração a clientes fintech
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="QuantumBank OS",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🏦 QuantumBank OS</h1>', unsafe_allow_html=True)
st.markdown("### Sistema de Trading Quântico para Fintechs")
st.markdown("---")

# Sidebar - Configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seleção de ativo
    asset_options = {
        "BTC-USD": "Bitcoin/USD",
        "ETH-USD": "Ethereum/USD", 
        "PETR4.SA": "Petrobras (B3)",
        "ITUB4.SA": "Itaú (B3)",
        "BOVA11.SA": "ETF Ibovespa"
    }
    
    selected_asset = st.selectbox(
        "Selecione o Ativo:",
        list(asset_options.keys()),
        format_func=lambda x: asset_options[x]
    )
    
    # Capital inicial
    initial_capital = st.number_input(
        "Capital Inicial (R$):",
        min_value=1000,
        max_value=1000000,
        value=50000,
        step=5000
    )
    
    # Tolerância a risco
    risk_tolerance = st.select_slider(
        "Tolerância a Risco:",
        options=["Muito Baixa", "Baixa", "Moderada", "Alta", "Muito Alta"],
        value="Moderada"
    )
    
    # Período de análise
    period = st.selectbox(
        "Período de Análise:",
        ["7 dias", "30 dias", "90 dias", "1 ano"],
        index=2
    )
    
    # Botão de análise
    analyze_clicked = st.button(
        "🔮 Executar Análise Quântica",
        type="primary",
        use_container_width=True
    )
    
    st.markdown("---")
    st.info("""
    **Demo Gratuita**
    
    Sistema completo disponível para:
    - ✅ Fintechs
    - ✅ Bancos digitais  
    - ✅ Gestoras de recursos
    
    **Contato:**
    [seu-email@quantumbank.com](mailto:seu-email@quantumbank.com)
    """)

# Dados simulados (ou reais se yfinance funcionar)
@st.cache_data
def get_market_data(asset, period="90d"):
    """Obtém dados de mercado"""
    try:
        # Tenta dados reais
        import yfinance as yf
        ticker = yf.Ticker(asset)
        data = ticker.history(period=period)
        
        if len(data) > 0:
            return data
    except:
        pass
    
    # Dados simulados para demonstração
    dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
    base_price = 100
    
    # Gera série com tendência + ruído + ciclos
    trend = np.linspace(0, 0.5, 90)
    noise = np.random.normal(0, 0.02, 90)
    cycles = 0.1 * np.sin(np.linspace(0, 8*np.pi, 90))
    
    prices = base_price * np.exp(np.cumsum(trend + noise + cycles))
    
    data = pd.DataFrame({
        'Open': prices * 0.99,
        'High': prices * 1.02,
        'Low': prices * 0.98,
        'Close': prices,
        'Volume': np.random.lognormal(10, 1, 90) * 1000
    }, index=dates)
    
    return data

# Classe de análise quântica (simplificada para demo)
class QuantumAnalyzer:
    def __init__(self):
        self.name = "QuantumBank Analyzer v1.0"
    
    def analyze(self, price_data):
        """Análise quântica simplificada"""
        returns = np.diff(np.log(price_data))
        
        # Métricas básicas
        volatility = np.std(returns) * np.sqrt(252)
        sharpe_ratio = (np.mean(returns) * 252) / (volatility + 1e-10)
        
        # Análise de tendência (Hurst simplificado)
        lags = range(2, 50)
        tau = [np.std(np.subtract(price_data[lag:], price_data[:-lag])) for lag in lags]
        hurst = np.polyfit(np.log(lags), np.log(tau), 1)[0] * 2
        
        # Sinal de trading
        short_ma = np.mean(price_data[-20:])
        long_ma = np.mean(price_data[-50:])
        
        if short_ma > long_ma and hurst > 0.55:
            signal = "📈 COMPRAR"
            confidence = min(0.95, hurst * 0.8)
        elif short_ma < long_ma and hurst > 0.55:
            signal = "📉 VENDER"
            confidence = min(0.95, hurst * 0.8)
        else:
            signal = "⏸️ MANTER"
            confidence = 0.5
        
        return {
            "signal": signal,
            "confidence": confidence,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "hurst_exponent": hurst,
            "market_type": "Tendência" if hurst > 0.6 else "Reversão" if hurst < 0.4 else "Aleatório",
            "short_ma": short_ma,
            "long_ma": long_ma
        }
    
    def monte_carlo_simulation(self, initial_price, days=30):
        """Simulação Monte Carlo"""
        simulations = 1000
        drift = 0.0003
        volatility = 0.015
        
        final_prices = []
        for _ in range(simulations):
            prices = [initial_price]
            for _ in range(days):
                shock = drift + volatility * np.random.randn()
                prices.append(prices[-1] * np.exp(shock))
            final_prices.append(prices[-1])
        
        return {
            "expected_price": np.mean(final_prices),
            "confidence_95": (np.percentile(final_prices, 2.5), np.percentile(final_prices, 97.5)),
            "probability_profit": np.mean(np.array(final_prices) > initial_price),
            "var_95": np.percentile(initial_price - np.array(final_prices), 95)
        }

# Inicializa analisador
analyzer = QuantumAnalyzer()

# Obtém dados
data = get_market_data(selected_asset, period.replace(" dias", "d").replace("1 ano", "1y"))
latest_price = data['Close'].iloc[-1]

# Executa análise se botão clicado ou na primeira execução
if analyze_clicked or 'analysis' not in st.session_state:
    analysis = analyzer.analyze(data['Close'].values)
    simulation = analyzer.monte_carlo_simulation(latest_price)
    st.session_state.analysis = analysis
    st.session_state.simulation = simulation
else:
    analysis = st.session_state.analysis
    simulation = st.session_state.simulation

# Layout principal - Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Preço Atual", f"R$ {latest_price:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Sinal", analysis["signal"], delta=f"{analysis['confidence']*100:.1f}% conf")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Volatilidade Anual", f"{analysis['volatility']*100:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    prob_profit = simulation['probability_profit'] * 100
    st.metric("Prob. Lucro (30d)", f"{prob_profit:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# Gráfico de preços
st.subheader("📊 Análise de Preços")

fig = go.Figure()

# Linha de preço
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['Close'],
    mode='lines',
    name='Preço',
    line=dict(color='#1E88E5', width=2)
))

# Médias móveis
fig.add_trace(go.Scatter(
    x=data.index[-50:],
    y=[analysis['short_ma']] * 50 if len(data) >= 50 else [],
    mode='lines',
    name='MA 20',
    line=dict(color='#FF9800', width=1, dash='dash')
))

fig.add_trace(go.Scatter(
    x=data.index[-50:],
    y=[analysis['long_ma']] * 50 if len(data) >= 50 else [],
    mode='lines',
    name='MA 50',
    line=dict(color='#4CAF50', width=1, dash='dash')
))

fig.update_layout(
    title=f"Evolução do Preço - {asset_options[selected_asset]}",
    xaxis_title="Data",
    yaxis_title="Preço (R$)",
    template="plotly_dark",
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Colunas para relatórios
col_left, col_right = st.columns(2)

with col_left:
    with st.expander("🔍 Análise Quântica Detalhada", expanded=True):
        st.write(f"**Exponente de Hurst:** {analysis['hurst_exponent']:.3f}")
        st.write(f"**Tipo de Mercado:** {analysis['market_type']}")
        st.write(f"**Índice de Sharpe:** {analysis['sharpe_ratio']:.3f}")
        st.write(f"**Confiança do Sinal:** {analysis['confidence']*100:.1f}%")
        
        # Barra de confiança
        st.progress(analysis['confidence'])

with col_right:
    with st.expander("🎯 Projeção Quântica (30 dias)", expanded=True):
        st.write(f"**Preço Esperado:** R$ {simulation['expected_price']:.2f}")
        st.write(f"**Intervalo 95%:** R$ {simulation['confidence_95'][0]:.2f} - R$ {simulation['confidence_95'][1]:.2f}")
        st.write(f"**Value at Risk (95%):** R$ {simulation['var_95']:.2f}")
        
        # Gráfico de distribuição
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=np.random.normal(simulation['expected_price'], 
                              (simulation['confidence_95'][1] - simulation['confidence_95'][0])/4, 
                              1000),
            nbinsx=30,
            name="Distribuição",
            marker_color='#667eea'
        ))
        
        fig_dist.update_layout(
            title="Distribuição de Retornos Esperados",
            xaxis_title="Preço Futuro (R$)",
            yaxis_title="Frequência",
            template="plotly_dark",
            height=300
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)

# Seção de simulação de portfólio
st.subheader("💰 Simulação de Portfólio")

col_sim1, col_sim2, col_sim3 = st.columns(3)

with col_sim1:
    expected_return = st.slider(
        "Retorno Esperado (% ao ano):",
        min_value=5,
        max_value=30,
        value=12,
        step=1
    )

with col_sim2:
    investment_years = st.slider(
        "Período (anos):",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

with col_sim3:
    monthly_contribution = st.number_input(
        "Aporte Mensal (R$):",
        min_value=0,
        max_value=10000,
        value=1000,
        step=500
    )

# Cálculo de projeção
monthly_rate = (1 + expected_return/100) ** (1/12) - 1
months = investment_years * 12

future_value = initial_capital * (1 + monthly_rate) ** months
for i in range(months):
    future_value += monthly_contribution * (1 + monthly_rate) ** (months - i - 1)

total_invested = initial_capital + (monthly_contribution * months)
total_profit = future_value - total_invested

st.success(f"""
**Projeção do Portfólio:**
- **Valor Futuro:** R$ {future_value:,.2f}
- **Total Investido:** R$ {total_invested:,.2f}  
- **Lucro Projetado:** R$ {total_profit:,.2f}
- **Retorno Total:** {(future_value/total_invested - 1)*100:.1f}%
""")

# CTA final
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; color: white;">
    <h2 style="color: white; margin-top: 0;">🚀 Pronto para Implementar?</h2>
    <p style="font-size: 1.1rem;">
        Esta demonstração mostra <strong>apenas 10%</strong> do poder do sistema QuantumBank OS completo.
    </p>
    
    <h4 style="color: white;">Para sua Fintech ou Banco Digital:</h4>
    <ul>
        <li><strong>Algoritmo Quântico Completo</strong> (não apenas demo)</li>
        <li><strong>Integração com suas APIs bancárias</strong></li>
        <li><strong>Dashboard personalizado com sua marca</strong></li>
        <li><strong>Relatórios de compliance automáticos</strong></li>
        <li><strong>Suporte técnico 24/7</strong></li>
    </ul>
    
    <h4 style="color: white;">📞 Entre em Contato:</h4>
    <p>
        <strong>Email:</strong> [seu-email@quantumbank.com](mailto:seu-email@quantumbank.com)<br>
        <strong>Modelo:</strong> Revenue-Share (70% para você, 30% para nós)<br>
        <strong>Custo Inicial:</strong> ZERO
    </p>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.caption("""
QuantumBank OS v1.0 • Desenvolvido por MontUniversal & Parceiro • 
[GitHub](https://github.com/LEVIATAMEDO/quantum-bank-os) • 
Licença: Revenue-Share Partnership
Add interactive dashboard

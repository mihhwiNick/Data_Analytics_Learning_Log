import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#==============================================================================
# CẤU HÌNH DỮ LIỆU MẪU
#==============================================================================

VN_STOCKS = {
    'VIC': {'name': 'Vingroup', 'sector': 'Bất động sản', 'base_price': 45.5},
    'VNM': {'name': 'Vinamilk', 'sector': 'Tiêu dùng', 'base_price': 75.2},
    'VCB': {'name': 'Vietcombank', 'sector': 'Ngân hàng', 'base_price': 95.8},
    'FPT': {'name': 'FPT Corporation', 'sector': 'Công nghệ', 'base_price': 85.6},
    'HPG': {'name': 'Hoa Phat Group', 'sector': 'Thép', 'base_price': 28.9}
}

def generate_price_history(ticker, days=30):
    """Tạo dữ liệu giá lịch sử"""
    base_price = VN_STOCKS[ticker]['base_price']
    dates = [datetime.now() - timedelta(days=x) for x in range(days, 0, -1)]
    
    prices = []
    current = base_price
    for i in range(days):
        change = np.random.uniform(-0.03, 0.03)
        current = current * (1 + change)
        prices.append(current)
    
    return pd.DataFrame({
        'Date': dates,
        'Close': prices,
        'Open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
        'High': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        'Low': [p * (1 + np.random.uniform(-0.02, 0)) for p in prices],
        'Volume': [np.random.randint(1000000, 5000000) for _ in prices]
    })

def get_stock_summary(ticker):
    """Tạo dữ liệu summary mẫu"""
    base_data = VN_STOCKS[ticker]
    current_price = base_data['base_price'] * (1 + np.random.uniform(-0.02, 0.02))
    prev_close = current_price * (1 + np.random.uniform(-0.01, 0.01))
    
    return {
        'Previous Close': f"{prev_close:.2f}",
        'Open': f"{current_price * 0.99:.2f}",
        'Bid': f"{current_price * 0.998:.2f} x 1,000",
        'Ask': f"{current_price * 1.002:.2f} x 500",
        "Day's Range": f"{current_price * 0.97:.2f} - {current_price * 1.03:.2f}",
        '52 Week Range': f"{base_data['base_price'] * 0.7:.2f} - {base_data['base_price'] * 1.4:.2f}",
        'Volume': f"{np.random.randint(1000000, 5000000):,}",
        'Avg. Volume': f"{np.random.randint(2000000, 4000000):,}",
        'Market Cap': f"{base_data['base_price'] * 1000000000:,.0f}",
        'Beta': f"{np.random.uniform(0.8, 1.5):.2f}",
        'PE Ratio (TTM)': f"{np.random.uniform(8, 20):.2f}",
        'EPS (TTM)': f"{base_data['base_price']/12:.2f}",
        'Earnings Date': '2024-01-25 to 2024-01-29'
    }

#==============================================================================
# TAB 1: SUMMARY
#==============================================================================

def tab1_summary():
    st.title("Summary")
    
    if ticker == '-':
        st.info("Select ticker on the left to begin")
        return
    
    st.write(f"## {ticker} - {VN_STOCKS[ticker]['name']}")
    
    # Lấy dữ liệu summary
    summary_data = get_stock_summary(ticker)
    
    # Hiển thị 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trading Information")
        left_data = {
            'Previous Close': summary_data['Previous Close'],
            'Open': summary_data['Open'],
            'Bid': summary_data['Bid'],
            'Ask': summary_data['Ask'],
            "Day's Range": summary_data["Day's Range"],
            '52 Week Range': summary_data['52 Week Range'],
            'Volume': summary_data['Volume'],
            'Avg. Volume': summary_data['Avg. Volume']
        }
        
        for key, value in left_data.items():
            st.write(f"**{key}:** {value}")
    
    with col2:
        st.subheader("Valuation Measures")
        right_data = {
            'Market Cap': summary_data['Market Cap'],
            'Beta (5Y Monthly)': summary_data['Beta'],
            'PE Ratio (TTM)': summary_data['PE Ratio (TTM)'],
            'EPS (TTM)': summary_data['EPS (TTM)'],
            'Earnings Date': summary_data['Earnings Date'],
            'Forward Dividend & Yield': '0.88 (0.59%)',
            'Ex-Dividend Date': 'Nov 05, 2024',
            '1y Target Est': f"{VN_STOCKS[ticker]['base_price'] * 1.2:.2f}"
        }
        
        for key, value in right_data.items():
            st.write(f"**{key}:** {value}")
    
    # Biểu đồ giá
    st.subheader("Price Chart")
    hist_data = generate_price_history(ticker, 180)  # 6 tháng
    
    fig = px.area(hist_data, x='Date', y='Close', 
                  title=f'{ticker} Historical Price')
    
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

#==============================================================================
# TAB 2: CHART
#==============================================================================

def tab2_chart():
    st.title("Chart")
    st.write(ticker)
    
    st.write("Set duration to '-' to select date range")
    
    # Controls
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        start_date = st.date_input("Start date", datetime.today().date() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End date", datetime.today().date())
    with col3:
        duration = st.selectbox("Select duration", ['-', '1M', '3M', '6M', 'YTD', '1Y'])
    with col4:
        inter = st.selectbox("Select interval", ['1d', '1w'])
    with col5:
        plot_type = st.selectbox("Select Plot", ['Line', 'Candle'])
    
    if ticker != '-':
        # Tạo dữ liệu chart
        hist_data = generate_price_history(ticker, 90)
        
        # Vẽ biểu đồ
        if plot_type == 'Line':
            fig = px.line(hist_data, x='Date', y='Close', title=f'{ticker} Price Chart')
        else:
            fig = go.Figure(data=[go.Candlestick(x=hist_data['Date'],
                open=hist_data['Open'], high=hist_data['High'],
                low=hist_data['Low'], close=hist_data['Close'])])
            fig.update_layout(title=f'{ticker} Candlestick Chart')
        
        st.plotly_chart(fig, use_container_width=True)

#==============================================================================
# TAB 3: STATISTICS
#==============================================================================

def tab3_statistics():
    st.title("Statistics")
    st.write(ticker)
    
    if ticker == '-':
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Valuation Measures")
        valuation_data = {
            'Market Cap': '2.461T',
            'Enterprise Value': '2.532T',
            'Trailing P/E': '26.74',
            'Forward P/E': '24.56',
            'PEG Ratio': '2.35'
        }
        for key, value in valuation_data.items():
            st.write(f"**{key}:** {value}")
        
        st.header("Financial Highlights")
        st.subheader("Fiscal Year")
        st.write("**Fiscal Year Ends:** Sep 30, 2024")
        st.write("**Most Recent Quarter:** Sep 30, 2024")
        
        st.subheader("Profitability")
        st.write("**Profit Margin:** 25.34%")
        st.write("**Operating Margin:** 29.15%")
        
    with col2:
        st.header("Trading Information")
        st.subheader("Stock Price History")
        price_data = {
            'Beta': '1.21',
            '52-Week Change': '12.45%',
            'S&P500 52-Week Change': '8.76%'
        }
        for key, value in price_data.items():
            st.write(f"**{key}:** {value}")
        
        st.subheader("Share Statistics")
        share_data = {
            'Avg Vol (3 month)': '75.72M',
            'Avg Vol (10 day)': '63.64M',
            'Shares Outstanding': '16.32B'
        }
        for key, value in share_data.items():
            st.write(f"**{key}:** {value}")

#==============================================================================
# TAB 4: FINANCIALS (ĐÃ FIX LỖI)
#==============================================================================

def tab4_financials():
    st.title("Financials")
    st.write(ticker)
    
    if ticker == '-':
        return
    
    statement = st.selectbox("Show", ['Income Statement', 'Balance Sheet', 'Cash Flow'])
    period = st.selectbox("Period", ['Yearly', 'Quarterly'])
    
    # Dữ liệu mẫu cho báo cáo tài chính - SỬA LẠI DÙNG st.table thay vì st.dataframe
    if statement == 'Income Statement':
        data = {
            'Item': ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income'],
            '2023': ['100.0B', '40.0B', '25.0B', '20.0B'],
            '2022': ['95.0B', '38.0B', '23.0B', '18.0B'],
            '2021': ['85.0B', '34.0B', '20.0B', '16.0B'],
            '2020': ['75.0B', '30.0B', '18.0B', '14.0B']
        }
    elif statement == 'Balance Sheet':
        data = {
            'Item': ['Total Assets', 'Total Liabilities', 'Total Equity', 'Cash'],
            '2023': ['150.0B', '80.0B', '70.0B', '25.0B'],
            '2022': ['140.0B', '75.0B', '65.0B', '22.0B'],
            '2021': ['130.0B', '70.0B', '60.0B', '20.0B'],
            '2020': ['120.0B', '65.0B', '55.0B', '18.0B']
        }
    else:  # Cash Flow
        data = {
            'Item': ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Net Change'],
            '2023': ['30.0B', '-15.0B', '-10.0B', '5.0B'],
            '2022': ['28.0B', '-12.0B', '-8.0B', '8.0B'],
            '2021': ['25.0B', '-10.0B', '-7.0B', '8.0B'],
            '2020': ['22.0B', '-8.0B', '-6.0B', '8.0B']
        }
    
    df = pd.DataFrame(data)
    st.table(df)

#==============================================================================
# TAB 5: ANALYSIS (TAB MỚI)
#==============================================================================

def tab5_analysis():
    st.title("Analysis")
    st.write(ticker)
    
    if ticker == '-':
        st.info("Select a ticker to view analysis")
        return
    
    st.write("**Currency in USD**")
    
    # 1. Analyst Recommendations
    st.header("📊 Analyst Recommendations")
    
    rec_data = {
        'Strong Buy': np.random.randint(15, 25),
        'Buy': np.random.randint(20, 30),
        'Hold': np.random.randint(10, 20),
        'Sell': np.random.randint(0, 5),
        'Strong Sell': np.random.randint(0, 3)
    }
    
    # Hiển thị biểu đồ recommendations
    fig_rec = px.pie(
        values=list(rec_data.values()), 
        names=list(rec_data.keys()),
        title=f'Analyst Recommendations for {ticker}'
    )
    st.plotly_chart(fig_rec, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Mean Recommendation", "Buy", "Strong Buy → Buy")
        st.metric("Price Target", f"{VN_STOCKS[ticker]['base_price'] * 1.15:.2f}", "+15%")
    
    with col2:
        st.metric("Number of Analysts", "25", "+2")
        st.metric("Rating Score", "2.1", "-0.2")
    
    # 2. Earnings Estimate
    st.header("📈 Earnings Estimate")
    
    earnings_data = {
        'Period': ['Current Qtr', 'Next Qtr', 'Current Year', 'Next Year'],
        'Avg Estimate': [
            f"${np.random.uniform(1.5, 2.5):.2f}", 
            f"${np.random.uniform(1.6, 2.6):.2f}",
            f"${np.random.uniform(6.5, 8.5):.2f}", 
            f"${np.random.uniform(7.0, 9.0):.2f}"
        ],
        'Low Estimate': [
            f"${np.random.uniform(1.2, 1.8):.2f}", 
            f"${np.random.uniform(1.3, 1.9):.2f}",
            f"${np.random.uniform(5.5, 7.0):.2f}", 
            f"${np.random.uniform(6.0, 7.5):.2f}"
        ],
        'High Estimate': [
            f"${np.random.uniform(2.5, 3.0):.2f}", 
            f"${np.random.uniform(2.6, 3.2):.2f}",
            f"${np.random.uniform(8.5, 10.0):.2f}", 
            f"${np.random.uniform(9.0, 11.0):.2f}"
        ]
    }
    
    st.table(pd.DataFrame(earnings_data))
    
    # 3. Revenue Estimate
    st.header("💰 Revenue Estimate")
    
    revenue_data = {
        'Period': ['Current Qtr', 'Next Qtr', 'Current Year', 'Next Year'],
        'Avg Estimate (B)': [
            f"${np.random.uniform(80, 120):.1f}",
            f"${np.random.uniform(85, 125):.1f}", 
            f"${np.random.uniform(350, 450):.1f}",
            f"${np.random.uniform(380, 480):.1f}"
        ],
        'Sales Growth (YoY)': [
            f"+{np.random.uniform(5, 15):.1f}%",
            f"+{np.random.uniform(6, 16):.1f}%", 
            f"+{np.random.uniform(8, 18):.1f}%",
            f"+{np.random.uniform(10, 20):.1f}%"
        ]
    }
    
    st.table(pd.DataFrame(revenue_data))

#==============================================================================
# TAB 6: MONTE CARLO SIMULATION
#==============================================================================

def tab6_monte_carlo():
    st.title("Monte Carlo Simulation")
    st.write(ticker)
    
    if ticker == '-':
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        simulations = st.selectbox("Number of Simulations (n)", [200, 500, 1000])
    with col2:
        time_horizon = st.selectbox("Time Horizon (t)", [30, 60, 90])
    
    # Tạo simulation đơn giản
    base_price = VN_STOCKS[ticker]['base_price']
    
    # Tạo dữ liệu simulation
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i in range(min(50, simulations)):  # Hiển thị 50 đường
        prices = [base_price]
        for _ in range(time_horizon):
            change = np.random.normal(0, 0.02)
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        ax.plot(prices, alpha=0.1, color='blue')
    
    ax.axhline(y=base_price, color='red', linestyle='--', linewidth=2)
    ax.set_title(f'Monte Carlo Simulation for {ticker}')
    ax.set_xlabel('Days')
    ax.set_ylabel('Price')
    
    st.pyplot(fig)
    
    # Value at Risk
    st.subheader('Value at Risk (VaR)')
    ending_prices = [base_price * (1 + np.random.normal(0, 0.15)) for _ in range(1000)]
    var_95 = base_price - np.percentile(ending_prices, 5)
    
    st.write(f'VaR at 95% confidence interval is: {var_95:.2f} USD')

#==============================================================================
# TAB 7: PORTFOLIO TREND
#==============================================================================

def tab7_portfolio():
    st.title("Your Portfolio's Trend")
    
    # Chọn các mã cổ phiếu
    selected_tickers = st.multiselect(
        "Select tickers in your portfolio",
        options=list(VN_STOCKS.keys()),
        default=['VIC', 'VNM', 'VCB']
    )
    
    if selected_tickers:
        # Tạo dữ liệu portfolio
        portfolio_data = pd.DataFrame()
        
        for t in selected_tickers:
            hist_data = generate_price_history(t, 365)  # 1 năm
            portfolio_data[t] = hist_data['Close'].values
        
        portfolio_data.index = hist_data['Date']
        
        # Vẽ biểu đồ
        fig = px.line(portfolio_data, title='Portfolio Performance')
        st.plotly_chart(fig, use_container_width=True)
        
        # Hiển thị thông tin portfolio
        st.subheader("Portfolio Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Value", "1,250,000,000 VND", "2.5%")
        with col2:
            st.metric("Daily P&L", "+1,250,000 VND", "0.1%")
        with col3:
            st.metric("YTD Return", "+15.2%", "1.3%")

#==============================================================================
# MAIN APP
#==============================================================================

def main():
    st.sidebar.title("VN Stock Dashboard")
    
    # Danh sách ticker
    ticker_list = ['-'] + list(VN_STOCKS.keys())
    global ticker
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    
    # Chọn tab - ĐÃ SẮP XẾP LẠI
    tabs = {
        "Summary": tab1_summary,
        "Chart": tab2_chart, 
        "Statistics": tab3_statistics,
        "Financials": tab4_financials,
        "Analysis": tab5_analysis,      # Tab 5: Analysis
        "Monte Carlo Simulation": tab6_monte_carlo,  # Tab 6
        "Your Portfolio's Trend": tab7_portfolio     # Tab 7
    }
    
    selected_tab = st.sidebar.radio("Select tab", list(tabs.keys()))
    
    # Hiển thị tab được chọn
    tabs[selected_tab]()

if __name__ == "__main__":
    st.set_page_config(page_title="VN Stock Dashboard", layout="wide")
    main()
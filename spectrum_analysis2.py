import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Spectrum Auction Dashboard 2023-24",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .band-header {
        color: #2e8b57;
        font-size: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">📡 Spectrum Auction Dashboard 2023-24</h1>', unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_spectrum_data():
    """Load and process spectrum auction data"""
    
    # 800 MHz Band Data
    data_800mhz = {
        'State': ['Andhra Pradesh', 'Bihar', 'Delhi', 'Gujarat', 'Haryana', 'Himachal Pradesh', 
                 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Kolkata', 'Madhya Pradesh', 
                 'Maharashtra', 'Mumbai', 'Odisha', 'Punjab', 'Rajasthan', 'Tamil Nadu', 
                 'Uttar Pradesh (East)', 'West Bengal'],
        'Blocks_800MHz': [8, 8, 5, 3, 3, 6, 2, 5, 5, 4, 4, 4, 4, 7, 6, 4, 5, 8, 4],
        'Quantum_800MHz': [10.0, 10.0, 6.25, 3.75, 3.75, 7.5, 2.5, 6.25, 6.25, 5.0, 5.0, 5.0, 5.0, 8.75, 7.5, 5.0, 6.25, 10.0, 5.0]
    }
    
    # 900 MHz Band Data
    data_900mhz = {
        'State': ['Andhra Pradesh', 'Assam', 'Bihar', 'Delhi', 'Gujarat', 'Haryana', 
                 'Himachal Pradesh', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Kolkata', 
                 'Madhya Pradesh', 'Maharashtra', 'Mumbai', 'North East', 'Odisha', 'Punjab', 
                 'Rajasthan', 'Tamil Nadu', 'Uttar Pradesh (East)', 'Uttar Pradesh (West)', 'West Bengal'],
        'Blocks_900MHz': [22, 34, 59, 4, 8, 23, 17, 67, 23, 7, 14, 22, 14, 4, 22, 42, 6, 22, 42, 31, 59, 44],
        'Quantum_900MHz': [4.4, 6.8, 11.8, 0.8, 1.6, 4.6, 3.4, 13.4, 4.6, 1.4, 2.8, 4.4, 2.8, 0.8, 4.4, 8.4, 1.2, 4.4, 8.4, 6.2, 11.8, 8.8]
    }
    
    # 1800 MHz Band Data
    data_1800mhz = {
        'State': ['Andhra Pradesh', 'Assam', 'Bihar', 'Delhi', 'Gujarat', 'Haryana', 
                 'Himachal Pradesh', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Kolkata', 
                 'Madhya Pradesh', 'Maharashtra', 'Mumbai', 'North East', 'Odisha', 'Punjab', 
                 'Rajasthan', 'Tamil Nadu', 'Uttar Pradesh (East)'],
        'Blocks_1800MHz': [45, 43, 51, 55, 20, 142, 66, 30, 24, 127, 93, 6, 12, 92, 11, 44, 49, 35, 17, 5],
        'Quantum_1800MHz': [9.0, 8.6, 10.2, 11.0, 4.0, 28.4, 13.2, 6.0, 4.8, 25.4, 18.6, 1.2, 2.4, 18.4, 2.2, 8.8, 9.8, 7.0, 3.4, 1.0]
    }
    
    # High frequency bands data
    high_freq_data = {
        'State': ['Andhra Pradesh', 'Assam', 'Bihar', 'Delhi', 'Gujarat', 'Haryana', 
                 'Himachal Pradesh', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Kolkata', 
                 'Madhya Pradesh', 'Maharashtra', 'Mumbai', 'North East', 'Odisha', 'Punjab', 
                 'Rajasthan', 'Tamil Nadu', 'Uttar Pradesh (East)', 'Uttar Pradesh (West)', 'West Bengal'],
        '2100MHz': [15, 5, 0, 10, 5, 0, 15, 5, 5, 0, 10, 10, 5, 10, 5, 10, 5, 0, 0, 0, 10, 0],
        '2300MHz': [10, 0, 0, 10, 0, 0, 0, 0, 10, 0, 10, 0, 0, 10, 0, 0, 0, 0, 10, 0, 0, 0],
        '2500MHz': [0, 0, 10, 0, 0, 0, 10, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0],
        '3300MHz': [50, 100, 50, 50, 50, 50, 70, 70, 20, 20, 50, 20, 50, 50, 70, 100, 50, 20, 50, 50, 20, 50],
        '26GHz': [400, 650, 650, 450, 100, 250, 650, 650, 400, 0, 450, 250, 250, 350, 650, 650, 350, 300, 300, 400, 300, 250]
    }
    
    # Create DataFrames
    df_800 = pd.DataFrame(data_800mhz)
    df_900 = pd.DataFrame(data_900mhz)
    df_1800 = pd.DataFrame(data_1800mhz)
    df_high = pd.DataFrame(high_freq_data)
    
    return df_800, df_900, df_1800, df_high

# Load data
df_800, df_900, df_1800, df_high = load_spectrum_data()

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox("Select Analysis View", [
    "Executive Summary", 
    "Band-wise Analysis", 
    "State-wise Comparison", 
    "Market Opportunities",
    "Strategic Insights"
])

if page == "Executive Summary":
    st.header("📈 Executive Summary")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_800_quantum = df_800['Quantum_800MHz'].sum()
        st.metric("Total 800MHz Spectrum", f"{total_800_quantum:.1f} MHz", "Primary Band")
    
    with col2:
        total_900_quantum = df_900['Quantum_900MHz'].sum()
        st.metric("Total 900MHz Spectrum", f"{total_900_quantum:.1f} MHz", "High Demand")
    
    with col3:
        total_1800_quantum = df_1800['Quantum_1800MHz'].sum()
        st.metric("Total 1800MHz Spectrum", f"{total_1800_quantum:.1f} MHz", "LTE Primary")
    
    with col4:
        total_states = len(set(df_800['State'].tolist() + df_900['State'].tolist() + df_1800['State'].tolist()))
        st.metric("Coverage Areas", f"{total_states}", "States/Circles")
    
    st.markdown("---")
    
    # Total spectrum by band
    st.subheader("📊 Total Spectrum Available by Band")
    
    band_totals = {
        'Band': ['800 MHz', '900 MHz', '1800 MHz', '2100 MHz', '2300 MHz', '2500 MHz', '3300 MHz', '26 GHz'],
        'Total_MHz': [
            df_800['Quantum_800MHz'].sum(),
            df_900['Quantum_900MHz'].sum(), 
            df_1800['Quantum_1800MHz'].sum(),
            df_high['2100MHz'].sum(),
            df_high['2300MHz'].sum(),
            df_high['2500MHz'].sum(),
            df_high['3300MHz'].sum(),
            df_high['26GHz'].sum()
        ]
    }
    
    df_bands = pd.DataFrame(band_totals)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_bands = px.bar(df_bands, x='Band', y='Total_MHz', 
                          title="Total Spectrum Available by Frequency Band",
                          color='Total_MHz',
                          color_continuous_scale='viridis')
        fig_bands.update_layout(height=400)
        st.plotly_chart(fig_bands, use_container_width=True)
    
    with col2:
        fig_pie = px.pie(df_bands, values='Total_MHz', names='Band',
                        title="Spectrum Distribution")
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Market insights
    st.subheader("💡 Key Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **High-Value Opportunities:**
        - 26 GHz band offers massive spectrum (6,650 MHz total)
        - 3300 MHz provides good capacity for 5G deployment
        - 900 MHz highly valuable for coverage
        """)
    
    with col2:
        st.markdown("""
        **Strategic Considerations:**
        - Limited 800/900 MHz availability requires strategic bidding
        - High frequency bands (3300 MHz, 26 GHz) support capacity needs
        - State-wise variations create regional opportunities
        """)

elif page == "Band-wise Analysis":
    st.header("📡 Band-wise Spectrum Analysis")
    
    # Band selection
    selected_band = st.selectbox("Select Frequency Band for Analysis", 
                                ["800 MHz", "900 MHz", "1800 MHz", "High Frequency Bands"])
    
    if selected_band == "800 MHz":
        st.subheader("800 MHz Band Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_800_blocks = px.bar(df_800, x='State', y='Blocks_800MHz',
                                   title="800 MHz Blocks by State",
                                   color='Blocks_800MHz',
                                   color_continuous_scale='blues')
            fig_800_blocks.update_xaxes(tickangle=45)
            st.plotly_chart(fig_800_blocks, use_container_width=True)
        
        with col2:
            fig_800_quantum = px.bar(df_800, x='State', y='Quantum_800MHz',
                                    title="800 MHz Spectrum Quantum by State",
                                    color='Quantum_800MHz',
                                    color_continuous_scale='greens')
            fig_800_quantum.update_xaxes(tickangle=45)
            st.plotly_chart(fig_800_quantum, use_container_width=True)
        
        # Top opportunities
        st.subheader("Top 800 MHz Opportunities")
        top_800 = df_800.nlargest(5, 'Quantum_800MHz')[['State', 'Blocks_800MHz', 'Quantum_800MHz']]
        st.dataframe(top_800, use_container_width=True)
    
    elif selected_band == "900 MHz":
        st.subheader("900 MHz Band Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_900_blocks = px.bar(df_900, x='State', y='Blocks_900MHz',
                                   title="900 MHz Blocks by State",
                                   color='Blocks_900MHz',
                                   color_continuous_scale='oranges')
            fig_900_blocks.update_xaxes(tickangle=45)
            st.plotly_chart(fig_900_blocks, use_container_width=True)
        
        with col2:
            fig_900_quantum = px.bar(df_900, x='State', y='Quantum_900MHz',
                                    title="900 MHz Spectrum Quantum by State", 
                                    color='Quantum_900MHz',
                                    color_continuous_scale='reds')
            fig_900_quantum.update_xaxes(tickangle=45)
            st.plotly_chart(fig_900_quantum, use_container_width=True)
        
        # Distribution analysis
        st.subheader("900 MHz Distribution Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(df_900, x='Quantum_900MHz', nbins=10,
                                   title="Distribution of 900 MHz Spectrum Quantum")
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Top opportunities
            st.subheader("Top 900 MHz Opportunities")
            top_900 = df_900.nlargest(5, 'Quantum_900MHz')[['State', 'Blocks_900MHz', 'Quantum_900MHz']]
            st.dataframe(top_900, use_container_width=True)
    
    elif selected_band == "1800 MHz":
        st.subheader("1800 MHz Band Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_1800_blocks = px.bar(df_1800, x='State', y='Blocks_1800MHz',
                                    title="1800 MHz Blocks by State",
                                    color='Blocks_1800MHz',
                                    color_continuous_scale='purples')
            fig_1800_blocks.update_xaxes(tickangle=45)
            st.plotly_chart(fig_1800_blocks, use_container_width=True)
        
        with col2:
            fig_1800_quantum = px.bar(df_1800, x='State', y='Quantum_1800MHz',
                                     title="1800 MHz Spectrum Quantum by State",
                                     color='Quantum_1800MHz',
                                     color_continuous_scale='viridis')
            fig_1800_quantum.update_xaxes(tickangle=45)
            st.plotly_chart(fig_1800_quantum, use_container_width=True)
        
        # Top opportunities
        st.subheader("Top 1800 MHz Opportunities")
        top_1800 = df_1800.nlargest(5, 'Quantum_1800MHz')[['State', 'Blocks_1800MHz', 'Quantum_1800MHz']]
        st.dataframe(top_1800, use_container_width=True)
    
    else:  # High Frequency Bands
        st.subheader("High Frequency Bands Analysis")
        
        # Heatmap for high frequency bands
        high_freq_matrix = df_high.set_index('State')[['2100MHz', '2300MHz', '2500MHz', '3300MHz', '26GHz']]
        
        fig_heatmap = px.imshow(high_freq_matrix.T, 
                               title="High Frequency Spectrum Availability Heatmap",
                               color_continuous_scale='viridis',
                               aspect='auto')
        fig_heatmap.update_layout(height=500)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Individual band analysis
        col1, col2 = st.columns(2)
        
        with col1:
            fig_3300 = px.bar(df_high, x='State', y='3300MHz',
                             title="3300 MHz Spectrum by State",
                             color='3300MHz',
                             color_continuous_scale='plasma')
            fig_3300.update_xaxes(tickangle=45)
            st.plotly_chart(fig_3300, use_container_width=True)
        
        with col2:
            fig_26ghz = px.bar(df_high, x='State', y='26GHz',
                              title="26 GHz Spectrum by State",
                              color='26GHz',
                              color_continuous_scale='inferno')
            fig_26ghz.update_xaxes(tickangle=45)
            st.plotly_chart(fig_26ghz, use_container_width=True)

elif page == "State-wise Comparison":
    st.header("🗺️ State-wise Spectrum Comparison")
    
    # State selection
    selected_states = st.multiselect("Select States for Comparison", 
                                    df_800['State'].tolist(),
                                    default=['Andhra Pradesh', 'Delhi', 'Maharashtra', 'Karnataka'])
    
    if selected_states:
        # Merge data for selected states
        df_merged = df_800[df_800['State'].isin(selected_states)].copy()
        
        # Add 900 MHz data
        df_900_filtered = df_900[df_900['State'].isin(selected_states)]
        df_merged = df_merged.merge(df_900_filtered[['State', 'Quantum_900MHz']], on='State', how='left')
        
        # Add 1800 MHz data
        df_1800_filtered = df_1800[df_1800['State'].isin(selected_states)]
        df_merged = df_merged.merge(df_1800_filtered[['State', 'Quantum_1800MHz']], on='State', how='left')
        
        # Fill NaN values with 0
        df_merged = df_merged.fillna(0)
        
        # Stacked bar chart
        fig_stacked = go.Figure()
        
        fig_stacked.add_trace(go.Bar(name='800 MHz', x=df_merged['State'], y=df_merged['Quantum_800MHz']))
        fig_stacked.add_trace(go.Bar(name='900 MHz', x=df_merged['State'], y=df_merged['Quantum_900MHz']))
        fig_stacked.add_trace(go.Bar(name='1800 MHz', x=df_merged['State'], y=df_merged['Quantum_1800MHz']))
        
        fig_stacked.update_layout(barmode='stack', title='Total Spectrum Comparison by State')
        st.plotly_chart(fig_stacked, use_container_width=True)
        
        # Detailed comparison table
        st.subheader("Detailed Spectrum Comparison")
        
        # Calculate total spectrum
        df_merged['Total_Spectrum'] = df_merged['Quantum_800MHz'] + df_merged['Quantum_900MHz'] + df_merged['Quantum_1800MHz']
        
        comparison_table = df_merged[['State', 'Quantum_800MHz', 'Quantum_900MHz', 'Quantum_1800MHz', 'Total_Spectrum']]
        comparison_table.columns = ['State', '800 MHz', '900 MHz', '1800 MHz', 'Total (MHz)']
        
        st.dataframe(comparison_table, use_container_width=True)
        
        # Market share analysis
        st.subheader("Market Share Analysis")
        
        total_available = comparison_table['Total (MHz)'].sum()
        comparison_table['Market Share %'] = (comparison_table['Total (MHz)'] / total_available * 100).round(2)
        
        fig_pie_states = px.pie(comparison_table, values='Total (MHz)', names='State',
                               title=f"Market Share Among Selected States")
        st.plotly_chart(fig_pie_states, use_container_width=True)

elif page == "Market Opportunities":
    st.header("💼 Market Opportunities Analysis")
    
    # Calculate opportunity scores
    st.subheader("Opportunity Scoring Matrix")
    
    # Merge all data for comprehensive analysis
    df_opportunities = df_800.copy()
    df_opportunities = df_opportunities.merge(df_900[['State', 'Quantum_900MHz']], on='State', how='left')
    df_opportunities = df_opportunities.merge(df_1800[['State', 'Quantum_1800MHz']], on='State', how='left')
    df_opportunities = df_opportunities.merge(df_high[['State', '3300MHz', '26GHz']], on='State', how='left')
    df_opportunities = df_opportunities.fillna(0)
    
    # Calculate opportunity scores (normalized)
    df_opportunities['Coverage_Score'] = (df_opportunities['Quantum_800MHz'] + df_opportunities['Quantum_900MHz']) / 2
    df_opportunities['Capacity_Score'] = (df_opportunities['Quantum_1800MHz'] + df_opportunities['3300MHz']/10) / 2
    df_opportunities['Future_Score'] = df_opportunities['26GHz'] / 100
    df_opportunities['Total_Score'] = (df_opportunities['Coverage_Score'] + df_opportunities['Capacity_Score'] + df_opportunities['Future_Score']) / 3
    
    # Opportunity matrix
    fig_opportunity = px.scatter(df_opportunities, x='Coverage_Score', y='Capacity_Score',
                               size='Future_Score', color='Total_Score',
                               hover_name='State',
                               title="Market Opportunity Matrix",
                               labels={'Coverage_Score': 'Coverage Opportunity (800+900 MHz)',
                                      'Capacity_Score': 'Capacity Opportunity (1800+3300 MHz)'})
    
    st.plotly_chart(fig_opportunity, use_container_width=True)
    
    # Top opportunities
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Top Coverage Opportunities")
        top_coverage = df_opportunities.nlargest(5, 'Coverage_Score')[['State', 'Coverage_Score', 'Quantum_800MHz', 'Quantum_900MHz']]
        st.dataframe(top_coverage, use_container_width=True)
    
    with col2:
        st.subheader("🚀 Top Capacity Opportunities") 
        top_capacity = df_opportunities.nlargest(5, 'Capacity_Score')[['State', 'Capacity_Score', 'Quantum_1800MHz', '3300MHz']]
        st.dataframe(top_capacity, use_container_width=True)
    
    # Investment recommendations
    st.subheader("💡 Investment Recommendations")
    
    high_value_states = df_opportunities[df_opportunities['Total_Score'] > df_opportunities['Total_Score'].quantile(0.75)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**High Priority States:**")
        for state in high_value_states['State'].tolist():
            st.write(f"• {state}")
    
    with col2:
        st.markdown("**Strategic Focus Areas:**")
        st.write("• Prioritize 800/900 MHz for coverage")
        st.write("• Target 3300 MHz for 5G capacity")
        st.write("• Consider 26 GHz for future readiness")
        st.write("• Focus on high-scoring states first")

else:  # Strategic Insights
    st.header("🎯 Strategic Insights & Recommendations")
    
    # Portfolio optimization
    st.subheader("📊 Portfolio Optimization Analysis")
    
    # Calculate total investment scenarios
    df_strategy = df_800.copy()
    df_strategy = df_strategy.merge(df_900[['State', 'Quantum_900MHz']], on='State', how='left')
    df_strategy = df_strategy.merge(df_1800[['State', 'Quantum_1800MHz']], on='State', how='left')
    df_strategy = df_strategy.merge(df_high[['State', '3300MHz', '26GHz']], on='State', how='left')
    df_strategy = df_strategy.fillna(0)
    
    # Scenario analysis
    st.subheader("📈 Investment Scenarios")
    
    scenario = st.selectbox("Select Investment Strategy", 
                           ["Conservative (Low Bands Focus)", 
                            "Balanced Portfolio", 
                            "Aggressive (5G Focus)",
                            "Future-Ready (High Bands)"])
    
    if scenario == "Conservative (Low Bands Focus)":
        df_strategy['Priority_Score'] = df_strategy['Quantum_800MHz'] * 0.5 + df_strategy['Quantum_900MHz'] * 0.5
        focus_bands = "800 MHz & 900 MHz"
        strategy_desc = "Focus on coverage and rural penetration"
        
    elif scenario == "Balanced Portfolio":
        df_strategy['Priority_Score'] = (df_strategy['Quantum_800MHz'] * 0.3 + 
                                       df_strategy['Quantum_900MHz'] * 0.3 + 
                                       df_strategy['Quantum_1800MHz'] * 0.4)
        focus_bands = "All traditional bands"
        strategy_desc = "Balanced coverage and capacity"
        
    elif scenario == "Aggressive (5G Focus)":
        df_strategy['Priority_Score'] = (df_strategy['Quantum_1800MHz'] * 0.4 + 
                                       df_strategy['3300MHz'] * 0.6)
        focus_bands = "1800 MHz & 3300 MHz"
        strategy_desc = "5G deployment and urban capacity"
        
    else:  # Future-Ready
        df_strategy['Priority_Score'] = (df_strategy['3300MHz'] * 0.4 + 
                                       df_strategy['26GHz'] * 0.6)
        focus_bands = "3300 MHz & 26 GHz"
        strategy_desc = "Future 5G advanced services"
    
    # Display strategy results
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_strategy = px.bar(df_strategy.nlargest(10, 'Priority_Score'), 
                             x='State', y='Priority_Score',
                             title=f"Top States for {scenario} Strategy",
                             color='Priority_Score',
                             color_continuous_scale='viridis')
        fig_strategy.update_xaxes(tickangle=45)
        st.plotly_chart(fig_strategy, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        **Strategy Details:**
        - **Focus Bands:** {focus_bands}
        - **Objective:** {strategy_desc}
        - **Top State:** {df_strategy.loc[df_strategy['Priority_Score'].idxmax(), 'State']}
        - **Score Range:** {df_strategy['Priority_Score'].min():.1f} - {df_strategy['Priority_Score'].max():.1f}
        """)
    
    # Risk analysis
    st.subheader("⚠️ Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **High Competition Risk:**
        - Delhi (limited spectrum)
        - Mumbai (high demand)
        - Bangalore markets
        """)
    
    with col2:
        st.markdown("""
        **Medium Risk:**
        - Tier-1 cities
        - High growth states
        - Industrial hubs
        """)
    
    with col3:
        st.markdown("""
        **Low Risk:**
        - Rural-focused circles
        - Northeastern states
        - Niche frequency bands
        """)
    
    # Final recommendations
    st.subheader("🏆 Final Strategic Recommendations")
    
    recommendations = """
    ## Key Recommendations for Spectrum Auction Strategy:
    
    ### 1. **Priority Bands by Use Case**
    - **Coverage Extension**: Focus on 800/900 MHz in rural areas
    - **Urban Capacity**: Target 1800/2100 MHz in metro circles  
    - **5G Deployment**: Secure 3300 MHz for immediate 5G rollout
    - **Future Readiness**: Consider 26 GHz for advanced 5G services
    
    ### 2. **Geographic Strategy**
    - **Tier-1 Markets**: Balanced portfolio across all bands
    - **Tier-2 Cities**: Focus on 1800/3300 MHz for growth
    - **Rural Areas**: Prioritize 800/900 MHz for coverage
    
    ### 3. **Budget Allocation Guidelines**
    - **40%**: Low bands (800/900 MHz) for coverage
    - **35%**: Mid bands (1800/2100 MHz) for capacity
    - **20%**: 3300 MHz for 5G
    - **5%**: 26 GHz for future readiness
    
    ### 4. **Risk Mitigation**
    - Diversify across multiple bands and circles
    - Avoid over-concentration in high-competition areas
    - Maintain strategic reserves for opportunistic bidding
    
    ### 5. **Timeline Considerations**
    - **Immediate (0-6 months)**: Deploy acquired 1800/3300 MHz
    - **Short-term (6-18 months)**: Roll out 5G services
    - **Medium-term (1-3 years)**: Optimize network with all bands
    - **Long-term (3+ years)**: Leverage 26 GHz for advanced services
    """
    
    st.markdown(recommendations)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    📡 Spectrum Auction Dashboard 2023-24 | Strategic Decision Support Tool
</div>
""", unsafe_allow_html=True)

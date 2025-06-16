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
        'State': ['Andhra Pradesh', 'Bihar', 'Delhi', 'Gujarat', 'Haryana', 
                 'Himachal Pradesh', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Kolkata', 
                 'Madhya Pradesh', 'Maharashtra', 'Mumbai', 'Odisha', 'Punjab', 
                 'Rajasthan', 'Tamil Nadu', 'Uttar Pradesh (East)', 'West Bengal'],
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
    "State-wise Comparison"
])

if page == "Executive Summary":
    st.header("📈 Executive Summary")
    
    # Key metrics for all bands
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_800_quantum = df_800['Quantum_800MHz'].sum()
        st.metric("Total 800MHz Spectrum", f"{total_800_quantum:.2f} MHz", "Coverage")
        
        total_900_quantum = df_900['Quantum_900MHz'].sum()
        st.metric("Total 900MHz Spectrum", f"{total_900_quantum:.1f} MHz", "High Demand")
    
    with col2:
        total_1800_quantum = df_1800['Quantum_1800MHz'].sum()
        st.metric("Total 1800MHz Spectrum", f"{total_1800_quantum:.1f} MHz", "LTE Primary")
        
        total_2100_quantum = df_high['2100MHz'].sum()
        st.metric("Total 2100MHz Spectrum", f"{total_2100_quantum:.0f} MHz", "3G/LTE")
    
    with col3:
        total_2300_quantum = df_high['2300MHz'].sum()
        st.metric("Total 2300MHz Spectrum", f"{total_2300_quantum:.0f} MHz", "LTE TDD")
        
        total_2500_quantum = df_high['2500MHz'].sum()
        st.metric("Total 2500MHz Spectrum", f"{total_2500_quantum:.0f} MHz", "Broadband")
    
    with col4:
        total_3300_quantum = df_high['3300MHz'].sum()
        st.metric("Total 3300MHz Spectrum", f"{total_3300_quantum:.0f} MHz", "5G")
        
        total_26ghz_quantum = df_high['26GHz'].sum()
        st.metric("Total 26GHz Spectrum", f"{total_26ghz_quantum:.0f} MHz", "mmWave 5G")
    
    st.markdown("---")
    
    # Total spectrum by band (including all bands)
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

elif page == "Band-wise Analysis":
    st.header("📡 Band-wise Spectrum Analysis")
    
    # Updated band selection to include all bands
    selected_band = st.selectbox("Select Frequency Band for Analysis", 
                                ["800 MHz", "900 MHz", "1800 MHz", "2100 MHz", "2300 MHz", "2500 MHz", "3300 MHz", "26 GHz"])
    
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
        
        # Top 10 opportunities
        st.subheader("Top 800 MHz Opportunities")
        top_800 = df_800.nlargest(10, 'Quantum_800MHz')[['State', 'Blocks_800MHz', 'Quantum_800MHz']]
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
        
        # Top 10 opportunities
        st.subheader("Top 900 MHz Opportunities")
        top_900 = df_900.nlargest(10, 'Quantum_900MHz')[['State', 'Blocks_900MHz', 'Quantum_900MHz']]
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
        
        # Top 10 opportunities
        st.subheader("Top 1800 MHz Opportunities")
        top_1800 = df_1800.nlargest(10, 'Quantum_1800MHz')[['State', 'Blocks_1800MHz', 'Quantum_1800MHz']]
        st.dataframe(top_1800, use_container_width=True)
    
    elif selected_band == "2100 MHz":
        st.subheader("2100 MHz Band Analysis")
        
        # Filter states with non-zero 2100 MHz spectrum
        df_2100_filtered = df_high[df_high['2100MHz'] > 0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_2100 = px.bar(df_2100_filtered, x='State', y='2100MHz',
                             title="2100 MHz Spectrum by State",
                             color='2100MHz',
                             color_continuous_scale='blues')
            fig_2100.update_xaxes(tickangle=45)
            st.plotly_chart(fig_2100, use_container_width=True)
        
        with col2:
            # Summary statistics
            st.subheader("2100 MHz Summary")
            total_2100 = df_high['2100MHz'].sum()
            available_states = len(df_2100_filtered)
            avg_spectrum = df_2100_filtered['2100MHz'].mean() if not df_2100_filtered.empty else 0
            
            st.metric("Total 2100 MHz Spectrum", f"{total_2100} MHz")
            st.metric("States with 2100 MHz", f"{available_states}")
            st.metric("Average per State", f"{avg_spectrum:.1f} MHz")
        
        # Top 10 opportunities
        st.subheader("Top 2100 MHz Opportunities")
        if not df_2100_filtered.empty:
            top_2100 = df_2100_filtered.nlargest(10, '2100MHz')[['State', '2100MHz']]
            st.dataframe(top_2100, use_container_width=True)
        else:
            st.write("No states have 2100 MHz spectrum available.")
    
    elif selected_band == "2300 MHz":
        st.subheader("2300 MHz Band Analysis")
        
        # Filter states with non-zero 2300 MHz spectrum
        df_2300_filtered = df_high[df_high['2300MHz'] > 0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not df_2300_filtered.empty:
                fig_2300 = px.bar(df_2300_filtered, x='State', y='2300MHz',
                                 title="2300 MHz Spectrum by State",
                                 color='2300MHz',
                                 color_continuous_scale='greens')
                fig_2300.update_xaxes(tickangle=45)
                st.plotly_chart(fig_2300, use_container_width=True)
            else:
                st.write("No visualization available - limited state coverage")
        
        with col2:
            # Summary statistics
            st.subheader("2300 MHz Summary")
            total_2300 = df_high['2300MHz'].sum()
            available_states = len(df_2300_filtered)
            
            st.metric("Total 2300 MHz Spectrum", f"{total_2300} MHz")
            st.metric("States with 2300 MHz", f"{available_states}")
            if available_states > 0:
                avg_spectrum = df_2300_filtered['2300MHz'].mean()
                st.metric("Average per State", f"{avg_spectrum:.1f} MHz")
        
        # Top 10 opportunities
        st.subheader("Top 2300 MHz Opportunities")
        if not df_2300_filtered.empty:
            top_2300 = df_2300_filtered.nlargest(10, '2300MHz')[['State', '2300MHz']]
            st.dataframe(top_2300, use_container_width=True)
        else:
            st.write("No states have 2300 MHz spectrum available.")
    
    elif selected_band == "2500 MHz":
        st.subheader("2500 MHz Band Analysis")
        
        # Filter states with non-zero 2500 MHz spectrum
        df_2500_filtered = df_high[df_high['2500MHz'] > 0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not df_2500_filtered.empty:
                fig_2500 = px.bar(df_2500_filtered, x='State', y='2500MHz',
                                 title="2500 MHz Spectrum by State",
                                 color='2500MHz',
                                 color_continuous_scale='reds')
                fig_2500.update_xaxes(tickangle=45)
                st.plotly_chart(fig_2500, use_container_width=True)
            else:
                st.write("No visualization available - limited state coverage")
        
        with col2:
            # Summary statistics
            st.subheader("2500 MHz Summary")
            total_2500 = df_high['2500MHz'].sum()
            available_states = len(df_2500_filtered)
            
            st.metric("Total 2500 MHz Spectrum", f"{total_2500} MHz")
            st.metric("States with 2500 MHz", f"{available_states}")
            if available_states > 0:
                avg_spectrum = df_2500_filtered['2500MHz'].mean()
                st.metric("Average per State", f"{avg_spectrum:.1f} MHz")
        
        # Top 10 opportunities
        st.subheader("Top 2500 MHz Opportunities")
        if not df_2500_filtered.empty:
            top_2500 = df_2500_filtered.nlargest(10, '2500MHz')[['State', '2500MHz']]
            st.dataframe(top_2500, use_container_width=True)
        else:
            st.write("No states have 2500 MHz spectrum available.")
    
    elif selected_band == "3300 MHz":
        st.subheader("3300 MHz Band Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_3300 = px.bar(df_high, x='State', y='3300MHz',
                             title="3300 MHz Spectrum by State",
                             color='3300MHz',
                             color_continuous_scale='plasma')
            fig_3300.update_xaxes(tickangle=45)
            st.plotly_chart(fig_3300, use_container_width=True)
        
        with col2:
            # Summary statistics
            st.subheader("3300 MHz Summary")
            total_3300 = df_high['3300MHz'].sum()
            available_states = len(df_high[df_high['3300MHz'] > 0])
            avg_spectrum = df_high[df_high['3300MHz'] > 0]['3300MHz'].mean()
            
            st.metric("Total 3300 MHz Spectrum", f"{total_3300} MHz")
            st.metric("States with 3300 MHz", f"{available_states}")
            st.metric("Average per State", f"{avg_spectrum:.1f} MHz")
        
        # Top 10 opportunities
        st.subheader("Top 3300 MHz Opportunities")
        top_3300 = df_high.nlargest(10, '3300MHz')[['State', '3300MHz']]
        st.dataframe(top_3300, use_container_width=True)
    
    elif selected_band == "26 GHz":
        st.subheader("26 GHz Band Analysis")
        
        # Filter states with non-zero 26 GHz spectrum
        df_26ghz_filtered = df_high[df_high['26GHz'] > 0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_26ghz = px.bar(df_26ghz_filtered, x='State', y='26GHz',
                              title="26 GHz Spectrum by State",
                              color='26GHz',
                              color_continuous_scale='inferno')
            fig_26ghz.update_xaxes(tickangle=45)
            st.plotly_chart(fig_26ghz, use_container_width=True)
        
        with col2:
            # Summary statistics
            st.subheader("26 GHz Summary")
            total_26ghz = df_high['26GHz'].sum()
            available_states = len(df_26ghz_filtered)
            avg_spectrum = df_26ghz_filtered['26GHz'].mean() if not df_26ghz_filtered.empty else 0
            
            st.metric("Total 26 GHz Spectrum", f"{total_26ghz} MHz")
            st.metric("States with 26 GHz", f"{available_states}")
            st.metric("Average per State", f"{avg_spectrum:.1f} MHz")
        
        # Top 10 opportunities
        st.subheader("Top 26 GHz Opportunities")
        if not df_26ghz_filtered.empty:
            top_26ghz = df_26ghz_filtered.nlargest(10, '26GHz')[['State', '26GHz']]
            st.dataframe(top_26ghz, use_container_width=True)
        else:
            st.write("No states have 26 GHz spectrum available.")

elif page == "State-wise Comparison":
    st.header("🗺️ State-wise Spectrum Comparison")
    
    # Get all unique states from all dataframes
    all_states = []
    all_states.extend(df_800['State'].tolist())
    all_states.extend(df_900['State'].tolist())
    all_states.extend(df_1800['State'].tolist())
    all_states.extend(df_high['State'].tolist())
    all_states = sorted(list(set(all_states)))
    
    # State selection with no default selection
    selected_states = st.multiselect("Select States for Comparison", 
                                    all_states,
                                    default=[])
    
    if selected_states:
        # Create comprehensive merged dataframe
        comparison_data = []
        
        for state in selected_states:
            state_data = {'State': state}
            
            # 800 MHz data
            state_800 = df_800[df_800['State'] == state]
            state_data['800MHz'] = state_800['Quantum_800MHz'].iloc[0] if not state_800.empty else 0
            
            # 900 MHz data
            state_900 = df_900[df_900['State'] == state]
            state_data['900MHz'] = state_900['Quantum_900MHz'].iloc[0] if not state_900.empty else 0
            
            # 1800 MHz data
            state_1800 = df_1800[df_1800['State'] == state]
            state_data['1800MHz'] = state_1800['Quantum_1800MHz'].iloc[0] if not state_1800.empty else 0
            
            # High frequency data
            state_high = df_high[df_high['State'] == state]
            if not state_high.empty:
                state_data['2100MHz'] = state_high['2100MHz'].iloc[0]
                state_data['2300MHz'] = state_high['2300MHz'].iloc[0]
                state_data['2500MHz'] = state_high['2500MHz'].iloc[0]
                state_data['3300MHz'] = state_high['3300MHz'].iloc[0]
                state_data['26GHz'] = state_high['26GHz'].iloc[0]
            else:
                state_data['2100MHz'] = 0
                state_data['2300MHz'] = 0
                state_data['2500MHz'] = 0
                state_data['3300MHz'] = 0
                state_data['26GHz'] = 0
            
            comparison_data.append(state_data)
        
        df_comparison = pd.DataFrame(comparison_data)
        
        # Stacked bar chart for all bands
        fig_stacked = go.Figure()
        
        bands = ['800MHz', '900MHz', '1800MHz', '2100MHz', '2300MHz', '2500MHz', '3300MHz', '26GHz']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD']
        
        for i, band in enumerate(bands):
            if band in df_comparison.columns:
                fig_stacked.add_trace(go.Bar(
                    name=f'{band}', 
                    x=df_comparison['State'], 
                    y=df_comparison[band],
                    marker_color=colors[i]
                ))
        
        fig_stacked.update_layout(
            barmode='stack', 
            title='Total Spectrum Comparison by State (All Bands)',
            xaxis_title='State',
            yaxis_title='Spectrum (MHz)',
            height=500
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
        # Detailed comparison table
        st.subheader("Detailed Spectrum Comparison")
        
        # Calculate total spectrum (excluding 26 GHz for readability)
        df_comparison['Total_Low_Mid'] = (df_comparison['800MHz'] + 
                                         df_comparison['900MHz'] + 
                                         df_comparison['1800MHz'] + 
                                         df_comparison['2100MHz'] + 
                                         df_comparison['2300MHz'] + 
                                         df_comparison['2500MHz'] + 
                                         df_comparison['3300MHz'])
        
        comparison_table = df_comparison[['State', '800MHz', '900MHz', '1800MHz', '2100MHz', 
                                        '2300MHz', '2500MHz', '3300MHz', '26GHz', 'Total_Low_Mid']]
        comparison_table.columns = ['State', '800 MHz', '900 MHz', '1800 MHz', '2100 MHz', 
                                  '2300 MHz', '2500 MHz', '3300 MHz', '26 GHz', 'Total (MHz)']
        
        st.dataframe(comparison_table, use_container_width=True)
        
        # Market share analysis
        st.subheader("Market Share Analysis")
        
        total_available = comparison_table['Total (MHz)'].sum()
        if total_available > 0:
            comparison_table['Market Share %'] = (comparison_table['Total (MHz)'] / total_available * 100).round(2)
            
            fig_pie_states = px.pie(comparison_table, values='Total (MHz)', names='State',
                                   title=f"Market Share Among Selected States (Excluding 26 GHz)")
            st.plotly_chart(fig_pie_states, use_container_width=True)
    else:
        st.info("Please select states to compare their spectrum allocations.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    📡 Spectrum Auction Dashboard 2023-24 | Strategic Decision Support Tool | Network Planning & Strategy - Vi™
</div>
""", unsafe_allow_html=True)
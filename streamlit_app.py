import streamlit as st
from visitor_guide import TorontoVisitorGuide
import matplotlib.pyplot as plt
import plotly.express as px  # For interactive charts

def create_app():
    st.title("Toronto Taylor Swift Concert Visitor Guide")
    
    guide = TorontoVisitorGuide()
    
    # Define region data
    region_data = {
        "ON1 (Windsor/London)": 4,
        "ON2 (Kitchener/Waterloo)": 5,
        "ON3 (Kingston/Ottawa)": 8,
        "ON4 (Barrie/North)": 9
    }
    
    # Sidebar for user inputs
    st.sidebar.header("Your Information")
    
    # Region selection
    origin_region = st.sidebar.selectbox(
        "Where are you coming from?",
        list(region_data.keys())
    )

    arrival_info = guide.get_arrival_recommendation(origin_region[:3])
    
    transport_method = st.sidebar.selectbox(
        "How are you planning to get to Toronto?",
        ["Car", "Subway", "Other"]  # Removed Bus option
    )
    
    # Get default hours based on selected region
    default_hours = region_data[origin_region]
    
    # Hours slider with default value from region
    free_time = st.sidebar.slider(
        "How many hours do you have for sightseeing?",
        0, 12, default_hours,
        help="Default time is based on your location, but you can adjust if needed"
    )
    
    # Add note about suggested hours
    st.sidebar.info(f"💡 Based on data, visitors from {origin_region} typically have {default_hours} hours for sightseeing")
    
    # Main content
    st.header("Your Personalized Guide")
    
    # Arrival recommendations with highlighted time
    st.subheader("📅 Arrival Planning")
    if arrival_info['recommended_arrival_time']:
        col1, col2 = st.columns([1.5, 3])
        with col1:
            st.write("**Recommended Arrival Time:**")
        with col2:
            st.markdown(f"<span style='background-color: #ffeb3b; padding: 2px 8px; border-radius: 4px; font-weight: bold; color: black;'>{arrival_info['recommended_arrival_time'].strftime('%I:%M %p')}</span>", unsafe_allow_html=True)
        
        st.write(f"**Why this time?** {arrival_info['reason']}")

    # If subway is selected, show additional information
    if transport_method == "Subway":
        st.subheader("🚇 Subway Traffic Information")
        
        # Create two columns for better layout
        col1, col2 = st.columns([3,2])
        
        with col1:
            st.write("**Peak Traffic Hours to Avoid:**")
            peak_hours = {
                "ON1": "5:00 PM (17:00)",
                "ON2": "4:00 PM (16:00)",
                "ON3": "1:00 PM (13:00)",
                "ON4": "12:00 PM (12:00)"
            }
            
            selected_region = origin_region[:3]  # Get ON1, ON2, etc.
            peak_time = peak_hours.get(selected_region, "Data not available")
            
            st.warning(f"⚠️ Highest subway traffic from your region is typically around {peak_time}")
            
            st.write("""
            **Tips for Subway Travel:**
            - Consider traveling 30-60 minutes before the peak time
            - Have your transit fare ready before entering the station
            - Follow TTC updates for service changes
            - Consider using alternate stations if your nearest one is busy
            """)
        
        with col2:
            st.info(f"""
            **Your Region ({selected_region}):**
            - Peak Traffic: {peak_time}
            - Recommended Arrival: {int(peak_hours[selected_region].split(':')[0]) - 1}:00
            - Average Travel Time to Core: ~{arrival_info['free_hours']} hours
            """)

    # Tourist suggestions
    st.subheader("🎯 Suggested Itinerary")
    suggestions = guide.get_tourist_suggestions(free_time)
    st.write(f"**Plan Type:** {suggestions['description']}")

    # Display activities in a more organized way
    st.write("**Recommended Activities:**")
    for activity in suggestions['activities']:
        with st.container():
            st.markdown("""---""")
            col1, col2 = st.columns([2,3])
            
            with col1:
                st.subheader(activity['name'])
                st.write(f"⏱️ **Duration:** {activity['duration']}")
                st.write(f"🏷️ **Type:** {activity['type']}")
                
            with col2:
                st.write("**About:**")
                st.write(activity['description'])

    # Add estimated total time
    total_hours = sum(float(activity['duration'].split()[0]) for activity in suggestions['activities'])
    st.markdown("""---""")
    st.write(f"⏰ **Total Time Needed:** Approximately {total_hours} hours")

    # Tips and warnings
    st.subheader("⚠️ Important Tips")
    st.write("""
    - Arrive early to avoid long queues
    - Have your tickets ready on your phone
    - Bring water and snacks
    - Check the weather forecast
    - Consider using public transit to avoid parking issues
    """)

    # Add transportation tips based on origin
    st.subheader("🚗 Getting Around")
    transport_tips = {
        "ON1": "Consider taking the UP Express from Pearson Airport or driving to a subway station and using TTC.",
        "ON2": "GO Transit offers regular service to Union Station. Consider the GO Train for convenience.",
        "ON3": "VIA Rail connects to Union Station. The GO Train is also available from some locations.",
        "ON4": "GO Transit's Barrie line provides direct access to downtown. Consider parking at a GO station."
    }
    st.write(transport_tips.get(origin_region[:3], "Use public transit to avoid downtown parking challenges."))

if __name__ == "__main__":
    create_app()
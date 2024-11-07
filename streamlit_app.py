import streamlit as st
from visitor_guide import TorontoVisitorGuide

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
    
    # Arrival recommendations
    st.subheader("📅 Arrival Planning")
    arrival_info = guide.get_arrival_recommendation(origin_region[:3])
    if arrival_info['recommended_arrival_time']:
        st.write(f"**Recommended Arrival Time:** {arrival_info['recommended_arrival_time'].strftime('%I:%M %p')}")
        st.write(f"**Why this time?** {arrival_info['reason']}")
    
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
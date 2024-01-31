import streamlit as st
from usellm import UseLLM, Message, Options
from utils import TOUR_GUIDE_SYSTEM, TRIP_PLANNER_SYSTEM

# Add Streamlit Components import
import streamlit.components.v1 as components

# Initialize LLM service
service = UseLLM(service_url="https://usellm.org/api/llm")

# Add styles and settings here
st.set_page_config(page_title="Travel and Tourism", page_icon="✈️")

# Add a background image using st.image
background_image = "https://unsplash.com/photos/jetski-on-body-of-water-MA8YoAoKpfY"
st.markdown(
    f"""
    <style>
    
        .stApp {{
            background-image: url("{background_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        body {{
            margin: 0;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Create a function for the image carousel
def image_carousel():
    images = ["img/banner1.jpg", "img/banner2.jpg", "img/banner3.jpg"]
    components.html(
        f"""
        <div  id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
                {"".join(f'<div style="margin-top:-100px; margin-left:-100px;" class="carousel-item {"active" if i==0 else ""}">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img width="850px" src="https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg?cs=srgb&dl=pexels-james-wheeler-414612.jpg&fm=jpg" class="d-block w-100" alt="..."></div>' for i, img in enumerate(images))}
            </div>
        </div>
        <script>
            setInterval(function() {{
                $('#carouselExampleControls').carousel('next');
            }}, 4000);
        </script>
        """,
        height=400,
    )

# Create a function for the client testimonials with circular images
def client_testimonials():
    testimonials = [
        {"name": "John Doe", "comment": "Amazing travel experience with excellent service!"},
        {"name": "Jane Smith", "comment": "Highly recommended for trip planning. They make it stress-free!" },
        {"name": "Bob Johnson", "comment": "Professional and friendly. Will use their services again."}, 
        {"name": "Emily White", "comment": "Best travel agency! They exceeded my expectations."},
    ]

    for testimonial in testimonials:
      
        st.write(f"**{testimonial['name']}**: {testimonial['comment']}")
        st.write("---")

# Add styles
st.markdown(
    """
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        nav {
            background-color: #034f84;
            padding: 15px 20px;
            color: #fff;
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }
        .logo a {
            color: #fff;
            font-size: 28px;
            font-weight: bold;
            text-decoration: none;
        }
        .nav-links a {
            color: #fff;
            margin: 0 20px;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease-in-out;
        }
        .nav-links a:hover {
            color: #ffd700;
        }
        .footer {
            background-color: #034f84;
            color: #fff;
            padding: 20px;
            text-align: center;
            width: 100%;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set the title and icon
st.title("Ultra travels")

# Create the main function
def main():
    # Create a navbar
    st.markdown("<nav><div class='nav-links'><a href='#'>Home</a><a href='#'>Tour Guide</a><a href='#'>Trip Planner</a><a href='#'>About Us</a><a href='#'>Testimonials</a></div></nav>", unsafe_allow_html=True)

    # Create a sidebar for page selection
    page = st.sidebar.selectbox("Select Page", ["Home", "Tour Guide", "Trip Planner", "About Us", "Client Testimonials", "Contact Us"])

    if page == "Home":
        st.title("Welcome to our Travel and Tourism Website!")
        image_carousel()
        st.write("Explore the beauty of different destinations with us.")
        st.write("Plan your trip, get recommendations, and make your travel memorable.")

    elif page == "Tour Guide":
        st.title("Tour Guide Assistant")
        user_input = st.text_input("Enter the Place You Want to Visit", key="input1")
        if st.button("Send", key="button1"): 
            if user_input:
                output = get_response(TOUR_GUIDE_SYSTEM, user_input)
                show(output)
            else:
                st.markdown("Please Enter Some Text")

    elif page == "Trip Planner":
        st.title("Personal Trip Planner")
        user_input = st.text_input("Enter the Place You Want to Visit", key="input2")
        days = st.number_input("Enter the Number of Days", min_value=1, key="input3")
        budget = st.number_input("Enter Your Budget (INR)", min_value=0, key="input4")  
        if st.button("Send", key="button2"): 
            if user_input and days and budget:
                trip_planner_system = TRIP_PLANNER_SYSTEM.format(days, budget)
                output = get_response(trip_planner_system, user_input)
                show(output)
            else:
                st.markdown("Please Enter Valid Inputs")

    elif page == "About Us":
        st.title("About Us")
        st.write("Welcome to our Travel and Tourism platform! We are dedicated to providing you with the best travel experiences.")
        st.write("Our team is committed to making your journey memorable.")

    elif page == "Client Testimonials":
        st.title("Client Testimonials")
        client_testimonials()

    elif page == "Contact Us":
        st.title("Contact Us")
        st.write("Feel free to reach out to us for any inquiries or assistance.")
        st.write("Email: info@mytravelagency.com")
        st.write("Phone: 1-800-123-4567")

    # Create a footer
    st.markdown("<div class='footer'>Contact: info@mytravelagency.com | Phone: 1-800-123-4567</div>", unsafe_allow_html=True)

# Function to interact with LLM
def get_response(system_message, user_input):
    messages = [
        Message(role="system", content=system_message),
        Message(role="user", content=user_input)
    ]
    options = Options(messages=messages)
    output = service.chat(options)
    return output

# Function to display LLM response
def show(output):
    if output:
        st.markdown(output.content)

# Run the main function
if __name__ == "__main__":
    main()

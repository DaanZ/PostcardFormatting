
import streamlit as st

from history import History
from streaming import streaming_interface

postcard_system_message = """
Chicago Real Estate Marketing Plan
1. Understand Your Target Audience
Segment your audience: Focus on specific groups like first-time homebuyers, luxury property seekers, or investors.
Highlight local expertise: Chicago neighborhoods vary greatly. Mention areas like Lincoln Park, Wicker Park, or Gold Coast to connect with your audience.
Incorporate data: Use statistics such as average home prices or growth trends in specific neighborhoods.
2. Craft a Strong Headline
Use attention-grabbing phrases relevant to the Chicago market:
“Your Dream Home in Lincoln Park Awaits!”
“Thinking of Selling in River North? Let’s Maximize Your Return!”
“Exclusive Chicago Properties—Don’t Miss Out!”
3. Showcase Your Value Proposition
Highlight unique selling points:
“Free home valuation in Chicago—find out what your property is worth!”
“Access exclusive Chicago listings before they hit the market!”
Demonstrate credibility: Mention credentials, such as being a top agent in Chicago or a track record of fast sales.
4. Incorporate Visuals
Use high-quality images of iconic Chicago landmarks like Millennium Park, Willis Tower, or Lake Michigan.
Showcase properties you’ve sold or listed, featuring both interiors and exteriors.
Use a clean, branded layout with your logo and colors for consistency.
5. Add a Clear Call-to-Action (CTA)
Include a compelling action step:
“Call [Phone Number] for a Free Consultation.”
“Scan this QR Code for Chicago’s Latest Listings.”
“Visit [Website] to Find Your Chicago Home.”
“Text ‘HOME’ to [Number] for Instant Updates.”
6. Leverage Testimonials and Local Success Stories
Feature client quotes like:
“John helped us sell our Wicker Park condo in just 7 days!”
Highlight success metrics:
“Sold for 10% over asking price in Bucktown!”
7. Provide a Limited-Time Offer
Create urgency to spur action:
“List by [Date] and Save $500 on Closing Costs.”
“First 5 consultations this month are FREE—don’t wait!”
8. Tailor to the Season
Winter: Highlight cozy homes or Chicago’s snowy skyline.
Summer: Showcase outdoor spaces and proximity to beaches.
Spring/Fall: Emphasize moving seasons and the appeal of seasonal property markets.
9. Ensure Easy Contact Options
Include phone number, email, website, and social media handles.
Add a QR code or scheduling link to simplify next steps.
10. Print and Distribution Tips
Use thick, glossy cardstock for a premium feel.
Partner with local businesses or cafés to distribute postcards.
Target high-traffic neighborhoods with direct mail campaigns using zip code targeting.
Sample Messaging for a Chicago Real Estate Postcard
Front:
🏠 Your Chicago Home Expert is Here! 🏙
“Thinking of Buying or Selling in Wicker Park? Let’s Talk!”

Back:
Hi, I’m [Your Name], a real estate expert specializing in Chicago neighborhoods like Lincoln Park, Bucktown, and Lakeview.

📞 Call today for a FREE home valuation: [Your Number]
📱 Scan the QR code for exclusive Chicago listings.
🔑 Let’s make your real estate goals a reality!
"""


def postcard_front(image_path: str, container_height: int = 400, container_width: int = 600):
    # Allow user to upload or use the default image
    with st.container(border=True):
        st.image(image_path)


def postcard_text(container_height: int = 400, container_width: int = 600):
    # Set the height of the panel
    padding_proportion = 0.1  # Padding proportion (10%)
    font_size_proportion = 0.05  # Font size proportion relative to height
    stamp_size_proportion = 0.2  # Stamp size as a proportion of the container height
    stamp_margin_proportion = 0.05  # Margin around the stamp as a proportion of the container height

    # Calculated values
    padding_left = container_height * padding_proportion
    text_size = int(container_height * font_size_proportion)
    stamp_size = container_height * stamp_size_proportion
    stamp_margin = container_height * stamp_margin_proportion

    with st.container(border=True):
        # Create two columns
        col1, col2 = st.columns([6, 4])  # Adjusted width ratios for left margin

        # Left column with a margin for the message input
        with col1:
            message_component = st.text_area(
                "",
                st.session_state.postcard_message,
                height=container_height,
                max_chars=1000,
                label_visibility="collapsed"
            )

            if message_component:
                st.session_state.postcard_message = message_component


        # Right column with rows for the stamp and address input
        with col2:
            # Row 1: Placeholder for the stamp
            with st.container():
                st.html(
                    f"""
                            <div style="position: relative; height: {stamp_size + 2 * stamp_margin}px;">
                                <div style="position: absolute; top: {stamp_margin}px; right: {stamp_margin}px; 
                                border: 1px solid grey; height: {stamp_size}px; width: {stamp_size}px; 
                                text-align: center; line-height: {stamp_size}px;">
                                    STAMP
                                </div>
                            </div>
                            """
                )

            # Row 2: Address text input
            address_component = st.text_area(
                "",
                st.session_state.postcard_address,
                height=container_height // 2,
                max_chars=500,
                label_visibility="collapsed"
            )



if __name__ == "__main__":
    # Text data
    message_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    address_text = """John Doe  
1234 W Maple Avenue  
Apt 5B  
Chicago, IL 60611  
USA"""

    st.set_page_config(
        page_title="Click2Mail",
        page_icon="✉️",
        layout="wide"
    )

    if 'postcard_message' not in st.session_state:
        st.session_state.postcard_message = message_text

    if 'postcard_address' not in st.session_state:
        st.session_state.postcard_address = address_text

    if 'postcard_image_path' not in st.session_state:
        st.session_state.postcard_image_path = "images/house.png"

    col1, col2 = st.columns(2)
    with col1:
        st.title("Click2Mail: Postcards")

    with col2:
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            st.session_state.postcard_image_path = uploaded_image

    col1, col2 = st.columns(2)
    height = 300
    width = int(height * 210 / 148)

    if 'history' not in st.session_state:
        st.session_state.history = History()
        st.session_state.history.system(postcard_system_message)
        st.session_state.history.assistant("How can I help you today?")

    with col1:
        with st.container(border=True, height=int(height*2.5)):
            streaming_interface()

    with col2:
        postcard_front(st.session_state.postcard_image_path, height, width)
        postcard_text(height, width)

        st.button("Generate Postcard")


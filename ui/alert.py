import streamlit as st
import api.alert as alert

"""
class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    alert_type = Column(String, nullable=False)
    creation_times = relationship("AlertTime", back_populates="alert")
    location = relationship("Location", back_populates="alerts")
    user = relationship("User", back_populates="alerts")
"""


def create_alert():
    with st.form("create_alert"):
        st.title("Create Alert")
        title = st.text_input("Title", value=None)
        description = st.text_area("Description", value=None)
        alert_type = st.selectbox(
            "Alert Type",
            ["Fire", "Flood", "Earthquake", "Tornado", "Tsunami"],
            index=None,
        )
        if st.form_submit_button("Submit"):
            st.success("Alert Created!")


def edit_alert():
    pass


def delete_alert():
    pass


def all_alerts():
    pass

import re
import dns.resolver
import streamlit as st


def is_valid_email_format(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None


def is_valid_password(password):
    if len(password) < 8:
        st.error("Password must be at least 8 characters long.")
        return False
    elif not any(char.isupper() for char in password):
        st.error("Password must contain at least one uppercase letter.")
        return False
    elif not any(char.isdigit() for char in password):
        st.error("Password must contain at least one digit.")
        return False
    elif not any(char in "!@#$%^&*()-+" for char in password):
        st.error("Password must contain at least one special character.")
        return False
    return True


def is_valid_email(email):
    if not is_valid_email_format(email):
        return False
    try:
        # dont know what i'm doing, but works then fine for me
        domain = email.split("@")[1]
        mx_records = dns.resolver.resolve(domain, "MX")
        return bool(mx_records)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

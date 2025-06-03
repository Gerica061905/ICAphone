import streamlit as st
import re
import math
import io

st.set_page_config(page_title="ICAPhone", layout="centered")
st.title("📱 ICAPhone")
st.markdown("""
Enter any phone numbers below. This app will:
- Clean and format them to **+63 format**
- Group them into batches of **50** (48 middle + your 1st and 50th number)
- Allow you to **download** the output as a `.txt` file
""")

# --- Formatting function ---
def format_number(number):
    number = str(number).strip()
    number = ''.join(filter(str.isdigit, number))
    if number.startswith('63') and len(number) == 11:
        number = '639' + number[2:]
    if len(number) == 9 and not number.startswith('9'):
        number = '9' + number
    if len(number) == 10 and number.startswith('9'):
        number = '63' + number
    if number.startswith('63') and len(number) == 12:
        return '+' + number
    return None

# --- User Inputs ---
input_text = st.text_area("Enter phone numbers (any format):", height=200)
batch_name = st.text_input("(Optional) Batch Name:")
first_number = st.text_input("1st number:")
fiftieth_number = st.text_input("50th number:")
file_name = st.text_input("file name:", value="output")

if st.button("🚀 Process Numbers"):
    if not input_text.strip():
        st.warning("Please enter phone numbers to process.")
    elif not first_number or not fiftieth_number:
        st.warning("You must enter both the 1st and 50th numbers.")
    else:
        raw_numbers = re.findall(r"\+?\d{10,13}", input_text)
        formatted_numbers = [format_number(n) for n in raw_numbers]
        formatted_numbers = [n for n in formatted_numbers if n]
        formatted_numbers = list(dict.fromkeys(formatted_numbers))

        first_number_fmt = format_number(first_number)
        fiftieth_number_fmt = format_number(fiftieth_number)

        if not first_number_fmt or not fiftieth_number_fmt:
            st.error("Invalid format for 1st or 50th number.")
        else:
            batch_size = 48
            max_batches = 200
            total_batches = min(max_batches, math.ceil(len(formatted_numbers) / batch_size))

            if total_batches == 0:
                st.info("You need at least 1 number to make a batch.")
            else:
                output_lines = []
                for i in range(total_batches):
                    start = i * batch_size
                    end = min(start + batch_size, len(formatted_numbers))
                    middle_48 = formatted_numbers[start:end]
                    batch = [first_number_fmt] + middle_48 + [fiftieth_number_fmt]
                    if batch_name:
    output_lines.append(f"{batch_name} Batch {i+1}:")
else:
    output_lines.append(f"Batch {i+1}:")
output_lines.extend(batch)
output_lines.append("")  # Blank line between batches


                output_str = "\n".join(output_lines)
                st.success(f"Generated {total_batches} batch(es).")
                st.text_area("📋 Output Preview:", value=output_str, height=300)

                # Download as text file
                download_file = io.StringIO(output_str)
                st.download_button(
                    label="📥 Download .txt",
                    data=download_file.getvalue(),
                    file_name=f"{file_name.strip()}({total_batches}x).txt",
                    mime="text/plain"
                )

import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="HR Data Management System", layout="wide")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "employees" not in st.session_state:
    st.session_state.employees = pd.DataFrame([
        {"Employee ID": 101, "Name": "Arun", "Department": "HR", "Gender": "Male", "Mobile": "9876543201", "Attendance (%)": 92},
        {"Employee ID": 102, "Name": "Divya", "Department": "Production", "Gender": "Female", "Mobile": "9876543202", "Attendance (%)": 88},
        {"Employee ID": 103, "Name": "Karthik", "Department": "HR", "Gender": "Male", "Mobile": "9876543203", "Attendance (%)": 95},
        {"Employee ID": 104, "Name": "Meena", "Department": "Finance", "Gender": "Female", "Mobile": "9876543204", "Attendance (%)": 90},
        {"Employee ID": 105, "Name": "Ravi", "Department": "Production", "Gender": "Male", "Mobile": "9876543205", "Attendance (%)": 85},
        {"Employee ID": 106, "Name": "Suresh", "Department": "HR", "Gender": "Male", "Mobile": "9876543206", "Attendance (%)": 91},
        {"Employee ID": 107, "Name": "Anitha", "Department": "Finance", "Gender": "Female", "Mobile": "9876543207", "Attendance (%)": 93},
        {"Employee ID": 108, "Name": "Prakash", "Department": "Maintenance", "Gender": "Male", "Mobile": "9876543208", "Attendance (%)": 87},
        {"Employee ID": 109, "Name": "Kavya", "Department": "HR", "Gender": "Female", "Mobile": "9876543209", "Attendance (%)": 96},
        {"Employee ID": 110, "Name": "Vijay", "Department": "Production", "Gender": "Male", "Mobile": "9876543210", "Attendance (%)": 89},
        {"Employee ID": 111, "Name": "Swathi", "Department": "Finance", "Gender": "Female", "Mobile": "9876543211", "Attendance (%)": 94},
        {"Employee ID": 112, "Name": "Naveen", "Department": "Maintenance", "Gender": "Male", "Mobile": "9876543212", "Attendance (%)": 86},
        {"Employee ID": 113, "Name": "Priya", "Department": "HR", "Gender": "Female", "Mobile": "9876543213", "Attendance (%)": 97},
        {"Employee ID": 114, "Name": "Ashok", "Department": "Production", "Gender": "Male", "Mobile": "9876543214", "Attendance (%)": 84},
        {"Employee ID": 115, "Name": "Ramya", "Department": "Finance", "Gender": "Female", "Mobile": "9876543215", "Attendance (%)": 92},
        {"Employee ID": 116, "Name": "Manoj", "Department": "HR", "Gender": "Male", "Mobile": "9876543216", "Attendance (%)": 90},
        {"Employee ID": 117, "Name": "Deepa", "Department": "Maintenance", "Gender": "Female", "Mobile": "9876543217", "Attendance (%)": 88},
        {"Employee ID": 118, "Name": "Ramesh", "Department": "Production", "Gender": "Male", "Mobile": "9876543218", "Attendance (%)": 91},
        {"Employee ID": 119, "Name": "Lakshmi", "Department": "Finance", "Gender": "Female", "Mobile": "9876543219", "Attendance (%)": 95},
        {"Employee ID": 120, "Name": "Senthil", "Department": "Maintenance", "Gender": "Male", "Mobile": "9876543220", "Attendance (%)": 89},
    ])

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.markdown("<h1 style='text-align:center;color:#1F618D;'>HR Management Login</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.markdown("<h1 style='text-align:center;color:#2E86C1;'>HR Data Management Dashboard</h1>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = st.session_state.employees

    # -------- SIDEBAR FILTERS --------
    st.sidebar.markdown("### 🔍 HR Filters")

    dept = st.sidebar.selectbox("Department", ["All"] + list(df["Department"].unique()))
    gender = st.sidebar.selectbox("Gender", ["All"] + list(df["Gender"].unique()))

    filtered_df = df.copy()
    if dept != "All":
        filtered_df = filtered_df[filtered_df["Department"] == dept]
    if gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]

    # -------- SEARCH --------
    st.sidebar.markdown("### 🔎 Search Employee")
    search_id = st.sidebar.text_input("Employee ID")

    if search_id:
        if search_id.isdigit():
            temp = filtered_df[filtered_df["Employee ID"] == int(search_id)]
            if temp.empty:
                st.warning("❌ Employee Not Found")
            else:
                st.success("✅ Employee Found")
                filtered_df = temp
        else:
            st.warning("⚠ Enter numeric ID")

    # -------- TABLE --------
    st.markdown("### 👨‍💼 Employee Records")
    st.dataframe(filtered_df, use_container_width=True)

    # -------- ADD EMPLOYEE --------
    st.markdown("### ➕ Add Employee")
    with st.form("add"):
        eid = st.number_input("Employee ID", step=1)
        name = st.text_input("Name")
        dept_new = st.selectbox("Department", ["HR", "Production", "Finance", "Maintenance"])
        gender_new = st.selectbox("Gender", ["Male", "Female"])
        mobile = st.text_input("Mobile Number")
        attendance = st.slider("Attendance (%)", 0, 100)

        if st.form_submit_button("Add"):
            if eid in df["Employee ID"].values:
                st.error("Employee ID already exists")
            else:
                st.session_state.employees = pd.concat(
                    [df, pd.DataFrame([{
                        "Employee ID": int(eid),
                        "Name": name,
                        "Department": dept_new,
                        "Gender": gender_new,
                        "Mobile": mobile,
                        "Attendance (%)": attendance
                    }])],
                    ignore_index=True
                )
                st.success("Employee Added")
                st.rerun()

    # -------- UPDATE EMPLOYEE --------
    st.markdown("### ✏ Update Employee")
    uid = st.number_input("Employee ID to Update", step=1)

    if uid in df["Employee ID"].values:
        row = df[df["Employee ID"] == uid].iloc[0]

        new_name = st.text_input("Name", row["Name"])
        new_mobile = st.text_input("Mobile", row["Mobile"])
        new_dept = st.selectbox("Department", ["HR", "Production", "Finance", "Maintenance"], index=["HR","Production","Finance","Maintenance"].index(row["Department"]))
        new_gender = st.selectbox("Gender", ["Male", "Female"], index=["Male","Female"].index(row["Gender"]))
        new_att = st.slider("Attendance (%)", 0, 100, row["Attendance (%)"])

        if st.button("Update"):
            st.session_state.employees.loc[df["Employee ID"] == uid, ["Name","Mobile","Department","Gender","Attendance (%)"]] = [
                new_name, new_mobile, new_dept, new_gender, new_att
            ]
            st.success("Employee Updated Successfully")
            st.rerun()

    # -------- DELETE EMPLOYEE --------
    st.markdown("### 🗑 Delete Employee")
    did = st.number_input("Employee ID to Delete", step=1)

    if st.button("Delete"):
        if did in df["Employee ID"].values:
            st.session_state.employees = df[df["Employee ID"] != did]
            st.success("Employee Deleted")
            st.rerun()
        else:
            st.error("Employee ID not found")

    # -------- CHART --------
    st.markdown("### 📊 Department-wise Employee Count")
    st.bar_chart(st.session_state.employees["Department"].value_counts())

# ---------------- MAIN ----------------
if st.session_state.logged_in:
    dashboard()
else:
    login_page()

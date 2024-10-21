from datetime import datetime

import pandas as pd
import streamlit as st

from src.utils.mongodb import delete_one, find, insert_many, insert_one

st.session_state.data = find()

st.set_page_config(page_title="Sales UON", layout="wide")

st.title("Sales UON")

with st.expander("Upload CSV file", expanded=False):
    csv = st.file_uploader("Sales Files", type="csv")
    if csv:
        st.subheader("Preview")
        sales_data = pd.read_csv(csv, delimiter=";")
        st.dataframe(sales_data.head(), use_container_width=True)
        if st.button("Upload Data", use_container_width=True):
            result = insert_many(sales_data.to_dict("records"))
            if result:
                st.success("Successfully Uploaded Data")

with st.popover("Add Vehicle Sale", use_container_width=True):
    make = st.text_input("Make")
    model = st.text_input("Model")
    vin = st.number_input("VIN", step=1, min_value=1)
    sale_date = st.date_input("Sale Date", max_value=datetime.now())
    # if st.button("Submit"):
    if not make and model and vin and sale_date:
        st.error("Please Enter The Vehicle Sale Data")
    vin_is_unique = bool(find({"VIN": vin}))
    if vin_is_unique:
        st.error("VIN is already in use, please enter a unique vin.".upper())
    if st.button("Submit", use_container_width=True, disabled=vin_is_unique):
        data = {
            "Make": make,
            "Model": model,
            "VIN": vin,
            "SaleDate": sale_date.strftime("%d/%m/%Y"),
        }
        st.session_state.data.append(data)
        insert_one(data)

if st.session_state.data:
    st.subheader("Sales Data")
    makes = st.multiselect(
        "Filter by Make",
        set([make["Make"] for make in st.session_state.data]),
        key="filter_by_make",
    )

    query = {}
    if makes:
        query["Make"] = {"$in": makes}

    data = find(query)
    if data:
        st.session_state.data = data

    selected_values = st.dataframe(
        st.session_state.data,
        use_container_width=True,
        column_order=["Make", "Model", "VIN", "SaleDate"],
        selection_mode="multi-row",
        on_select="rerun",
    )

    if selected_values:
        st.subheader("Selected Entries")
        vehicles = []
        for value in selected_values["selection"]["rows"]:
            vehicle = st.session_state.data[value]
            vehicles
            with st.expander(
                f"{vehicle["Make"]} {vehicle["Model"]} {vehicle["VIN"]} {vehicle["SaleDate"]}"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    with st.popover("Edit", use_container_width=True):
                        make = st.text_input(
                            "Make",
                            value=vehicle["Make"],
                            key=f"edit_{vehicle["VIN"]}_make",
                        )
                        model = st.text_input(
                            "Model",
                            value=vehicle["Model"],
                            key=f"edit_{vehicle["VIN"]}_model",
                        )
                        vin = st.number_input(
                            "VIN",
                            value=vehicle["VIN"],
                            step=1,
                        )
                        sale_date = st.date_input(
                            "Sale Date",
                            value=datetime.strptime(vehicle["SaleDate"], "%d/%m/%Y"),
                        )
                with col2:
                    with st.popover("Delete", use_container_width=True):
                        if st.button(
                            "Confirm",
                            key=f"delete_{vehicle["VIN"]}",
                            use_container_width=True,
                        ):
                            delete_one({"VIN": vehicle["VIN"]})

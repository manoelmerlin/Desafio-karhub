import pandas as pd
import uuid

normalized_data = []

a_car_list = pd.read_excel(r"default_files/a_list_car_model_standard_meli.xlsx")

df = pd.DataFrame(a_car_list, columns=["maker", "model", "year", "version"],)

all_car_makers = df[df["maker"].str.contains(" ")]["maker"].unique()

for i in range(len(a_car_list)):
    normalized_data.append({
        "maker":a_car_list["maker"][i],
        "model": a_car_list["model"][i],
        "year": a_car_list["year"][i],
        "version": str(a_car_list["version"][i]),
    })

b_car_list = pd.read_excel(r"default_files/b_list_cp_application_complete.xlsx")

application_data = pd.DataFrame(b_car_list, columns=["application_start"])

car_names_to_not_capitalize = ["SEAT", "KIA", "MERCEDES-BENZ", "CITROEN",]

car_name_with_especial_treat = {
    "CITROEN": "Citroën",
    "MERCEDES-BENZ": "Mercedes-Benz",
}

for value in application_data["application_start"]:
    if isinstance(value, str) and "@#" in value:
        car_info = value.split("@#")

        car_splited_info = car_info[0].split(" ")

        car_name = car_splited_info[0]

        if len(car_name) > 3 and car_name not in car_names_to_not_capitalize:
            car_name = car_name.capitalize()

        if car_name in car_name_with_especial_treat:
            car_name = car_name_with_especial_treat[car_name]

        found = a_car_list[a_car_list["maker"] == car_name].any()

        data_to_append = {
            "maker": "",
            "model": "",
            "year": int(car_splited_info[len(car_splited_info) - 1]),
            "version": car_info[1],
        }

        if not found["maker"]:
            str_to_compare = car_name + " " + car_splited_info[1].capitalize()

            if str_to_compare in all_car_makers:
                data_to_append["maker"] = str_to_compare
                data_to_append["model"] = car_splited_info[2]
            else:
                data_to_append["maker"] = car_name
                data_to_append["model"] = car_splited_info[1]
        else:
            data_to_append["maker"] = car_name
            data_to_append["model"] = car_splited_info[1]

        if data_to_append not in normalized_data:
            normalized_data.append(data_to_append)

car_list_df = pd.DataFrame(normalized_data).\
    sort_values(["maker", "model", "year", "version"],)

car_list_df.to_excel(
    f"processed_files/car_model_{uuid.uuid4()}.xlsx",
    columns=["maker", "model", "year", "version"],
    index=False,
)

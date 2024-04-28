import streamlit as st
import requests
import os

# define the URL of the API
############################
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['local_api_uri']


## Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'

## display info about the URL we are using
st.write(f"Currently running on API: {BASE_URI}")


# ask user for input
#######################

## get the url from the user
with st.form("Enter url you want to analyze"):

    url_input = st.text_input("Enter the url of the website you want to analyse.")
    submitted_url = st.form_submit_button("Submit url")

if submitted_url:

    st.session_state["url"] = url_input
    st.write("Let's analyse the url: ", url_input)

## ask the user what informations to retrieve (max 3)
if len(url_input)>0:
    ## info no.1
    with st.form(f"Describe the information you want to retrieve. - No.1"):

        keyword_input_1 = st.text_input("What kind of information do you want to find? Use keywords only.")
        description_input_1 = st.text_input("Give a short description of that information.")
        submitted_info_1 = st.form_submit_button("Submit info 1")

    if submitted_info_1:

        st.session_state["keywords_1"] = keyword_input_1
        st.session_state["description_1"] = description_input_1
        st.write(f"Keywords no.1: ", keyword_input_1)
        st.write(f"Description no.1: ", description_input_1)


    if len(keyword_input_1)>0 and len(description_input_1)>0:
        ## info no.2
        with st.form(f"Describe the information you want to retrieve. - No.2"):

            keyword_input_2 = st.text_input("What kind of information do you want to find? Use keywords only.")
            description_input_2 = st.text_input("Give a short description of that information.")
            submitted_info_2 = st.form_submit_button("Submit info 2")

        if submitted_info_2:

            st.session_state["keywords_2"] = keyword_input_2
            st.session_state["description_2"] = description_input_2
            st.write(f"Keywords no.2: ", keyword_input_2)
            st.write(f"Description no.2: ", description_input_2)

        if len(keyword_input_2)>0 and len(description_input_2)>0:
            ## info no.3
            with st.form(f"Describe the information you want to retrieve. - No.3"):

                keyword_input_3 = st.text_input("What kind of information do you want to find? Use keywords only.")
                description_input_3 = st.text_input("Give a short description of that information.")
                submitted_info_3 = st.form_submit_button("Submit info 3")

            if submitted_info_3:

                st.session_state["keywords_3"] = keyword_input_3
                st.session_state["description_3"] = description_input_3
                st.write(f"Keywords no.3: ", keyword_input_3)
                st.write(f"Description no.3: ", description_input_3)


    # add button to start the analysis
    start_analysis = st.button("Start analysis")

    if start_analysis:
        ## The API endpoint to communicate with
        url_post = BASE_URI + "url-analysis"

        sought_data = {}
        if st.session_state.get("keywords_1") is not None and st.session_state.get("description_1") is not None:

            sought_data[st.session_state["keywords_1"]] = st.session_state["description_1"]
            if st.session_state.get("keywords_2") is not None and st.session_state.get("description_2") is not None:

                sought_data[st.session_state["keywords_2"]] = st.session_state["description_2"]
                if st.session_state.get("keywords_3") is not None and st.session_state.get("description_3") is not None:

                    sought_data[st.session_state["keywords_3"]] = st.session_state["description_3"]


        data = {
            "url" : st.session_state["url"],
            "sought_data" : sought_data
        }

        res = requests.post(url=url_post, json=data)

        if res.status_code == 200:

            res_json = res.json()
            res_body = res_json.get("extracted_data")

            if res_body is not None:

                for keyword, description in res_body.items():
                    st.write(f"Found info about {keyword}:")
                    st.write(description)

        else:
            st.markdown("<h3 style='text-align: center; color: #E73D53;'>Oops, something went wrong 😓 Please try again.</h3>", unsafe_allow_html=True)
            print(res.status_code, res.content)

# install packages
install_requirements:
	@pip install -r requirements.txt

# streamlit commands
streamlit_local:
	@API_URI=local_api_uri streamlit run front.py

streamlit_cloud:
	@API_URI=cloud_api_uri streamlit run front.py

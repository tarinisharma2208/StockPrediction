# Stock prediction — Streamlit deployment

Quick steps to deploy this app to Streamlit Community Cloud or run locally.

Deployment (Streamlit Community Cloud):
1. Push this `Stock prediction` folder to a GitHub repository.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, select the repository and branch, and set the main file path to `Stock prediction/app.py`.
4. Click **Deploy** — Streamlit will install dependencies from `Stock prediction/requirements.txt`.

Run locally:

```powershell
cd "C:\Users\Arya Singh\OneDrive\Desktop\Tarini\Stock prediction"
python -m pip install -r requirements.txt
streamlit run app.py
```

Notes:
- Ensure any required data files are present in the same folder if `app.py` reads them.
- If you need private data or secrets, use Streamlit's Secrets management.

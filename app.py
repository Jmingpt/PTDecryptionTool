import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def fernet_decrypt(key, encrypted_message):
    key = key.encode()
    cipher = Fernet(key)
    decrypted_message = cipher.decrypt(encrypted_message.encode())

    return decrypted_message.decode()


def run():
    st.set_page_config(
        page_title="Decryption Tool",
        page_icon="🔑"
    )
    st.title("Decryption Tool")

    with st.sidebar:
        key = st.text_input(
            label='Decryption Key',
            value=''
        )

    uploaded_file = st.file_uploader(
        label='Choose a CSV file',
        type='csv',
        accept_multiple_files=False
    )
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        cols = data.columns.tolist()

        if key != '':
            nonencrypt_cols = []
            for col in cols:
                if 'name' in col.lower() or 'email' in col.lower():
                    data[f'decrypted_{col}'] = data[col].apply(lambda x: fernet_decrypt(key, x))
                else:
                    nonencrypt_cols.append(col)

            result_cols = nonencrypt_cols + [c for c in data.columns if c.startswith('decrypted')]
            result = data[result_cols]
            result.columns = [c.lower().replace(' ', '_') for c in result.columns]
            st.dataframe(
                data=result.sample(100),
                use_container_width=True,
                hide_index=True
            )

            download_cols = st.columns((1, 2))
            with download_cols[0]:
                download_df = convert_df(result)
                st.download_button(
                    label="Download data as .csv",
                    data=download_df,
                    file_name='decrypted_file.csv',
                    mime='text/csv',
                )
            with download_cols[1]:
                st.markdown(f'Total rows of the file: **{result.shape[0]}**')


if __name__ == "__main__":
    run()

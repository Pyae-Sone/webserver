def upload_file(filedata):
    # This function saves the uploaded file to the server
    with open('uploaded_file', 'wb') as f:
        f.write(filedata)